""" A lightweight workflow management tool written in pure Python.

TODO:
    - Task change detection
        - via variable-anonymized AST
    - Priority-based scheduling
"""
from __future__ import annotations
from typing import Callable, ClassVar, Generic, NewType, TypeVar, Any, cast, overload
from typing_extensions import ParamSpec, Concatenate, Self
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, Future, ThreadPoolExecutor, wait, FIRST_COMPLETED, Executor
from functools import wraps
import importlib.util
import ast
import os
import sys
import logging
import inspect
import json
import base64
import shutil

import click
import cloudpickle
import zlib
import diskcache as dc
import networkx as nx


class Context:
    cache_dir = Path(os.getenv('CP_CACHE_DIR', './.cache'))
    executor_name = os.getenv('CP_EXECUTOR', 'process')
    max_workers = int(os.getenv('CP_MAX_WORKERS', -1))
    detect_source_change = bool(os.getenv('CP_DETECT_SOURCE_CHANGE', 0))
    num_cpu = os.cpu_count()

    @classmethod
    def get_executor(cls, max_workers: int | None = None) -> Executor:
        if cls.executor_name == 'process':
            executor_type = ProcessPoolExecutor
        elif cls.executor_name == 'thread':
            executor_type = ThreadPoolExecutor
        else:
            raise ValueError('Unrecognized executor name:', cls.executor_name)
        if max_workers is None:
            max_workers = cls.max_workers
        if max_workers < 0:
            assert isinstance(cls.num_cpu, int)
            assert -cls.num_cpu <= cls.max_workers
            max_workers = cls.num_cpu + 1 + cls.max_workers
        return executor_type(max_workers=max_workers)


LOGGER = logging.getLogger(__name__)


Json = NewType('Json', str)


K = TypeVar('K')
T = TypeVar('T')
P = ParamSpec('P')
R = TypeVar('R', covariant=True)
D = TypeVar('D')


Serializer = tuple[Callable[[Any], bytes], Callable[[bytes], Any]]
DEFAULT_SERIALIZER: Serializer = (cloudpickle.dumps, cloudpickle.loads)


@dataclass(frozen=True)
class Database(Generic[T, D]):
    """ Manage the cache of tasks.
    Layout:
    Context.cache_dir / 'checkpoint' / name / result     # return values
    Context.cache_dir / 'checkpoint' / name / timestamp  # timestamps
    Context.cache_dir / 'checkpoint' / name / data       # other data created by tasks
    """
    name: str
    base_path: Path
    compress_level: int
    result_cache: dc.Cache
    timestamp_cache: dc.Cache
    serializer: Serializer = DEFAULT_SERIALIZER

    @classmethod
    def make(cls, name: str, compress_level: int) -> Self:
        base_path = Context.cache_dir / 'checkpoint' / name
        return Database(
                name=name,
                base_path=base_path,
                compress_level=compress_level,
                result_cache=dc.Cache(base_path / 'result'),
                timestamp_cache=dc.Cache(base_path / 'timestamp'),
                )

    def __post_init__(self) -> None:
        self.data_directory.mkdir(exist_ok=True)
        self.source_path.parent.mkdir(exist_ok=True)

    @property
    def data_directory(self) -> Path:
        return Path(self.base_path) / 'data'

    @property
    def source_path(self) -> Path:
        return Path(self.base_path) / 'code' / 'source.txt'

    def update_source_if_necessary(self, source: str) -> datetime:
        # Update source cache
        if self.source_path.exists():
            cached_source = open(self.source_path, 'r').read()
        else:
            cached_source = None
        if cached_source != source:
            open(self.source_path, 'w').write(source)
        return self.load_source_timestamp()

    def load_source_timestamp(self) -> datetime:
        timestamp = self.source_path.stat().st_mtime_ns / 10 ** 9
        return datetime.fromtimestamp(timestamp)

    def _dumps(self, obj: Any) -> bytes:
        dumps, _ = self.serializer
        return zlib.compress(dumps(obj), level=self.compress_level)

    def _loads(self, data: bytes) -> Any:
        _, loads = self.serializer
        return loads(zlib.decompress(data))

    def save(self, key: Json, obj: T) -> datetime:
        data = self._dumps(obj)
        with self.result_cache as ref:
            ref[key] = data

        timestamp = datetime.now()
        with self.timestamp_cache as ref:
            ref[key] = timestamp.timestamp()
        return timestamp

    def load(self, key: Json) -> T:
        with self.result_cache as ref:
            data = ref[key]
        return self._loads(data)

    def load_timestamp(self, key: Json) -> datetime:
        with self.timestamp_cache as ref:
            ts = ref[key]
        return datetime.fromtimestamp(ts)

    def __contains__(self, key: T) -> bool:
        with self.result_cache as ref:
            return key in ref

    def list_keys(self) -> list[str]:
        with self.result_cache as ref:
            return list(map(str, ref))

    def _get_caches(self) -> list[dc.Cache]:
        return [self.result_cache, self.timestamp_cache]

    def clear(self) -> None:
        for cache in self._get_caches():
            cache.clear()
        if self.data_directory.exists():
            shutil.rmtree(self.data_directory)
        self.data_directory.mkdir()

    def delete(self, key: Json) -> None:
        for cache in self._get_caches():
            with cache as ref:
                del ref[key]


Runner = Callable[[], R]  # Delayed computation
RunnerFactory = Callable[P, Runner[R]]


TaskKey = tuple[str, Json]


@dataclass(frozen=True)
class TaskSkeleton(Generic[R]):
    task_factory: TaskFactory[..., R]
    key: Json

    _register: ClassVar[dict[TaskKey, Runner[Any]]] = dict()

    def to_tuple(self) -> TaskKey:
        return self.task_factory.get_db_name(), self.key

    @property
    def arg_id(self) -> str:
        _, arg_str = self.to_tuple()
        return base64.urlsafe_b64encode(arg_str.encode()).decode().replace('=', '')

    @property
    def directory(self) -> Path:
        return Path(self.task_factory.db.data_directory) / self.arg_id

    def clear(self) -> None:
        db = self.task_factory.db
        db.delete(self.key)
        if self.directory.exists():
            shutil.rmtree(self.directory)

    def peek_timestamp(self) -> datetime | None:
        try:
            return self.task_factory.db.load_timestamp(self.key)
        except KeyError:
            return None

    def get_result(self) -> R:
        db = self.task_factory.db
        return db.load(self.key)

    def load_content(self, loader: RunnerFactory[[], R]) -> Task[R]:
        is_root = not self._register

        key = self.to_tuple()
        runner = self._register.get(key, None)
        if runner is None:
            runner = loader()
            self._register[key] = runner
        task = Task(task_factory=self.task_factory, key=self.key, runner=runner)

        if is_root:
            self._register.clear()
        return task


@dataclass(frozen=True)
class Task(TaskSkeleton[R]):
    """ Runner with cache """
    runner: Runner[R]

    def set_result(self) -> None:
        db = self.task_factory.db
        out = self.runner()
        db.save(self.key, out)

    def run(self, *, executor: Executor | None = None, max_workers: int | None = None) -> R:
        return self.run_with_info(executor=executor, max_workers=max_workers)[0]

    def run_with_info(
            self, *,
            executor: Executor | None = None,
            max_workers: int | None = None,
            dump_generations: bool = False
            ) -> tuple[R, dict[str, Any]]:
        graph = TaskGraph.build_from(self)
        if executor is None:
            executor = Context.get_executor(max_workers=max_workers)
        else:
            assert max_workers is None
        info = run_task_graph(graph=graph, executor=executor, dump_generations=dump_generations)
        return self.get_result(), info


@dataclass
class TaskFactory(Generic[P, R]):
    runner_factory: RunnerFactory[P, R]
    db: Database
    max_concurrency: int | None
    source_timestamp: datetime

    def get_db_name(self) -> str:
        return self.db.name

    def clear(self) -> None:
        self.db.clear()

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Task[R]:
        key = _serialize_arguments(self.runner_factory, *args, **kwargs)
        dummy = TaskSkeleton(task_factory=self, key=key)
        return dummy.load_content(loader=lambda: self.runner_factory(*args, **kwargs))


@overload
def task(fn: RunnerFactory[P, R]) -> TaskFactory[P, R]: ...
@overload
def task(*, compress_level: int = 0, max_concurrency: int | None = None) -> Callable[[RunnerFactory[P, R]], TaskFactory[P, R]]: ...
def task(*args, **kwargs) -> Any:
    if args:
        fn, = args
        return _task()(fn)
    else:
        return _task(**kwargs)


def _task(
        *, compress_level: int = 0, max_concurrency: int | None = None
        ) -> Callable[[RunnerFactory[P, R]], TaskFactory[P, R]]:
    """ Convert a runner factory into a task factory. """

    def decorator(fn: RunnerFactory[P, R]) -> TaskFactory[P, R]:
        name = _serialize_function(fn)
        db = Database.make(name=name, compress_level=compress_level)

        source = inspect.getsource(fn)
        formatted_source = ast.unparse(ast.parse(source))
        source_timestamp = db.update_source_if_necessary(formatted_source)

        return wraps(fn)(TaskFactory(
            runner_factory=fn, db=db,
            max_concurrency=max_concurrency,
            source_timestamp=source_timestamp
            ))
    return decorator


def _serialize_function(fn: Callable[..., Any]) -> str:
    return f'{fn.__module__}.{fn.__qualname__}'


def _normalize_arguments(fn: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> dict[str, Any]:
    params = inspect.signature(fn).bind(*args, **kwargs)
    params.apply_defaults()
    return params.arguments


def _serialize_arguments(fn: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> Json:
    arguments = _normalize_arguments(fn, *args, **kwargs)
    return cast(Json, json.dumps(arguments, separators=(',', ':'), sort_keys=True))


AnyTask = Task[Any]
Connector = Callable[[Callable[Concatenate[T, P], R]], Callable[P, R]]  # Takes (T, *P) -> R and return P -> R


@overload
def requires(task: Task[T]) -> Connector[T, P, R]: ...
@overload
def requires(task: list[Task[T]]) -> Connector[list[T], P, R]: ...
@overload
def requires(task: dict[K, Task[T]]) -> Connector[dict[K, T], P, R]: ...
def requires(task: AnyTask | list[AnyTask] | dict[Any, AnyTask]) -> Any:
    """ Register a task dependency """
    if isinstance(task, Task):
        return requires_single(task)
    elif isinstance(task, list):
        return requires_list(task)
    elif isinstance(task, dict):
        return requires_dict(task)
    else:
        raise TypeError(task)


@dataclass(frozen=True)
class Connected(Generic[T, P, R]):
    """ Connect a task to a function. """
    pre_task: Task[T]
    fn: Callable[Concatenate[T, P], R]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        x = self.pre_task.get_result()
        return self.fn(x, *args, **kwargs)

    def get_prerequisites(self) -> list[AnyTask]:
        return [self.pre_task]


def requires_single(task: Task[T]) -> Connector[T, P, R]:
    """ Register a task dependency """
    def decorator(fn: Callable[Concatenate[T, P], R]) -> Callable[P, R]:
        return Connected(task, fn)
    return decorator


@dataclass(frozen=True)
class ListConnected(Generic[T, P, R]):
    """ Connect a list of tasks to a function. """
    pre_tasks: list[Task[T]]
    fn: Callable[Concatenate[list[T], P], R]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        xs = [task.get_result() for task in self.pre_tasks]
        return self.fn(xs, *args, **kwargs)

    def get_prerequisites(self) -> list[AnyTask]:
        return self.pre_tasks


def requires_list(tasks: list[Task[T]]) -> Connector[list[T], P, R]:
    """ Register a task dependency """
    def decorator(fn: Callable[Concatenate[list[T], P], R]) -> Callable[P, R]:
        return ListConnected(tasks, fn)
    return decorator


@dataclass(frozen=True)
class DictConnected(Generic[K, T, P, R]):
    """ Connect a dict of tasks to a function. """
    pre_tasks: dict[K, Task[T]]
    fn: Callable[Concatenate[dict[K, T], P], R]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        xs = {k: task.get_result() for k, task in self.pre_tasks.items()}
        return self.fn(xs, *args, **kwargs)

    def get_prerequisites(self) -> list[AnyTask]:
        return list(self.pre_tasks.values())


def requires_dict(tasks: dict[K, Task[T]]) -> Connector[dict[K, T], P, R]:
    """ Register a task dependency """
    def decorator(fn: Callable[Concatenate[dict[K, T], P], R]) -> Callable[P, R]:
        return DictConnected(tasks, fn)
    return decorator


@dataclass
class RequiresDirectory(Generic[P, R]):
    fn: Callable[Concatenate[Path, P], R]
    directory: Path | None = None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        assert self.directory is not None, 'Directory not set. Bug?'
        if self.directory.exists():
            shutil.rmtree(self.directory)
        self.directory.mkdir()
        return self.fn(self.directory, *args, **kwargs)

    def set_directory(self, path: Path) -> None:
        self.directory = path


def requires_directory(fn: Callable[Concatenate[Path, P], R]) -> Callable[P, R]:
    """ Create fresh directory dedicated to the task """
    return RequiresDirectory(fn)


def get_prerequisite_tasks(task: AnyTask) -> list[AnyTask]:
    deps: list[Task[Any]] = []
    task_fn = task.runner
    while isinstance(task_fn, (Connected, ListConnected, DictConnected, RequiresDirectory)):
        if isinstance(task_fn, (Connected, ListConnected, DictConnected)):
            deps.extend(task_fn.get_prerequisites())
        else:
            task_fn.set_directory(task.directory)
        task_fn = task_fn.fn
    return deps


@dataclass
class TaskGraph:
    G: nx.DiGraph

    @classmethod
    def build_from(cls, root: AnyTask) -> Self:
        G = nx.DiGraph()
        seen: set[TaskKey] = set()
        to_expand = [root]
        while to_expand:
            task = to_expand.pop()
            x = task.to_tuple()
            if x not in seen:
                seen.add(x)
                prerequisite_tasks = get_prerequisite_tasks(task)
                to_expand.extend(prerequisite_tasks)
                G.add_node(x, task=task, timestamp=task.peek_timestamp(), source_timestamp=task.task_factory.source_timestamp)
                G.add_edges_from([(p.to_tuple(), x) for p in prerequisite_tasks])
        out = TaskGraph(G)
        out.trim()
        return out

    @property
    def size(self) -> int:
        return len(self.G)

    def get_task(self, key: TaskKey) -> AnyTask:
        return self.G.nodes[key]['task']

    def trim(self) -> None:
        self._mark_nodes_to_update()
        self._remove_fresh_nodes()
        self._transitive_reduction()

    def _mark_nodes_to_update(self) -> None:
        for x in nx.topological_sort(self.G):
            ts_task = self.G.nodes[x]['timestamp']
            ts_source = self.G.nodes[x]['source_timestamp']
            if ts_task is None or (Context.detect_source_change and ts_task < ts_source):
                self.G.add_node(x, to_update=True)
                continue
            for p in self.G.predecessors(x):
                pred_to_update = self.G.nodes[p]['to_update']
                ts_pred = self.G.nodes[p]['timestamp']
                if pred_to_update or ts_task < ts_pred:
                    self.G.add_node(x, to_update=True)
                    break
            else:
                self.G.add_node(x, to_update=False)

    def _remove_fresh_nodes(self) -> None:
        to_remove = [x for x, attr in self.G.nodes.items() if not attr['to_update']]
        self.G.remove_nodes_from(to_remove)

    def _transitive_reduction(self) -> None:
        TR = nx.transitive_reduction(self.G)
        TR.add_nodes_from(self.G.nodes(data=True))
        self.G = TR

    def get_task_factories(self) -> dict[str, TaskFactory[..., Any]]:
        return dict((path, attr['task'].task_factory) for (path, _), attr in self.G.nodes.items())

    def get_initial_tasks(self) -> list[TaskKey]:
        return [x for x in self.G if self.G.in_degree(x) == 0]

    def pop_with_new_leaves(self, x: TaskKey, disallow_non_leaf: bool = True) -> list[TaskKey]:
        if disallow_non_leaf:
            assert not list(self.G.predecessors(x))

        new_leaves: list[TaskKey] = []
        for y in self.G.successors(x):
            if self.G.in_degree(y) == 1:
                new_leaves.append(y)

        self.G.remove_node(x)
        return new_leaves

    def get_grouped_nodes(self) -> dict[str, list[Json]]:
        out: dict[str, list[Json]] = defaultdict(list)
        for x in self.G:
            path, args = x
            out[path].append(args)
        return dict(out)


def _group_nodes_by_db(tasks: list[TaskKey]) -> dict[str, list[TaskKey]]:
    out = defaultdict(list)
    for x in tasks:
        db, _ = x
        out[db].append(x)
    return dict(out)


def run_task_graph(graph: TaskGraph, executor: Executor, dump_generations: bool = False) -> dict[str, Any]:
    """ Consume task graph concurrently.
    """
    stats = {k: len(args) for k, args in graph.get_grouped_nodes().items()}
    LOGGER.info(f'Following tasks will be called: {stats}')
    info = {'stats': stats, 'generations': []}

    # Read concurrency budgets
    budgets: dict[str, int] = {}
    occupied: dict[str, int] = {}
    for path, fac in graph.get_task_factories().items():
        mc = fac.max_concurrency
        if mc is not None:
            budgets[path] = mc
            occupied[path] = 0

    # Execute tasks
    standby = _group_nodes_by_db(graph.get_initial_tasks())
    in_process: set[Future[TaskKey]] = set()
    with executor as executor:
        while standby or in_process:
            # Log some stats
            LOGGER.info(
                    f'nodes: {graph.size}, '
                    f'standby: {len(standby)}, '
                    f'in_process: {len(in_process)}'
                    )
            if dump_generations:
                info['generations'].append(graph.get_grouped_nodes())

            # Submit all leaf tasks
            leftover: dict[str, list[TaskKey]] = {}
            for path, keys in standby.items():
                if path in budgets:
                    free = budgets[path] - occupied[path]
                    to_submit, to_hold = keys[:free], keys[free:]
                    occupied[path] += len(to_submit)
                    if to_hold:
                        leftover[path] = to_hold
                else:
                    to_submit = keys

                for key in to_submit:
                    future = executor.submit(_run_task, cloudpickle.dumps(graph.get_task(key)))
                    in_process.add(future)

            # Wait for the first tasks to complete
            done, in_process = wait(in_process, return_when=FIRST_COMPLETED)

            # Update graph
            standby = defaultdict(list, leftover)
            for done_future in done:
                x_done = done_future.result()

                # Update occupied
                path = x_done[0]
                if path in occupied:
                    occupied[path] -= 1
                    assert occupied[path] >= 0

                # Remove node from graph
                ys = graph.pop_with_new_leaves(x_done)

                # Update standby
                for y in ys:
                    standby[y[0]].append(y)

    # Sanity check
    assert graph.size == 0, f'Graph is not empty. Should not happen.'
    assert all(n == 0 for n in occupied.values()), 'Incorrect task count. Should not happen.'
    return info


def _run_task(task_data: bytes) -> tuple[str, Json]:
    task = cloudpickle.loads(task_data)
    assert isinstance(task, Task)
    task.set_result()
    return task.to_tuple()


@click.command
@click.argument('taskfile', type=Path)
@click.option('-e', '--entrypoint', default='main', help='Task name for entrypoint.')
@click.option('-t', '--exec-type', type=click.Choice(['process', 'thread']), default='process')
@click.option('-w', '--max-workers', type=int, default=-1)
@click.option('--cache-dir', type=Path, default=None)
@click.option('-D', '--detect-source-change', is_flag=True, help='Automatically discard the cache per task once the source code (AST) is changed.')
def main(taskfile: Path, entrypoint: str, exec_type: str, max_workers: int, cache_dir: Path | None, detect_source_change: bool):
    # Set arguments as environment variables
    os.environ['CP_EXECUTOR'] = exec_type
    os.environ['CP_MAX_WORKERS'] = str(max_workers)
    os.environ['CP_CACHE_DIR'] = str(taskfile.parent / '.cache') if cache_dir is None else str(cache_dir)
    os.environ['CP_DETECT_SOURCE_CHANGE'] = str(int(detect_source_change))

    # Run script as module
    module_name = taskfile.with_suffix('').name
    spec = importlib.util.spec_from_file_location(module_name, taskfile)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Run the main task
    entrypoint_fn = getattr(module, entrypoint)
    assert type(entrypoint_fn).__name__ == TaskFactory.__name__, \
            f'Taskfile `{taskfile}` should contain a task(factory) `{entrypoint}`, but found `{entrypoint_fn}`.'
    entrypoint_fn = cast(TaskFactory, entrypoint_fn)
    task = entrypoint_fn()
    task.run()
    print(task.directory)
    return 0


if __name__ == '__main__':
    sys.exit(main())

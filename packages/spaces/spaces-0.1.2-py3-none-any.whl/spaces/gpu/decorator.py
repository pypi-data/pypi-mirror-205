"""
"""
from __future__ import annotations

import multiprocessing
import os
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from multiprocessing import Queue as _Queue
from multiprocessing.queues import Empty # type: ignore
from queue import SimpleQueue
from typing import Any
from typing import Callable
from typing import Generator
from typing import Generic
from typing import TypeVar
from typing_extensions import ParamSpec
from typing_extensions import TypeAlias

import psutil

from . import client
from .patching import Torch


_fork = multiprocessing.get_context('fork')
Process = _fork.Process
Queue = _fork.Queue

_Arg: TypeAlias = 'tuple[tuple[Any], dict[str, Any]]'
_Res = TypeVar('_Res')
_Param = ParamSpec('_Param')


@dataclass
class Worker(Generic[_Res]):
    process: Process
    arg_queue: _Queue[_Arg]
    res_queue: _Queue[_Res]


def GPU(task: Callable[_Param, _Res]) -> Callable[_Param, _Res]:

    worker: Worker[list[_Res] | Exception] | None = None

    def process_wrapper(*args: _Param.args, **kwargs: _Param.kwargs) -> _Res:
        print("process_wrapper")
        nonlocal worker
        if worker is None or not worker.process.is_alive():
            arg_queue: _Queue[_Arg] = Queue()
            res_queue: _Queue[list[_Res] | Exception] = Queue()
            fds = [c.fd for c in psutil.Process().connections()]
            process = Process(target=thread_wrapper, args=(arg_queue, res_queue, fds), daemon=True)
            worker = Worker(process=process, arg_queue=arg_queue, res_queue=res_queue)
            process.start()
        client.schedule()
        worker.arg_queue.put_nowait((args, kwargs))
        while worker.process.is_alive():
            try:
                res = worker.res_queue.get(timeout=1)
                if isinstance(res, Exception):
                    client.release(fail=True)
                    raise res
            except Empty:
                continue
            client.release()
            return res[0]
        client.release(fail=True)
        raise Exception("Operation aborted")
        

    def thread_wrapper(
        arg_queue: '_Queue[_Arg]',
        res_queue: '_Queue[list[_Res] | Exception]',
        fds: list[int],
    ):
        Torch.unpatch()
        for fd in fds:
            os.close(fd)
        while True:
            args, kwargs = arg_queue.get()
            with ThreadPoolExecutor() as executor:
                future = executor.submit(task, *args, **kwargs)
            try:
                res = [future.result()]
            except Exception as e:
                traceback.print_exc()
                res = e
            res_queue.put_nowait(res)
    
    return process_wrapper


def GPUGenerator(task: Callable[_Param, Generator[_Res, None, None]]) -> Callable[_Param, Generator[_Res, None, None]]:

    worker: Worker[list[_Res] | Exception | None] | None = None

    def process_wrapper(*args: _Param.args, **kwargs: _Param.kwargs) -> Generator[_Res, None, None]:
        print("process_wrapper")
        nonlocal worker
        if worker is None or not worker.process.is_alive():
            arg_queue: _Queue[_Arg] = Queue()
            res_queue: _Queue[list[_Res] | Exception | None] = Queue()
            fds = [c.fd for c in psutil.Process().connections()]
            process = Process(target=thread_wrapper, args=(arg_queue, res_queue, fds), daemon=True)
            worker = Worker(process=process, arg_queue=arg_queue, res_queue=res_queue)
            process.start()

        client.schedule()

        worker.arg_queue.put((args, kwargs))

        yield_qeueue: SimpleQueue[list[_Res] | Exception | None] = SimpleQueue()
        def fill_yield_queue(worker: Worker):
            while worker.process.is_alive():
                try:
                    res = worker.res_queue.get(timeout=1)
                except Empty:
                    continue
                if isinstance(res, Exception):
                    client.release(fail=True)
                    yield_qeueue.put(res)
                    return
                if res is None:
                    client.release()
                    yield_qeueue.put(None)
                    return
                yield_qeueue.put(res)
            client.release(fail=True)
            yield_qeueue.put(Exception("Operation aborted"))

        with ThreadPoolExecutor() as e:
            e.submit(fill_yield_queue, worker)
            while True:
                res = yield_qeueue.get()
                if isinstance(res, Exception):
                    raise res
                if res is None:
                    break
                yield res[0]


    def thread_wrapper(
        arg_queue: _Queue[_Arg],
        res_queue: _Queue[list[_Res] | Exception | None],
        fds: list[int],
    ):
        Torch.unpatch()
        for fd in fds:
            os.close(fd)
        while True:
            args, kwargs = arg_queue.get()
            def iterate():
                try:
                    for res in task(*args, **kwargs): # type: ignore
                        res_queue.put([res])
                except Exception as e:
                    traceback.print_exc()
                    res_queue.put(e)
            with ThreadPoolExecutor() as executor:
                executor.submit(iterate)
            res_queue.put(None)

    return process_wrapper

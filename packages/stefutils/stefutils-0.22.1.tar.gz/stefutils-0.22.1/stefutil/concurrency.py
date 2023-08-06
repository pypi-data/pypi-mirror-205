"""
concurrency

intended for (potentially heavy) data processing
"""

import os
import concurrent.futures
from typing import List, Tuple, Dict, Iterable, Callable, TypeVar, Union

import numpy as np
from tqdm.std import tqdm as std_tqdm  # root for type check
from tqdm.auto import tqdm
from tqdm.contrib import concurrent as tqdm_concurrent

from stefutil.container import group_n
from stefutil.prettier import ca


__all__ = ['conc_map', 'batched_conc_map', 'conc_yield']


T = TypeVar('T')
K = TypeVar('K')

MapFn = Callable[[T], K]
BatchedMapFn = Callable[[Tuple[List[T], int, int]], List[K]]


def _check_conc_mode(mode: str):
    ca.check_mismatch('Concurrency Mode', mode, ['thread', 'process'])


def conc_map(
        fn: MapFn, args: Iterable[T], with_tqdm: Union[bool, Dict] = False, n_worker: int = os.cpu_count(),
        mode: str = 'thread'
) -> Iterable[K]:
    """
    Wrapper for `concurrent.futures.map`

    :param fn: A function
    :param args: A list of elements as input to the function
    :param with_tqdm: If true, progress bar is shown
        If dict, treated as `tqdm` concurrent kwargs
            note `chunksize` is helpful
    :param n_worker: Number of concurrent workers
    :param mode: One of ['thread', 'process']
        Function has to be pickleable if 'process'
    :return: Iterator of `lst` elements mapped by `fn` with thread concurrency
    """
    _check_conc_mode(mode=mode)
    if with_tqdm:
        cls = tqdm_concurrent.thread_map if mode == 'thread' else tqdm_concurrent.process_map
        tqdm_args = (isinstance(with_tqdm, dict) and with_tqdm) or dict()
        return cls(fn, args, max_workers=n_worker, **tqdm_args)
    else:
        cls = concurrent.futures.ThreadPoolExecutor if mode == 'thread' else concurrent.futures.ProcessPoolExecutor
        with cls(max_workers=n_worker) as executor:
            return executor.map(fn, args)


"""
classes instead of nested functions, pickleable for multiprocessing
"""


class Map:
    def __init__(self, fn, pbar=None):
        self.fn = fn
        self.pbar = pbar

    def __call__(self, x):
        ret = self.fn(x)
        if self.pbar:
            self.pbar.update(1)
        return ret


class BatchedMap:
    def __init__(self, fn, is_batched_fn: bool, pbar=None):
        self.fn = fn if is_batched_fn else Map(fn, pbar)
        self.pbar = pbar
        self.is_batched_fn = is_batched_fn

    def __call__(self, args):
        # adhere to single-argument signature for `conc_map`
        lst, s, e = args
        if self.is_batched_fn:
            ret = self.fn(lst[s:e])
            if self.pbar:
                # TODO: update on the element level may not give a good estimate of completion if too large a batch
                self.pbar.update(e-s + 1)
            return ret
        else:
            return [self.fn(lst[i]) for i in range(s, e)]


def batched_conc_map(
        fn: Union[MapFn, BatchedMapFn],
        args: Union[Iterable[T], List[T], np.array], n: int = None, n_worker: int = os.cpu_count(),
        batch_size: int = None,
        with_tqdm: Union[bool, dict, tqdm] = False,
        is_batched_fn: bool = False,
        mode: str = 'thread'
) -> List[K]:
    """
    Batched concurrent mapping, map elements in list in batches
    Operates on batch/subset of `lst` elements given inclusive begin & exclusive end indices

    :param fn: A map function that operates on a single element
    :param args: A list of elements to map
    :param n: #elements to map if `it` is not Sized
    :param n_worker: Number of concurrent workers
    :param batch_size: Number of elements for each sub-process worker
        Inferred based on number of workers if not given
    :param with_tqdm: If true, progress bar is shown
        progress is shown on an element-level if possible
    :param is_batched_fn: If true, `conc_map` is called on the function passed in,
        otherwise, A batched version is created internally
    :param mode: One of ['thread', 'process']

    .. note:: Concurrently is not invoked if too little list elements given number of workers
        Force concurrency with `batch_size`
    """
    n = n or len(args)
    if (n_worker > 1 and n > n_worker * 4) or batch_size:  # factor of 4 is arbitrary, otherwise not worse the overhead
        preprocess_batch = batch_size or round(n / n_worker / 2)
        strts: List[int] = list(range(0, n, preprocess_batch))
        ends: List[int] = strts[1:] + [n]  # inclusive begin, exclusive end
        lst_out = []

        pbar = None
        if with_tqdm:
            tqdm_args = dict(mode=mode, n_worker=n_worker)
            if mode == 'thread':  # Able to show progress on element level
                # so create such a progress bar & disable for `conc_map`
                tqdm_args['with_tqdm'] = False
                if isinstance(with_tqdm, bool):
                    pbar = tqdm(total=n)
                elif isinstance(with_tqdm, dict):
                    _args = dict(total=n)
                    _args.update(with_tqdm)
                    pbar = tqdm(**_args)
                else:
                    assert isinstance(with_tqdm, std_tqdm)
                    pbar = with_tqdm
            else:  # `process`, have to rely on `tqdm.concurrent` which shows progress on batch level, see `conc_map`
                tqdm_args['with_tqdm'] = with_tqdm
        else:
            tqdm_args = dict(with_tqdm=False)

        batched_map = BatchedMap(fn, is_batched_fn, pbar)
        map_out = conc_map(fn=batched_map, args=[(args, s, e) for s, e in zip(strts, ends)], **tqdm_args)
        for lst_ in map_out:
            lst_out.extend(lst_)
        return lst_out
    else:
        gen = tqdm(args) if with_tqdm else args
        if is_batched_fn:
            _args = gen, 0, n
            return fn(*_args)
        else:
            return [fn(x) for x in gen]


class BatchedFn:
    def __init__(self, fn: MapFn, pbar=None):
        self.fn = fn
        self.pbar = pbar

    def __call__(self, args: Iterable[T]) -> List[K]:
        """
        No order enforced
        """
        ret = []
        for a in args:
            ret.append(self.fn(a))
            if self.pbar is not None:
                self.pbar.update(1)
        return ret


def conc_yield(
        fn: MapFn, args: Iterable[T], with_tqdm: Union[bool, Dict] = False,
        n_worker: int = os.cpu_count()-1,  # since the calling script consumes one process
        mode: str = 'thread', batch_size: Union[int, bool] = None
) -> Iterable[K]:
    """
    Wrapper for `concurrent.futures`, yielding results as they become available, irrelevant of order
        Intended for loading up data where each instance takes relatively heavy processing time

    :param fn: A function
    :param args: A list of elements as input to the function
    :param with_tqdm: If true, progress bar is shown
        If dict, treated as `tqdm` concurrent kwargs
            note `chunksize` is helpful
    :param n_worker: Number of concurrent workers
    :param mode: One of ['thread', 'process']
        Function has to be pickleable if 'process'
    :param batch_size: Number of elements for each sub-process worker
        Intended to lower concurrency overhead
    :return: Iterator of `lst` elements mapped by `fn` with thread concurrency
    """
    _check_conc_mode(mode=mode)

    cls = concurrent.futures.ThreadPoolExecutor if mode == 'thread' else concurrent.futures.ProcessPoolExecutor
    executor = cls(max_workers=n_worker)

    pbar = None
    if with_tqdm:
        tqdm_args = (isinstance(with_tqdm, dict) and with_tqdm) or dict()
        pbar = tqdm(**tqdm_args)

    if batch_size:
        batch_size = 32 if isinstance(batch_size, bool) else batch_size
        # pbar doesn't work w/ pickle hence multiprocessing
        fn = BatchedFn(fn=fn, pbar=pbar if mode == 'thread' else None)
        futures = set(executor.submit(fn, args_) for args_ in group_n(args, batch_size))
        for f in concurrent.futures.as_completed(futures):
            if mode == 'thread':
                res = f.result()
                futures.remove(f)
                yield from res
            else:
                res = f.result()
                futures.remove(f)
                if pbar is not None:
                    pbar.update(len(res))
                yield from res
    else:
        futures = set(executor.submit(fn, a) for a in args)
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            futures.remove(f)
            if with_tqdm:
                pbar.update(1)
            yield res


# DEV = True
DEV = False
if DEV:
    import time
    import random

    from stefutil.prettier import pl, mic


    def work(task_idx):
        t = random.uniform(1, 4)
        t = round(t, 3)
        print(f'Task {pl.i(task_idx)} launched, will sleep for {pl.i(t)} s')
        time.sleep(t)

        print(f'Task {pl.i(task_idx)} is done')
        return task_idx


if __name__ == '__main__':
    def work(task_idx):
        t = random.uniform(1, 4)
        print(f'Task {pl.i(task_idx)} launched, will sleep for {pl.i(t)}s')
        time.sleep(t)

        print(f'Task {pl.i(task_idx)} is done')
        return task_idx

    def try_concurrent_yield():

        # this will gather all results and return
        # with ThreadPoolExecutor() as executor:
        #     for result in executor.map(work, range(3)):
        #         print(result)
        # executor = concurrent.futures.ThreadPoolExecutor()
        executor = concurrent.futures.ProcessPoolExecutor()
        args = list(range(4))
        futures = [executor.submit(work, a) for a in args]
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            mic(res)
    # try_concurrent_yield()

    def check_conc_yield():
        batch = False

        if batch:
            bsz = 4
            n = 100
        else:
            bsz = None
            n = 10

        it = range(n)
        with_tqdm = dict(total=n)
        n_worker = 4

        mode = 'process'
        # mode = 'thread'
        for res in conc_yield(fn=work, args=it, with_tqdm=with_tqdm, n_worker=n_worker, mode=mode, batch_size=bsz):
            mic(res)
    # check_conc_yield()

    def test_conc_mem_use():
        from concurrent.futures import ThreadPoolExecutor, as_completed

        from stefutil.prettier import pl, get_logger

        n = 30
        # remove_job = True
        remove_job = False
        logger = get_logger('Mem Use')

        def dummy_fn(x: int):
            t = random.uniform(0.2, 1)
            logger.info(f'Calling dummy_fn w/ arg {pl.i(x)}, will sleep for {pl.i(t)}s')
            time.sleep(t)

            return x, [random.random() for _ in range(int(1e6))]

        # test_code = True
        test_code = False
        if test_code:
            n_processed = 0
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(dummy_fn, i) for i in range(n)}
                for f in as_completed(futures):
                    i, _ = f.result()
                    if remove_job:
                        futures.remove(f)
                    n_processed += 1
                    logger.info(f'Process {pl.i(i)} terminated, {pl.i(n_processed)} / {pl.i(n)} processed')
        else:
            args = dict(with_tqdm=dict(total=n), n_worker=3, mode='process', batch_size=4)
            for i in conc_yield(fn=dummy_fn, args=range(n), **args):
                i, _ = i
                logger.info(f'Process {pl.i(i)} terminated')
    test_conc_mem_use()

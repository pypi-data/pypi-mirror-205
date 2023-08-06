from typing import Generator, Any
from ..Decorators import threadify
from ..MetaClasses import AtomicClassMeta
from ..DataStructures import Queue


class AtomicQueue(Queue, metaclass=AtomicClassMeta):
    pass


def join_generators(*generators) -> Generator[Any, None, None]:
    """joins an arbitrary amount of generators to yield objects as soon someone yield an object

    Yields:
        Generator[Any, None, None]: resulting generator
    """
    q = AtomicQueue()
    threads_status = [False for _ in range(len(generators))]

    @threadify
    def yield_from_one(thread_id: int, gen):
        nonlocal threads_status
        try:
            while True:
                q.push(next(gen))
        except StopIteration:
            threads_status[thread_id] = True

    for i, gen in enumerate(generators):
        yield_from_one(i, gen)

    while not all(threads_status):
        while q.is_empty():
            pass
        yield q.pop()


__all__ = [
    "join_generators"
]

# spinner_proc.py

# credits: Adapted from Michele Simionato's
# multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/675659.html

# tag::SPINNER_PROC_IMPORTS[]
from multiprocessing import Process, Event  # <1>
from multiprocessing import synchronize     # <2>
import itertools
import time

def spin(msg: str, done: synchronize.Event) -> None:  # <3>
# end::SPINNER_PROC_IMPORTS[]
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

def slow() -> int:
    time.sleep(3)
    return 42

# tag::SPINNER_PROC_SUPER[]
def supervisor() -> int:
    done = Event()
    spinner = Process(target=spin,               # <4>
                      args=('thinking!', done))
    print('spinner object:', spinner)            # <5>
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result
# end::SPINNER_PROC_SUPER[]

def main() -> None:
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()


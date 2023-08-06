#!/usr/bin/env python3
import contextlib
import sys
import termios
import time
import typing


@contextlib.contextmanager
def non_canonical_mode() -> typing.Generator[None, None, None]:
    old_term = termios.tcgetattr(sys.stdin.fileno())
    new_term = termios.tcgetattr(sys.stdin.fileno())

    new_term[3] &= ~(termios.ICANON | termios.ECHO)
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, new_term)

    try:
        yield
    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, old_term)


def test_click_speed(num_clicks: int) -> None:
    with non_canonical_mode():
        sys.stdin.read(1)
        start_time = time.time()
        clicks = 1

        while clicks < num_clicks:
            sys.stdin.read(1)
            clicks += 1
            time_elapsed = time.time() - start_time
            print(f"\x1b[2K\r{(clicks / time_elapsed) * 60 / 4:.2f}bpm", end="")


def input_int(prompt: str) -> int:
    user_input = ""
    while not user_input.isdecimal():
        user_input = input(prompt)
    return int(user_input)


def main() -> int:
    num_clicks = input_int("Number of clicks: ")
    test_click_speed(num_clicks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import pytest


def test_a():
    assert 'x' == 'x'
    assert 'y' == 'y'
    assert 'x' == 'y'
    assert 'x' == 'y'


def test_b():
    print('i totally forgot to include a main maybe thats why this wont run')


if __name__ == '__main__':
    test_a()
    test_b()

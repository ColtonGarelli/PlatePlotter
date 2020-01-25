import pytest


def test_a():
    assert 'x' == 'x'
    assert 'y' == 'y'


def test_b():

    with pytest.raises(AssertionError):
        assert 'x' == 'y', "We didnt do it, boys"
    assert 'x' == 'y', "We didnt do it, boys"

if __name__ == '__main__':
    test_a()
    test_b()

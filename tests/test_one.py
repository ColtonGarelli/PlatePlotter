import pytest


def test_a():
    assert 'x' == 'x'
    assert 'y' == 'y'

    assert 'x' == 'y'


def test_b():
    assert 'x' == 'y', "We didnt do it, boys"
    with pytest.raises(AssertionError):
        assert 'x' == 'y'

if __name__ == '__main__':
    test_a()
    test_b()

from herald.utils import truncate


def test_trunc_list_long():
    args = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = truncate(args, 10)
    assert result == "[1, 2..<list>.., 10]"


def test_trunc_list_nested():
    args = [{"test": 1}, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], (1, 2, 3)]
    result = truncate(args, 10)
    assert result == "[{'te..<list>.., 3)]"  # fmt: skip


def test_trunc_dict():
    kwargs = {"test": "thisisaverylongstringvalue", "test2": 1}
    result = truncate(kwargs, 10)
    assert result == "{'tes..<dict>..': 1}"  # fmt: skip


def test_trunc_bool():
    args = True
    result = truncate(args, 10)
    assert result is True

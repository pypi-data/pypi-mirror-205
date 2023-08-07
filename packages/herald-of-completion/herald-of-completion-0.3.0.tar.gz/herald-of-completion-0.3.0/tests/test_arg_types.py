from herald.utils import build_arg_string, build_kwarg_string


def test_arg_str():
    args = ["test"]
    result = build_arg_string(args)
    assert result == "'test'"


def test_arg_int():
    args = [12]
    result = build_arg_string(args)
    assert result == "12"


def test_arg_float():
    args = [12.0]
    result = build_arg_string(args)
    assert result == "12.0"


def test_arg_list():
    args = [[1, 2, 3]]
    result = build_arg_string(args)
    assert result == "[1, 2, 3]"


def test_arg_list_nested():
    args = [[1, 2, 3], {"key": "val"}, {"key2": "verylongvalue2"}]
    result = build_arg_string(args)
    assert result == "[1, 2, 3], {'key..<dict>..val'}, {'key..<dict>..ue2'}"


def test_arg_tuple():
    args = [(1, 2, 3)]
    result = build_arg_string(args)
    assert result == "(1, 2, 3)"


def test_arg_dict():
    args = [{"test": 1}]
    result = build_arg_string(args)
    assert result == "{'tes..<dict>..': 1}"  # fmt: skip


def test_arg_set():
    args = [{1, 2, 3}]
    result = build_arg_string(args)
    assert result == "{1, 2, 3}"


def test_arg_bool():
    args = [True]
    result = build_arg_string(args)
    assert result == "True"


def test_arg_none():
    args = [None]
    result = build_arg_string(args)
    assert result == "None"


def test_arg_combo():
    args = [1, 2.0, (1, 2, 3), {"test": "no"}, {1, 2, 3}]
    result = build_arg_string(args)
    assert result == "1, 2.0, (1, 2, 3), {'tes..<dict>..'no'}, {1, 2, 3}"  # fmt: skip


def test_kwarg_str():
    kwargs = {"test": "test"}  # fmt: skip
    result = build_kwarg_string(kwargs)
    assert result == "test='test'"  # fmt: skip


def test_kwarg_int():
    kwargs = {"test": 1}
    result = build_kwarg_string(kwargs)
    assert result == "test=1"


def test_kwarg_float():
    kwargs = {"test": 1.0}
    result = build_kwarg_string(kwargs)
    assert result == "test=1.0"


def test_kwarg_list():
    kwargs = {"test": [1, 2, 3]}
    result = build_kwarg_string(kwargs)
    assert result == "test=[1, 2, 3]"


def test_kwarg_tuple():
    kwargs = {"test": (1, 2, 3)}
    result = build_kwarg_string(kwargs)
    assert result == "test=(1, 2, 3)"


def test_kwarg_dict():
    kwargs = {"test": {"test": 1}}  # fmt: skip
    result = build_kwarg_string(kwargs)
    assert result == "test={'tes..<dict>..': 1}"  # fmt: skip


def test_kwarg_bool():
    kwargs = {"test": True}
    result = build_kwarg_string(kwargs)
    assert result == "test=True"


def test_kwarg_set():
    kwargs = {"test": {1, 2, 3}}
    result = build_kwarg_string(kwargs)
    assert result == "test={1, 2, 3}"


def test_kwarg_none():
    kwargs = {"test": None}
    result = build_kwarg_string(kwargs)
    assert result == "test=None"


def test_kwarg_combo():
    kwargs = {"test": "test", "test2": 1}  # fmt: skip
    result = build_kwarg_string(kwargs)
    assert result == "test='test', test2=1"  # fmt: skip

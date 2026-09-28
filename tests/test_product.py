# ruff:noqa
import pytest
from best_buy_zwei.products import (
    Product,
    validate_non_negative_int,
    validate_non_negative_num,
    validate_non_empty_str,
)


"""
validate_non_negative_int
3 => 3
0 => 0
-1 => VE VALIDATE_ERR_MUST_BE_POSITIVE für "name"
True => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
2.0 => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
"2.0" => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
None => TE VALIDATE_ERR_NOT_OF_TYPE für "name"
"""


@pytest.mark.parametrize("value, result", [(3, 3), (0, 0)])
def test_validate_non_negative_int_for_valid_calls(value, result):
    assert validate_non_negative_int("_", value) == result


def test_validate_non_negative_int_ValueE_for_negative():
    with pytest.raises(ValueError) as err:
        validate_non_negative_int("bezeichner", -1)
    assert "bezeichner" in str(err.value)


@pytest.mark.parametrize("value", [True, 2.0, "2.0", None])
def test_validate_non_negative_int_TypeE_for_bad_type(value):
    with pytest.raises(TypeError) as err:
        validate_non_negative_int("bezeichner", value)
    assert "bezeichner" in str(err.value)


"""
validate_non_negative_num
3       => 3
3.0     => 3.0
0       => 0

-1      => ValueError w name

True    => TypeError w name
"2.0"   => "
None    => "
"""


@pytest.mark.parametrize("value, result", [(3, 3), (3.0, 3.0), (0, 0)])
def test_validate_non_negative_num_valid_calls(value, result):
    assert validate_non_negative_num("_", value) == result


def test_validate_non_negative_num_ValueE_for_negative():
    with pytest.raises(ValueError) as err:
        validate_non_negative_num("bezeichner", -1)
    assert "bezeichner" in str(err)


@pytest.mark.parametrize("value", (True, "2.0", None))
def test_validate_non_negative_num_TypeE_for_bad_type(value):
    with pytest.raises(TypeError) as err:
        validate_non_negative_num("bezeichner", value)
    assert "bezeichner" in str(err)


"""
validate_non_empty_str
"bla"       => "bla"
2           => TypeError w name
True        => "
None        => "
""          => ValueError w name
" "         => "
"""


def test_validate_non_empty_str_valid_call():
    assert validate_non_empty_str("_", "bla") == "bla"


@pytest.mark.parametrize("value", [2, True, None])
def test_validate_non_empty_str_TypeError_for_bad_type(value):
    with pytest.raises(TypeError) as err:
        validate_non_empty_str("bezeichner", value)
    assert "bezeichner" in str(err)


@pytest.mark.parametrize("value", ["", " "])
def test_validate_non_empty_str_ValueError_for_bad_type(value):
    with pytest.raises(ValueError) as err:
        validate_non_empty_str("bezeichner", value)
    assert "bezeichner" in str(err)


if __name__ == "__main__":
    pytest.main()

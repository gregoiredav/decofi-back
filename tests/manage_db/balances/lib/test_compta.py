import pytest

from manage_db.balances.lib.compta import flag_aggregat_depenses


@pytest.mark.parametrize("test_input,expected", [
    (('34', ['341'], []), False),
    (('341', ['341'], ['34']), False),
    (('341', ['34'], ['341']), False),
    (('341', ['34'], ['331']), True),
])
def test_flag_aggregat_depenses(test_input, expected):
    assert flag_aggregat_depenses(*test_input) == expected

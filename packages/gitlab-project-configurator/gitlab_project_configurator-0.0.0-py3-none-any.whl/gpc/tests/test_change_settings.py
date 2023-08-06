# Standard Library
import re

# Third Party Libraries
import pytest

# Gitlab-Project-Configurator Modules
from gpc.change_setting import ChangeSetting


SPACE = " "


@pytest.mark.parametrize(
    "before, after, expected_str",
    [
        (None, "something", "property_name None => something (added)"),
        (
            "something",
            "somethingelse",
            "property_name something => somethingelse (updated)",
        ),
    ],
)
def test_change_setting(before, after, expected_str):
    cs = ChangeSetting("property_name", before, after)
    rs = str(cs).strip()
    pattern = re.compile(r"\s+")
    rs = re.sub(pattern, " ", rs)
    assert rs == expected_str

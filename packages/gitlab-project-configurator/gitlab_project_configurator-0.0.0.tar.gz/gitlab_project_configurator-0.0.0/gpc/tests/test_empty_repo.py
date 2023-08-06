"""
test empty repo
----------------------------------
"""

# Third Party Libraries
from dictns import Namespace

# Gitlab-Project-Configurator Modules
from gpc.parameters import GpcParameters
from gpc.parameters import RunMode
from gpc.project_rule_executor import ProjectRuleExecutor


# pylint: disable=duplicate-code


def test_empty_repo(
    mocker,
    fake_gitlab,
    fake_project,
):
    project_rules = Namespace(
        {
            "default_branch": "master",
            "description": "new_description",
        }
    )
    fake_project.empty_repo = True
    p = ProjectRuleExecutor(
        fake_gitlab,
        "fake/path/to/project",
        project_rules,
        gpc_params=GpcParameters(
            mocker.Mock("fake_config"),
            config_project_url="new project url",
            gpc_enabled_badge_url="new image url",
            mode=RunMode.APPLY,
        ),
    )
    assert not p.executors

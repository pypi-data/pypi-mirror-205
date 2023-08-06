"""
Make the merge requests approval settings.
"""
# Standard Library

# Third Party Libraries
import attr

from structlog import get_logger

# Gitlab-Project-Configurator Modules
from gpc.executors.approvers_mixin import ChangeApprovers as ChangeApprovalSettings
from gpc.executors.approvers_mixin import OptionApproversMixin
from gpc.executors.profile_member_mixin import ProfileMemberMixin
from gpc.executors.properties_updator import ChangePropertyExecutor
from gpc.helpers.project_approval import ProjectApprovalSettings
from gpc.parameters import RunMode
from gpc.property_manager import PropertyBean


log = get_logger()


@attr.s
class ProjectOptions(PropertyBean, OptionApproversMixin):
    name = attr.ib(default="approval settings")
    enable_committers_approvers = attr.ib(default=None)  # type: bool
    reset_approvals_on_push = attr.ib(default=None)  # type: bool
    can_override_approvals_per_merge_request = attr.ib(default=None)  # type: bool
    enable_self_approval = attr.ib(default=None)  # type: bool

    @staticmethod
    def to_project_approval_settings(api_settings):
        project_settings = ProjectOptions()
        project_settings.enable_self_approval = api_settings.merge_requests_author_approval
        project_settings.enable_committers_approvers = api_settings.enable_committers_approvers
        project_settings.reset_approvals_on_push = api_settings.reset_approvals_on_push
        project_settings.can_override_approvals_per_merge_request = (
            not api_settings.disable_overriding_approvers_per_merge_request
        )
        return project_settings

    def get_query(self):
        pass

    def to_dict(self):
        return self.option_dict()


class MergeRequestApprovalSettingExecutor(ChangePropertyExecutor, ProfileMemberMixin):
    order = 57
    name = "mergerequests"
    sections = ["approval_settings"]

    def _apply(self):
        if self.changes:
            approval_settings = self.changes[0]
            if approval_settings.action == "kept":
                return
            manager = ProjectApprovalSettings(self.project)
            approval_settings_to_change = approval_settings.after  # type: ProjectOptions
            manager.reset_approvals_on_push = approval_settings_to_change.reset_approvals_on_push
            manager.merge_requests_author_approval = (
                approval_settings_to_change.enable_self_approval
            )
            manager.enable_committers_approvers = (
                approval_settings_to_change.enable_committers_approvers
            )
            manager.disable_overriding_approvers_per_merge_request = (
                approval_settings_to_change.disable_overriding_approvers_per_merge_request
            )
            manager.save()

    def _update(self, mode: RunMode, members_user, members_group):
        if "approval_settings" not in self.rule or self.rule.approval_settings is None:
            return
        project_settings = ProjectApprovalSettings(self.project)  # type: ignore
        old_settings = ProjectOptions.to_project_approval_settings(project_settings)
        project_approval_settings = self.to_project_approval_settings(
            project_settings, old_settings
        )
        self.changes.append(
            ChangeApprovalSettings(
                "approval_settings",
                old_settings,
                project_approval_settings,
                self.show_diff_only,
            )
        )

    def to_project_approval_settings(self, project_settings, old_settings):
        project_settings = ProjectOptions()
        self.init_options(project_settings, old_settings)
        return project_settings

    def init_options(self, project_settings, old_settings):
        if self.rule.approval_settings:
            project_settings.reset_approvals_on_push = self.rule.approval_settings.get(
                "remove_all_approvals_when_new_commits_are_pushed",
                old_settings.reset_approvals_on_push,
            )
            project_settings.can_override_approvals_per_merge_request = (
                self.rule.approval_settings.get(
                    "can_override_approvals_per_merge_request",
                    old_settings.can_override_approvals_per_merge_request,
                )
            )
            project_settings.enable_self_approval = self.rule.approval_settings.get(
                "enable_self_approval", old_settings.enable_self_approval
            )
            project_settings.enable_committers_approvers = self.rule.approval_settings.get(
                "enable_committers_approvers", old_settings.enable_committers_approvers
            )

        else:
            project_settings.reset_approvals_on_push = old_settings.reset_approvals_on_push
            project_settings.enable_self_approval = old_settings.enable_self_approval
            project_settings.enable_committers_approvers = old_settings.enable_committers_approvers
            project_settings.can_override_approvals_per_merge_request = (
                old_settings.can_override_approvals_per_merge_request
            )

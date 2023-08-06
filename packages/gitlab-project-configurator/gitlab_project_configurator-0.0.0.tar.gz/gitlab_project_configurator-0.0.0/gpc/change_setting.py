# Standard Library
from textwrap import indent
from typing import Dict

# Third Party Libraries
import attr

from boltons.cacheutils import cachedproperty
from colorama import Fore
from colorama import Style
from structlog import get_logger


log = get_logger()

COL_PROP = "{property_name:60}"
COL_SUBPROP = "{sub_prop:60}"
COL_BEFORE = "{before:35}"
COL_AFTER = "{after:35}"
COL_ACTION = "({action})"


class ChangeNamedPropertyMixin:
    REF_PROPERTY = COL_SUBPROP + " " + COL_BEFORE + " => " + COL_AFTER
    REF_PROPERTY_LIST = " " * 61 + COL_BEFORE + "    " + COL_AFTER

    @cachedproperty
    def differences(self):
        before_properties = {prop.name: prop for prop in self.before}
        after_properties = {prop.name: prop for prop in self.after}
        differences = {}
        for name, prop in before_properties.items():
            differences[name] = self._generate_diff(name, prop, after_properties)
        self._added_properties(differences, after_properties)
        return differences

    def _generate_diff(self, before_name, before, after_properties):
        current_diff = self._is_updated(before_name, before, after_properties)
        if not current_diff:
            current_diff = self._is_kept(before_name, before, after_properties)
        if not current_diff:
            current_diff = self._removed(before_name, before, after_properties)
        return current_diff

    def _is_updated(self, before_name, before, after_properties):
        result = {}
        if before_name in after_properties:
            after_prop = after_properties[before_name]
            if before != after_prop:
                result = {
                    "status": "updated",
                    "before": before.to_dict(),
                    "after": after_prop.to_dict(),
                }
        return result

    def _is_kept(self, before_name, before, after_properties):
        after_prop = None
        if self.keep_existing:
            # Existing property but user wants to keep it
            after_prop = before.to_dict()
        elif before_name in after_properties and before == after_properties[before_name]:
            after_prop = after_properties[before_name].to_dict()
        result = (
            {}
            if not after_prop
            else {
                "status": "kept",
                "before": before.to_dict(),
                "after": after_prop,
            }
        )
        return result

    def _added_properties(self, differences: Dict, after_properties: Dict, **kwargs):
        for name, prop in after_properties.items():
            if name not in differences:
                differences[name] = self._added(prop, **kwargs)

    # pylint: disable=unused-argument
    def _added(self, after_prop, **kwargs):
        return {
            "status": "added",
            "before": None,
            "after": after_prop.to_dict(),
        }

    def _removed(self, before_name, before, after_properties):
        return {
            "status": "removed",
            "before": before.to_dict(),
            "after": None,
        }

    # pylint: enable

    @cachedproperty
    def remove(self):
        to_removed = []
        for ref_pattern, difference in self.differences.items():
            if difference.get("status") == "removed":
                to_removed.append(ref_pattern)
        return to_removed

    @cachedproperty
    def update_or_create(self):
        to_update = []
        for ref_pattern, difference in self.differences.items():
            if difference.get("status") in ["updated", "added"]:
                to_update.append(ref_pattern)
        return to_update

    def diff_to_dict(self):
        differences = {}
        if self.has_diff():
            for name, difference in self.differences.items():
                if difference["status"] != "kept":
                    differences[name] = difference
            return {"property_name": self.property_name, "differences": differences}
        return None

    def to_string(self):
        to_str = COL_PROP.format(property_name=f"{self.indent_str}{self.property_name}") + "\n"
        index = 0
        for name, differences in self.differences.items():
            status = differences.get("status")
            before = differences.get("before")
            after = differences.get("after")
            if status in self.status_to_process:
                to_str = self._build_str_by_status(after, before, name, status, to_str)
            if index != len(self.differences) - 1:
                to_str += "\n"
            index += 1
        return to_str

    # flake8: noqa

    def _build_str_by_status(self, after, before, name, status, to_str):
        if status == "removed":
            to_str += self.FMT.format(
                property_name=f"      {self.indent_str}name",
                before=name,
                after="None",
                action=status,
            )
            to_str = self.generate_str_4_sub_properties(before, after, to_str)
        elif status == "updated":
            to_str += self.FMT.format(
                property_name=f"      {self.indent_str}name",
                before=name,
                after=name,
                action=status,
            )
            to_str = self.generate_str_4_sub_properties(before, after, to_str)
        elif status == "kept" and not self.show_diff_only:
            to_str += self.FMT.format(
                property_name=f"      {self.indent_str}name",
                before=name,
                after=name,
                action=status,
            )
            to_str = self.generate_str_4_sub_properties(before, after, to_str)
        elif status == "error" and not self.show_diff_only:
            to_str += self.FMT.format(
                property_name=f"      {self.indent_str}name",
                before=name,
                after=name,
                action=f"{Fore.RED}{status}{Style.RESET_ALL}",
            )
            to_str = self.generate_str_4_sub_properties(before, after, to_str)
        elif status == "added":
            to_str += self.FMT.format(
                property_name=f"      {self.indent_str}name",
                before="None",
                after=name,
                action=status,
            )
            to_str = self.generate_str_4_sub_properties(before, after, to_str)
        return to_str

    # flake8: qa

    def generate_str_4_sub_properties(self, before, after, to_str):
        for sub_prop in self.sub_properties:
            to_str = self.sub_property_to_str(after, before, sub_prop, to_str)
        return to_str

    def sub_property_to_str(self, after, before, sub_prop, to_str):
        before_split = ["None"]
        if before:
            before_split = (
                before.get(sub_prop)
                if isinstance(before.get(sub_prop), list)
                else [before.get(sub_prop)]
            )
        after_split = ["None"]
        if after:
            after_split = (
                after.get(sub_prop)
                if isinstance(after.get(sub_prop), list)
                else [after.get(sub_prop)]
            )
        to_str += (
            self.REF_PROPERTY.format(
                sub_prop=f"      {self.indent_str}{sub_prop}",
                before=str(before_split[0]),
                after=str(after_split[0]),
            )
            + "\n"
        )
        i = 1
        while i < len(before_split) or i < len(after_split):
            before_value = before_split[i] if i < len(before_split) else ""
            after_value = after_split[i] if i < len(after_split) else ""
            to_str += (
                self.REF_PROPERTY_LIST.format(before=str(before_value), after=str(after_value))
                + "\n"
            )
            i += 1
        return to_str


@attr.s
class ChangeSetting:
    FMT = COL_PROP + " " + COL_BEFORE + " => " + COL_AFTER + " " + COL_ACTION + "\n"
    FMT_TITLE = COL_PROP + " " + COL_BEFORE + "    " + COL_AFTER + " " + COL_ACTION + "\n"
    FMT_NO_ACTION = COL_PROP + " " + COL_BEFORE + "    " + COL_AFTER + " \n"
    HORIZONTAL_DOUBLEBAR = "=" * 150
    HORIZONTAL_BAR = "-" * 150

    property_name = attr.ib()
    before = attr.ib()
    after = attr.ib()
    show_diff_only = attr.ib(default=False)
    sub_level = attr.ib(default=0)
    keep_existing = attr.ib(default=False)

    @property
    def indent_str(self):
        return "      " * self.sub_level

    @property
    def title_change(self):
        return self.FMT_TITLE.format(
            property_name=f"{self.indent_str}{self.property_name}",
            before="",
            after="",
            action=self.action,
        )

    def __str__(self):
        before_split = str(self.before).splitlines()
        before_split = before_split if before_split else [""]
        after_split = str(self.after).splitlines()
        after_split = after_split if after_split else [""]
        str_value = self.FMT.format(
            property_name=f"{self.indent_str}{self.property_name}",
            before=before_split[0],
            after=after_split[0],
            action=self.action,
        )
        i = 1
        while i < len(before_split) or i < len(after_split):
            before_value = before_split[i] if i < len(before_split) else ""
            after_value = after_split[i] if i < len(after_split) else ""
            str_value += self.FMT_NO_ACTION.format(
                property_name="",
                before=before_value,
                after=after_value,
                action="",
            )
            i += 1
        return str_value

    def has_diff(self):
        return self.action != "kept"

    def indented(self, prefix="  "):
        return indent(str(self), prefix=prefix)

    @classmethod
    def get_line_header(cls, prefix="  "):
        return indent(
            cls.FMT.format(
                property_name="PROPERTY NAME",
                before="BEFORE",
                after="AFTER",
                action="ACTION",
            ),
            prefix=prefix,
        )

    def to_dict(self):
        return {
            "property_name": self.property_name,
            "differences": {
                "before": self.before,
                "after": self.after,
                "action": self.action,
            },
        }

    def diff_to_dict(self):
        if self.has_diff():
            return self.to_dict()
        return {}

    @cachedproperty
    def action(self):
        if self.after == self.before:
            return "kept"
        if self.after and self.before is None:
            return "added"
        if self.after is None and self.before:
            return "removed"
        return "updated"


class ChangeUnamedPropertyMixin(ChangeNamedPropertyMixin):
    REF_PROPERTY = COL_SUBPROP + " " + COL_BEFORE + " => " + COL_AFTER + " {action}\n"

    def _build_str_by_status(self, after, before, _name, status, to_str):
        if status == "removed":
            for i, sub_prop in enumerate(self.sub_properties):
                to_str += (
                    self.REF_PROPERTY.format(
                        sub_prop=f"      {sub_prop}",
                        before=str(before.get(sub_prop)),
                        after="None",
                        action=f"({status})" if i == 0 else "",
                    )
                    + "\n"
                )
        elif status == "updated":
            for i, sub_prop in enumerate(self.sub_properties):
                to_str += (
                    self.REF_PROPERTY.format(
                        sub_prop=f"      {sub_prop}",
                        before=str(before.get(sub_prop)),
                        after=str(after.get(sub_prop)),
                        action=f"({status})" if i == 0 else "",
                    )
                    + "\n"
                )
        elif status == "kept" and not self.show_diff_only:
            for i, sub_prop in enumerate(self.sub_properties):
                to_str += (
                    self.REF_PROPERTY.format(
                        sub_prop=f"      {sub_prop}",
                        before=str(before.get(sub_prop)),
                        after=str(after.get(sub_prop)),
                        action=f"({status})" if i == 0 else "",
                    )
                    + "\n"
                )
        elif status == "error":
            for i, sub_prop in enumerate(self.sub_properties):
                to_str += (
                    self.REF_PROPERTY.format(
                        sub_prop=f"      {sub_prop}",
                        before=str(before.get(sub_prop)),
                        after=str(after.get(sub_prop)),
                        action=f"({Fore.RED}{status}{Style.RESET_ALL})" if i == 0 else "",
                    )
                    + "\n"
                )
        elif status == "added":
            for i, sub_prop in enumerate(self.sub_properties):
                to_str += (
                    self.REF_PROPERTY.format(
                        sub_prop=f"      {sub_prop}",
                        before="None",
                        after=str(after.get(sub_prop)),
                        action=f"({status})" if i == 0 else "",
                    )
                    + "\n"
                )
        return to_str


class ChangePropertySetting(ChangeSetting, ChangeNamedPropertyMixin):
    def has_diff(self):
        return self.remove or self.update_or_create

    def to_dict(self):
        return {"property_name": self.property_name, "differences": self.differences}

    def __str__(self):
        return self.to_string()

    def diff_to_dict(self):
        return ChangeNamedPropertyMixin.diff_to_dict(self)


class ChangeUnNamedPropertySetting(ChangeSetting, ChangeUnamedPropertyMixin):
    def diff_to_dict(self):
        return ChangeNamedPropertyMixin.diff_to_dict(self)

    def has_diff(self):
        return self.remove or self.update_or_create

    def to_dict(self):
        return {"property_name": self.property_name, "differences": self.differences}

    def __str__(self):
        return self.to_string()


class ChangeSettingSubProperty(ChangeSetting):
    """Change setting with sub properties."""

    REF_PROPERTY = ChangeNamedPropertyMixin.REF_PROPERTY

    def __str__(self):
        change_str = self.title_change

        after = self.after.to_dict()
        before = self.before.to_dict()
        for name, value in after.items():
            change_str += (
                self.REF_PROPERTY.format(
                    sub_prop=f"      {self.indent_str}{name}",
                    before=str(before.get(name)),
                    after=str(value),
                )
                + "\n"
            )

        return change_str

    def to_dict(self):
        return {
            "property_name": self.property_name,
            "differences": {
                "before": self.before.to_dict(),
                "after": self.after.to_dict(),
                "action": self.action,
            },
        }

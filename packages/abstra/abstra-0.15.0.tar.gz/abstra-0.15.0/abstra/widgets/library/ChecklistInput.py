from ..widget_base import Input
from typing import Union, List, Dict


class ChecklistInput(Input):
    type = "checklist-input"

    def __init__(
        self, key: str, label: str, options: Union[List[str], List[Dict]], **kwargs
    ):
        super().__init__(key)
        self.label = label
        self.options = options
        self.initial_value = kwargs.get("initial_value", "")
        self.required = kwargs.get("required", True)
        self.hint = kwargs.get("hint", None)
        self.columns = kwargs.get("columns", 1)
        self.full_width = kwargs.get("full_width", False)
        self.disabled = kwargs.get("disabled", False)

    def json(self, **kwargs):
        return {
            "type": self.type,
            "key": self.key,
            "options": self.options,
            "label": self.label,
            "initialValue": self.initial_value or [],
            "required": self.required,
            "hint": self.hint,
            "columns": self.columns,
            "fullWidth": self.full_width,
            "disabled": self.disabled,
        }

    def convert_answer(self, answer: str) -> str:
        return answer

from abc import ABCMeta
from typing import Optional, Any, Dict, Union, List

from langchain_core.tools import BaseTool
from pydantic import BaseModel


class ResilientBaseTool(BaseTool, metaclass=ABCMeta):
    """
    This is a base tool that provides resilience to the tool execution.

    """

    def _parse_input(
        self, tool_input: Union[str, Dict[str, Any]], tool_call_id: Optional[str]
    ) -> Union[str, dict[str, Any]]:
        """
        This function parses the input for the tool.

        Sometimes the LLMs can mess up camelCase vs snake_case parameter names
        so we need to handle both cases

        :param tool_input: input for the tool
        :param tool_call_id: id of the tool call
        :return: input for the tool
        """
        #
        if isinstance(tool_input, dict):

            def camel_to_snake(name: str) -> str:
                return "".join(
                    [f"_{c.lower()}" if c.isupper() else c for c in name]
                ).lstrip("_")

            if not self.args_schema:
                return tool_input

            # find keys that are not present in self.args_schema
            # and convert them to snake_case
            assert self.args_schema is not None
            assert isinstance(self.args_schema, BaseModel)
            input_fields: List[str] = [c for c in self.args_schema.model_fields.keys()]
            tool_input = {
                (camel_to_snake(key) if key not in input_fields else key): value
                for key, value in tool_input.items()
            }
        return super()._parse_input(tool_input, tool_call_id)

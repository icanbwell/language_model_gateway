import logging
import os
from typing import Type

from langchain_experimental.utilities import PythonREPL
from pydantic import BaseModel, Field

from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool

logger = logging.getLogger(__file__)


class PythonReplToolInput(BaseModel):
    query: str = Field(description="A valid Python command to execute")


class PythonReplTool(ResilientBaseTool):
    name: str = "python_repl"
    description: str = "A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`."
    args_schema: Type[BaseModel] = PythonReplToolInput

    async def _arun(self, query: str) -> str:
        """Async implementation of the tool (in this case, just calls _run)"""
        try:
            python_repl = PythonREPL()
            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(f"Running Python Repl with query: {query}")
            result: str = python_repl.run(command=query)
            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(f"Python Repl result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error running Python Repl: {e}")
            logger.exception(e, stack_info=True)
            return f"Error running Python Repl: {e}"

    def _run(self, query: str) -> str:
        try:
            python_repl = PythonREPL()
            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(f"Running Python Repl with query: {query}")
            result: str = python_repl.run(command=query)
            if os.environ.get("LOG_INPUT_AND_OUTPUT", "0") == "1":
                logger.info(f"Python Repl result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error running Python Repl: {e}")
            logger.exception(e, stack_info=True)
            return f"Error running Python Repl: {e}"

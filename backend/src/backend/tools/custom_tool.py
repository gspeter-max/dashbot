from fastapi import FastAPI
from crewai.tools import BaseTool
import typing 
from pydantic import BaseModel, Field


class getCurrentApiCallMetaDataInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class getCurrentApiCallMetaData(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: typing.Type[BaseModel] = getCurrentApiCallMetaDataInput

    def _run(self, argument: str) -> str:
        
        return "this is an example of a tool output, ignore it and move along."

from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field


class ToolOutput(BaseModel):
    tool_call_id: Optional[str] = Field(
        None,
        description="The ID of the tool call in the `required_action` "
        "object within the run object the output is being submitted for.",
    )
    output: Optional[str] = Field(
        None,
        description="The output of the tool call to be submitted to continue the run.",
    )


class SubmitToolOutputsRunRequest(BaseModel):
    tool_outputs: List[ToolOutput] = Field(
        ..., description="A list of tools for which the outputs are being submitted."
    )
    stream: Optional[bool] = False

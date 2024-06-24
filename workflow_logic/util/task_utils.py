from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Literal
from typing_extensions import Annotated, Literal, TypedDict

class MessageDict(TypedDict):
    """A dictionary representing a message in a chat conversation."""
    role: Annotated[Literal["user", "assistant", "system", "tool"], Field(default="user", description="Role of the message")]
    content: Annotated[str, Field(description="Content of the message")]
    generated_by: Annotated[Literal["user", "llm", "tool"], Field(default="user", description="Who created the message")]
    step: Annotated[Optional[str], Field(default="", description="Process that is creating this message, usually the task_name or tool_name")]
    assistant_name: Annotated[Optional[str], Field(default="", description="Name of the assistant")]
    context: Annotated[Optional[Dict[str, Any]], Field(default=None, description="Context of the message")]
    type: Annotated[Optional[str], Field(default="text", description="Type of the message")]
    request_type: Annotated[Optional[str], Field(default=None, description="Request type of the message, if any. Can be 'approval', 'confirmation', etc.")]
    createdAt: Annotated[Optional[str], Field(default=None, description="Timestamp of the message")]
    updatedAt: Annotated[Optional[str], Field(default=None, description="Timestamp of the message")]
    created_by: Annotated[Optional[dict], Field(default=None, description="User id who created the message")]
    updated_by: Annotated[Optional[dict], Field(default=None, description="User id who updated the message")]

    def __str__(self):
        if self.type == "text":
            return f"{self.role}{f' ({self.assistant_name})' if self.assistant_name else ''}: {self.content}"
        elif self.type == "tool":
            return f"{self.role}: {self.content}{' (' + str(self.step) + ')' if self.step else ''}"

class SearchResult(TypedDict):
    """A dictionary representing a search result."""
    title: Annotated[str, Field(description="Title of the search result")]
    url: Annotated[str, Field("", description="URL of the search result")]
    content: Annotated[str, Field("", description="Content of the search result")]
    metadata: Annotated[Optional[Dict[str, Any]], Field({}, description="Metadata of the search result")]

class OutputInterface(BaseModel, ABC):
    content: List[Any] = Field([], description="The content of the output.")
    @abstractmethod
    def __str__(self) -> str:
        """Returns a string representation of the output."""
        pass

class StringOutput(OutputInterface):
    content: List[str] = Field([], description="The content of the output.")

    def __str__(self) -> str:
        return "\n".join(self.content)

class LLMChatOutput(OutputInterface):
    content: List[MessageDict] = Field([], description="List of messages in the chat conversation")

    def __str__(self) -> str:
        return "\n".join(
            [f"{message['role']}: " + (f"{message['assistant_name']}\n" if message.get('assistant_name') else "\n") + message['content']
             for message in self.content]
        )

class SearchOutput(OutputInterface):
    content: List[SearchResult] = Field([], description="List of search results")

    def __str__(self) -> str:
        return "\n".join(
            [f"Title: {result['title']}, URL: {result['url']}, Content: {result['content']}"
             for result in self.content]
        )
    
class ParameterDefinition(BaseModel):
    type: Annotated[str, Field(description="Type of the parameter")]
    description: Annotated[str, Field(description="Description of the parameter")]
    default: Annotated[Optional[Any], Field(description="Default value of the parameter")]

class FunctionParameters(BaseModel):
    """Parameters of a function as defined by the OpenAI API"""
    type: Annotated[Literal["object"], Field(description="Type of the parameters")]
    properties: Annotated[Dict[str, ParameterDefinition], Field(description="Dict of parameters name to their type, description, and default value")]
    required: Annotated[List[str], Field(description="Required parameters")]

class FunctionConfig(BaseModel):
    """A function as defined by the OpenAI API"""
    name: Annotated[str, Field(description="Name of the function")]
    description: Annotated[str, Field(description="Description of the function")]
    parameters: Annotated[FunctionParameters, Field(description="Parameters of the function")]

class ToolFunction(BaseModel):
    """A function under tool as defined by the OpenAI API."""
    type: Annotated[Literal["function"], Field(default="function", description="Type of the tool function")]
    function: Annotated[FunctionConfig, Field(description="Function under tool")]

class TaskResponse(BaseModel):
    task_name: str = Field(..., description="The name of the task")
    task_description: str = Field(..., description="A detailed description of the task")
    status: Literal["pending", "complete", "failed"] = Field(..., description="The current status of the task")
    result_code: int = Field(..., description="The result code indicating the success or failure of the task")
    task_outputs: Optional[OutputInterface] = Field(None, description="The output generated by the task")
    result_diagnostic: Optional[str] = Field(None, description="Diagnostic information for the task, if any")
    task_inputs: Optional[Dict[str, Any]] = Field(None, description="The inputs provided to the task")
    usage_metrics: Optional[Dict[str, Any]] = Field(None, description="Usage metrics for the task, like generated tokens, time taken, and cost.")
    execution_history: Optional[List[Dict[str, Any]]] = Field(None, description="Execution history of the task")

    def __str__(self) -> str:
        return f"{self.task_name}: {self.task_description}\nTask Output:\n{str(self.task_outputs)}"

class WorkflowOutput(OutputInterface):
    content: List[TaskResponse] = Field([], description="The task responses performed by the workflow.")

    def __str__(self) -> str:
        return "\n".join([f"{task.task_name}: {task.task_description}\nTask Output:{str(task.task_outputs)}" for task in self.content])

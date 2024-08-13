from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal, Dict, Any, List, Union
from typing_extensions import Optional, Literal
from workflow_logic.core.parameters import ToolCall
from workflow_logic.util.logging_config import LOGGER

class OutputInterface(BaseModel):
    content: List[Any] = Field([], description="The content of the output.")

    @property
    def output_type(self) -> str:
        return self.__class__.__name__
   
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data['output_type'] = self.output_type
        
        # Propagate args and kwargs to content if they are BaseModel objects
        if isinstance(self.content, list):
            data['content'] = [
                item.model_dump(*args, **kwargs) if isinstance(item, BaseModel) else item
                for item in self.content
            ]
        elif isinstance(self.content, BaseModel):
            data['content'] = self.content.model_dump(*args, **kwargs)
        
        return data
   
    def __str__(self) -> str:
        return str(self.content)

class TaskResponse(BaseModel):
    id: Optional[str] = Field(default=None, description="The id of the task response", alias="_id")
    task_id: Optional[str] = Field(None, description="The id of the task")
    task_name: str = Field(..., description="The name of the task")
    task_description: str = Field(..., description="A detailed description of the task")
    status: Literal["pending", "complete", "failed"] = Field(..., description="The current status of the task")
    result_code: int = Field(..., description="The result code indicating the success or failure of the task")
    result_diagnostic: Optional[str] = Field(None, description="Diagnostic information for the task, if any")
    task_inputs: Optional[Dict[str, Any]] = Field(None, description="The inputs provided to the task")
    usage_metrics: Optional[Dict[str, Any]] = Field(None, description="Usage metrics for the task, like generated tokens, time taken, and cost.")
    execution_history: Optional[List[Dict[str, Any]]] = Field(None, description="Execution history of the task")
    task_outputs: Optional[str] = Field(None, description="The output generated by the task")
    task_content: Optional[OutputInterface] = Field(None, description="An outputinterface with the content of the task output")

    def __str__(self) -> str:
        return f"{self.task_name}: {self.task_description}\nTask Output:\n{self.task_outputs}"
    
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if self.task_content and isinstance(self.task_content, OutputInterface):
            data['task_content'] = self.task_content.model_dump(*args, **kwargs)
        return data
    
class DatabaseTaskResponse(TaskResponse):
    task_content: Optional[Dict[str, Any]] = Field(None, description="The content of the task output, represents the model_dump of the OutputInterface used")
    
    def retrieve_task_outputs(self) -> 'OutputInterface':
        if not self.task_content:
            return StringOutput(content=[self.task_outputs])
        output_type = self.task_content.get("output_type")
        if output_type == "StringOutput":
            return StringOutput(**self.task_content)
        elif output_type == "LLMChatOutput":
            return LLMChatOutput(**self.task_content)
        elif output_type == "SearchOutput":
            return SearchOutput(**self.task_content)
        elif output_type == "WorkflowOutput":
            return WorkflowOutput(**self.task_content)
        else:
            return StringOutput(content=[self.task_outputs])
    
    def retrieve_task_response(self) -> TaskResponse:
        return TaskResponse(
            task_id=self.task_id,
            task_name=self.task_name,
            task_description=self.task_description,
            status=self.status,
            result_code=self.result_code,
            task_outputs=self.retrieve_task_outputs(),
            result_diagnostic=self.result_diagnostic,
            task_inputs=self.task_inputs,
            usage_metrics=self.usage_metrics,
            execution_history=self.execution_history
        )
    
    @classmethod
    def model_validate(cls, obj):
        if isinstance(obj, dict) and 'task_content' in obj and isinstance(obj['task_content'], OutputInterface):
            obj = obj.copy()
            obj['task_content'] = obj['task_content'].model_dump()
        return super().model_validate(obj) 
    
class MessageType(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    FILE = 'file'
    TASK_RESPONSE = 'TaskResponse'

class MessageDict(BaseModel):
    id: Optional[str] = Field(default="", description="The id of the message", alias="_id")
    role: Literal["user", "assistant", "system", "tool"] = Field(default="user", description="Role of the message")
    content: Optional[str] = Field(default=None, description="Content of the message")
    generated_by: Literal["user", "llm", "tool"] = Field(default="user", description="Who created the message")
    step: Optional[str] = Field(default="", description="Process that is creating this message, usually the task_name or tool_name")
    assistant_name: Optional[str] = Field(default="", description="Name of the assistant")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Context of the message")
    type: MessageType = Field(default="text", description="Type of the message")
    tool_calls: Optional[List[ToolCall]] = Field(default=None, description="List of tool calls in the message")
    tool_call_id: Optional[str] = Field(None, description="The id of the tool call that generated this task response")
    function_call: Optional[Dict[str, Any]] = Field(default=None, description="Function call in the message")
    request_type: Optional[str] = Field(default=None, description="Request type of the message, if any. Can be 'approval', 'confirmation', etc.")
    task_responses: Optional[List[TaskResponse]] = Field(default_factory=list, description="List of associated task responses")
    creation_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata about the creation of the message, like cost, tokens, end reason, etc.")
    createdAt: Optional[str] = Field(default=None, description="Timestamp of the message")
    updatedAt: Optional[str] = Field(default=None, description="Timestamp of the message")
    created_by: Optional[Union[str, dict]] = Field(default=None, description="User id who created the message")
    updated_by: Optional[Union[str, dict]] = Field(default=None, description="User id who updated the message")

    def __str__(self) -> str:
        role = self.role if self.role else ''
        content = self.content if self.content else ''
        msg_type = self.type if self.type else ''
        assistant_name = self.assistant_name if self.assistant_name else ''
        step = self.step if self.step else ''
        if msg_type == "text":
            return f"{role}{f' ({assistant_name})' if assistant_name else ''}: {content}"
        elif msg_type == "tool":
            return f"Tool result: {content}{f' ({step})' if step else ''}"
        return f"{role}: {content}"
    
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if self.tool_calls:
            data['tool_calls'] = [tool_call.model_dump(*args, **kwargs) for tool_call in self.tool_calls]
        if self.task_responses:
            data['task_responses'] = [task_response.model_dump(*args, **kwargs) for task_response in self.task_responses]
        return data

class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode='before')
    def sanitize_metadata(cls, values):
        sanitized_metadata = {}
        metadata = values.get('metadata', {})
        for key, val in metadata.items():
            try:
                if isinstance(val, datetime):
                    sanitized_metadata[key] = val.isoformat()
                else:
                    sanitized_metadata[key] = str(val)
            except Exception as e:
                LOGGER.error(f"Error serializing value for key {key}: {val}, Exception: {e}")
                sanitized_metadata[key] = "Unserializable value"
        values['metadata'] = sanitized_metadata
        return values

class StringOutput(OutputInterface):
    content: List[str] = Field([], description="The content of the output.")

    def __str__(self) -> str:
        return "\n".join(self.content)

class LLMChatOutput(OutputInterface):
    content: List[MessageDict] = Field([], description="List of messages in the chat conversation")

    def __str__(self) -> str:
        return "\n".join(
            [f"{message.role}: " + (f"{message.assistant_name}\n" if message.assistant_name else "\n") + message.content
             for message in self.content]
        )

class SearchOutput(OutputInterface):
    content: List[SearchResult] = Field([], description="List of search results")

    def __str__(self) -> str:
        return "\n".join(
            [f"Title: {result.title} \nURL: {result.url} \n Content: {result.content}\n"
             for result in self.content]
        )

class WorkflowOutput(OutputInterface):
    content: List[TaskResponse] = Field([], description="The task responses performed by the workflow.")

    def __str__(self) -> str:
        return "\n".join([f"{task.task_name}: {task.task_description}\nTask Output:{str(task.task_outputs)}" for task in self.content])
    
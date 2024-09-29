from __future__ import annotations
from typing import Optional, Literal, Dict, Any, List, TYPE_CHECKING
from pydantic import Field, ConfigDict, field_validator
from workflow_logic.core.data_structures.base_models import BaseDataStructure, ContentType, FileType
from workflow_logic.core.data_structures.central_types import ToolCallType, ReferencesType

if TYPE_CHECKING:
    from workflow_logic.core.data_structures.parameters import ToolCall
    from workflow_logic.core.data_structures.references import References

class MessageDict(BaseDataStructure):
    role: Literal["user", "assistant", "system", "tool"] = Field(default="user", description="Role of the message")
    content: Optional[str] = Field(default=None, description="Content of the message")
    generated_by: Literal["user", "llm", "tool"] = Field(default="user", description="Who created the message")
    step: Optional[str] = Field(default="", description="Process that is creating this message, usually the task_name or tool_name")
    assistant_name: Optional[str] = Field(default="", description="Name of the assistant")
    type: ContentType = Field(default=ContentType.TEXT, description="Type of the message")
    tool_calls: Optional[List[ToolCallType]] = Field(default=None, description="List of tool calls in the message")
    tool_call_id: Optional[str] = Field(None, description="The id of the tool call that generated this task response")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Context of the message")
    function_call: Optional[Dict[str, Any]] = Field(default=None, description="Function call in the message")
    request_type: Optional[str] = Field(default=None, description="Request type of the message, if any. Can be 'approval', 'confirmation', etc.")
    references: Optional[ReferencesType] = Field(default_factory=lambda: References(), description="References associated with this message")
    creation_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata about the creation of the message, like cost, tokens, end reason, etc.")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('tool_calls')
    def validate_tool_calls(cls, v):
        from workflow_logic.core.data_structures.parameters import ToolCall
        if v is None:
            return v
        
        validated_tool_calls = []
        for item in v:
            if isinstance(item, ToolCall):
                validated_tool_calls.append(item)
            elif isinstance(item, dict):
                validated_tool_calls.append(ToolCall(**item))
            else:
                raise ValueError(f"Invalid tool call type: {type(item)}")
        
        return validated_tool_calls
    
    def __str__(self) -> str:
        role = self.role if self.role else ''
        content = self.content if self.content else ''
        msg_type = self.type if self.type else ''
        assistant_name = self.assistant_name if self.assistant_name else ''
        step = self.step if self.step else ''
        
        message_parts = []

        # Base content
        if msg_type in [FileType.IMAGE, FileType.AUDIO, FileType.VIDEO, FileType.FILE]:
            message_parts.append(f"{role}: {content}")
            file_refs = self.references.get_references('files')
            if file_refs:
                message_parts.extend([str(file_ref) for file_ref in file_refs])
        elif msg_type == ContentType.TEXT:
            message_parts.append(f"{role}{f' ({assistant_name})' if assistant_name else ''}: {content}")
            if self.references:
                message_parts.append(f"References: {self.references.summary()}")
        elif msg_type == ContentType.TASK_RESPONSE:
            generated_by = f"(generated by {self.generated_by})" if self.generated_by in ['user', 'llm'] else ""
            message_parts.append(f"{role} - Step: {step} {generated_by}: {content}")
            task_responses = self.references.get_references('task_responses')
            if task_responses:
                message_parts.extend([str(task_response) for task_response in task_responses])
        elif msg_type == ContentType.MULTIPLE:
            message_parts.append(f"{role}{f' ({assistant_name})' if assistant_name else ''}: {content}")
            message_parts.append(self.references.detailed_summary())
        else:
            message_parts.append(f"{role}: {content}")

        return "\n".join(message_parts)
   
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if self.tool_calls:
            data['tool_calls'] = [tool_call.model_dump(*args, **kwargs) for tool_call in self.tool_calls]
        if self.references:
            data['references'] = self.references.model_dump(*args, **kwargs)
        return data
   
    def add_reference(self, reference: Any):
        """
        Add a reference to the message. This can be any type supported by the References class.
        """
        self.references.add_reference(reference)

    def get_references_by_type(self, ref_type: str) -> List[Any]:
        """
        Get references by type. This returns references of the specified type.
        """
        return self.references.get_references(ref_type)
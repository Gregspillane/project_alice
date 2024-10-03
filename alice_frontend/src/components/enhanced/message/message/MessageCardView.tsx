import React from 'react';
import {
    Typography,
    Box,
    Chip,
} from '@mui/material';
import { Person, AccessTime, AttachFile, TextSnippet, Engineering, PersonPin } from '@mui/icons-material';
import { MessageComponentProps } from '../../../../types/MessageTypes';
import CommonCardView from '../../common/enhanced_component/CardView';
import { CollectionElementString } from '../../../../types/CollectionTypes';
import { References } from '../../../../types/ReferenceTypes';
import useStyles from '../MessageStyles';
import CustomMarkdown from '../../common/markdown/CustomMarkdown';
import { useCardDialog } from '../../../../contexts/CardDialogContext';
import { FileReference } from '../../../../types/FileTypes';

interface ReferenceChipProps {
    reference: any;
    type: CollectionElementString | 'string_output';
    view: () => void;
}

const ReferenceChip: React.FC<ReferenceChipProps> = ({ reference, type, view }) => {
    let label = '';
    switch (type) {
        case 'Message':
            label = `Message: ${reference.content.substring(0, 20)}...`;
            break;
        case 'File':
            label = `File: ${reference.filename}`;
            break;
        case 'TaskResponse':
            label = `Task: ${reference.task_name}`;
            break;
        case 'URLReference':
            label = `URL: ${reference.url}`;
            break;
        case 'string_output':
            label = `Output: ${reference.substring(0, 20)}...`;
            break;
    }

    return (
        <Chip
            label={label}
            onClick={view}
            variant="outlined"
        />
    );
};

const hasAnyReferences = (references: References | undefined): boolean => {
    if (!references) return false;
    return !!(
        references.messages?.length ||
        references.files?.length ||
        references.task_responses?.length ||
        references.search_results?.length ||
        references.string_outputs?.length
    );
};

const MessageCardView: React.FC<MessageComponentProps> = ({
    item,
}) => {
    const classes = useStyles();
    const { selectCardItem } = useCardDialog();
    if (!item) {
        return <Typography>No message data available.</Typography>;
    }

    const renderReferences = () => {
        if (!item.references || !hasAnyReferences(item.references)) return 'No references';
        return (
            <Box>
                <Typography variant="subtitle2">References:</Typography>
                <Box display="flex" flexWrap="wrap" gap={1}>
                    {item.references.messages?.map((msg, index) => (
                        <ReferenceChip 
                            key={`msg-${index}`} 
                            reference={msg} 
                            type="Message" 
                            view={() => selectCardItem && selectCardItem('Message', msg._id!, msg)}
                        />
                    ))}
                    {item.references.files?.map((file, index) => (
                        <ReferenceChip 
                            key={`file-${index}`} 
                            reference={file} 
                            type="File" 
                            view={() => selectCardItem && selectCardItem('File', file._id!, file as FileReference)}
                        />
                    ))}
                    {item.references.task_responses?.map((task, index) => (
                        <ReferenceChip 
                            key={`task-${index}`} 
                            reference={task} 
                            type="TaskResponse" 
                            view={() => selectCardItem && selectCardItem('Task', task._id!, task)}
                        />
                    ))}
                    {item.references.search_results?.map((url, index) => (
                        <ReferenceChip 
                            key={`url-${index}`} 
                            reference={url} 
                            type="URLReference" 
                            view={() => selectCardItem && selectCardItem('URLReference', url._id!, url)}
                        />
                    ))}
                    {item.references.string_outputs?.map((str, index) => (
                        <ReferenceChip 
                            key={`str-${index}`} 
                            reference={str} 
                            type="string_output" 
                            view={() => {}} // No action for string outputs
                        />
                    ))}
                </Box>
            </Box>
        );
    };
    
    const getMessageClass = () => {
        if (item.generated_by === 'tool') return classes.toolMessage;
        switch (item.role) {
            case 'user':
                return classes.userMessage;
            case 'assistant':
            default:
                return classes.assistantMessage;
        }
    };

    const listItems = [
        {
            icon: <TextSnippet />,
            primary_text: "Content",
            secondary_text: <CustomMarkdown className={`${classes.messageSmall} ${getMessageClass()}`}>{item.content}</CustomMarkdown>
        },
        {
            icon: <Person />,
            primary_text: "Role",
            secondary_text: item.role
        },
        {
            icon: <PersonPin />,
            primary_text: "Assistant",
            secondary_text: item.assistant_name ?? "N/A"
        },
        {
            icon: <Engineering />,
            primary_text: "Generated By",
            secondary_text: item.generated_by
        },
        {
            icon: <AttachFile />,
            primary_text: "References",
            secondary_text: renderReferences()
        },
        {
            icon: <Person />,
            primary_text: "Metadata",
            secondary_text: JSON.stringify(item.creation_metadata ?? {}, null, 2),
        },
        {
            icon: <AccessTime />,
            primary_text: "Created At",
            secondary_text: new Date(item.createdAt || '').toLocaleString()
        },
    ];

    return (
        <CommonCardView
            elementType='Message'
            title={item.role}
            subtitle={`Type: ${item.type}`}
            id={item._id}
            listItems={listItems}
            item={item}
            itemType='messages'
        />
    );
};

export default MessageCardView;
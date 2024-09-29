import React from 'react';
import {
    Typography,
    ListItemButton,
    List,
    ListItem,
    ListItemText,
} from '@mui/material';
import { Person, AccessTime, Source, AttachFile, Assignment } from '@mui/icons-material';
import { MessageComponentProps } from '../../../../types/MessageTypes';
import CommonCardView from '../../common/enhanced_component/CardView';

const MessageCardView: React.FC<MessageComponentProps> = ({
    item,
    handleFileClick,
    handleTaskResultClick,
}) => {
    if (!item) {
        return <Typography>No message data available.</Typography>;
    }

    const listItems = [
        {
            icon: <Person />,
            primary_text: "Role",
            secondary_text: item.role
        },
        {
            icon: <AccessTime />,
            primary_text: "Created At",
            secondary_text: new Date(item.createdAt || '').toLocaleString()
        },
        {
            icon: <Source />,
            primary_text: "Generated By",
            secondary_text: item.generated_by
        },
        {
            icon: <AttachFile />,
            primary_text: "File References",
            secondary_text: (
                <List disablePadding>
                    {item.references?.map((file, index) => (
                        <ListItem key={index} disablePadding>
                            <ListItemButton onClick={() => handleFileClick && (file._id ? handleFileClick(file._id) : handleFileClick('', file))}>
                                <ListItemText primary={file.filename} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            )
        },
        {
            icon: <Assignment />,
            primary_text: "Task Responses",
            secondary_text: (
                <List disablePadding>
                    {item.task_responses?.map((taskResponse, index) => (
                        <ListItem key={index} disablePadding>
                            <ListItemButton onClick={() => handleTaskResultClick && (taskResponse._id ? handleTaskResultClick(taskResponse._id) : handleTaskResultClick('', taskResponse))}>
                                <ListItemText primary={taskResponse.task_name} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            )
        }
    ];

    return (
        <CommonCardView
            elementType='Message'
            title={`${item.role} Message`}
            subtitle={item.content}
            id={item._id}
            listItems={listItems}
        />
    );
};

export default MessageCardView;
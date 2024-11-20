import React, { useState } from 'react';
import { Box, Button, IconButton, useMediaQuery } from '@mui/material';
import { Add } from '@mui/icons-material';

import CreatePostWindow from './CreatePostWindow';


function CreatePostButton() {
    // Whether the screen is small (so certain elements can be hidden):
    const smallScreen = useMediaQuery('(max-width: 800px)');

    // Whether the post creation window is open:
    const [windowOpen, setWindowOpen] = useState(false);
    const toggleWindow = () => setWindowOpen(!windowOpen);

    return (
        <Box>
            {/* Conditionally showing an icon button or normal button depending on screen size */}
            {smallScreen ? (
                <IconButton 
                    onClick={toggleWindow} 
                    sx={{ 
                        margin: 1, 
                        color: 'primary.main', 
                        border: '2px solid', 
                        borderColor: 'primary.main' 
                    }}
                >
                    <Add />
                </IconButton>
            ) : (
                <Button 
                    variant='outlined'
                    onClick={toggleWindow}  
                    startIcon={<Add />} 
                    sx={{ fontWeight: 'bold', border: 2 }}
                >
                    Create
                </Button>
            )}
            <CreatePostWindow variant='createPost' isOpen={windowOpen} onClose={toggleWindow} />
        </Box>
    );
}

export default CreatePostButton;
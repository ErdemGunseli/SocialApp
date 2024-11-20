import { useEffect } from 'react';
import { Box, AppBar, Toolbar, Typography, useMediaQuery } from '@mui/material';
import { toast } from 'react-toastify';        


import { useUser } from '../../context/UserContext';
import AvatarMenu from './AvatarMenu';
import SearchPosts from '../Post/SearchPosts';
import CreatePostButton from '../Post/CreatePostButton';
import LoginButton from '../User/LoginButton';


function Header() {
    // Whether the screen is small (so certain elements can be hidden):
    const smallScreen = useMediaQuery('(max-width: 800px)');

    const { user } = useUser();

    // If the user is logged in, displaying a message:
    useEffect(() => {
        if (user?.name) {
            toast.success(`Welcome, ${user.name}`, 
                { 
                    toastId: 'Welcome',
                    position: 'bottom-left'
                })
        }
    }, [user])


    return (
        <AppBar position="sticky">
            {/* 'Toolbar' provides proper spacing & alignment for AppBar */}
            <Toolbar sx={{ display: 'flex', justifyContent: 'space-between'}}>
                <Box 
                    onClick={() => window.location.reload()}
                    sx={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}
                >
                    <Box component='img' src="/icon.png" alt="Social App" sx={{ mr: 2, height: 50 }} />
                    {/* Only showing this element if the screen is not very small */}
                    {!smallScreen && <Typography variant="title">Social App</Typography>}
                </Box>

                <Box sx={{ flex: 1, display: 'flex', justifyContent: 'center', px: 1 }}>
                    <SearchPosts />
                </Box>
                
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                {user && <CreatePostButton />}


                    {!user && <LoginButton />}
                    
                    <AvatarMenu />             
                </Box>
            </Toolbar>
        </AppBar>
    );
}

export default Header;

import { useState } from 'react';
import { Box, Avatar, Menu, MenuItem, Typography } from '@mui/material';
import { Person, Logout } from '@mui/icons-material';

import { useUser } from '../../context/UserContext';
import { logout } from '../../api/auth';
import AccountFormWindow from '../User/AccountFormWindow';


function AvatarMenu() {
    const { user, clearUser } = useUser();

    // The element that the menu is attached to:
    const [anchorEl, setAnchorEl] = useState(null);

    const [accountFormOpen, setAccountFormOpen] = useState(false);

    const handleAvatarClick = (event) => {
        if (user) {
            setAnchorEl(event.currentTarget);
        }
    };

    const handleClose = () => {
        // When the user clicks outside the menu, setting the anchor to null:
        setAnchorEl(null);
    };

    const handleLogout = () => {
        handleClose();
        clearUser();
        logout();
    };


    return (
        <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
            <Avatar 
                alt='User' 
                src={`http://localhost:8000/${user?.profile_image?.url}`}
                onClick={handleAvatarClick} 
                sx={{ cursor: 'pointer', width: 55, height: 55 }} 
            />

            <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                sx={{ mt: 2 }}
                slotProps={{ paper: { sx: { borderRadius: 3, p: 1 } } }}
            >
                {user && (
                    <Typography variant='subtitle' sx={{ m: 2 }}>
                        {`Hi ${user.name}`}
                    </Typography>
                )}
                <MenuItem onClick={() => {
                    setAccountFormOpen(true);
                    handleClose();
                }}>
                    <Person sx={{ mr: 1 }} />Account
                </MenuItem>
                
                <MenuItem onClick={handleLogout}>
                    <Logout sx={{ mr: 1 }} />Log Out
                </MenuItem>
            </Menu>

            <AccountFormWindow isOpen={accountFormOpen} onClose={() => setAccountFormOpen(false)} />

        </Box>
    );
}

export default AvatarMenu;
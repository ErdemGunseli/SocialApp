import React, { useState } from 'react';
import { Button, Box } from '@mui/material';

import { useUser } from '../../context/UserContext';
import { logout } from '../../api/auth';
import LoginWindow from './LoginWindow';


function LoginButton() {
  const { user } = useUser();

  // Whether the login window is open:
  const [windowOpen, setWindowOpen] = useState(false);
  const toggleWindow = () => setWindowOpen(!windowOpen);

  
  const handleLoginClick = () => {
    if (user) {
      logout();
    } else {
      toggleWindow()
    }
  };  

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', mx: 2}}>

      <Button onClick={handleLoginClick} variant='contained'>
        {user ? 'Log Out' : 'Log In'}
      </Button>

      <LoginWindow isOpen={windowOpen} onClose={toggleWindow} />
    </Box>
  );
}

export default LoginButton;


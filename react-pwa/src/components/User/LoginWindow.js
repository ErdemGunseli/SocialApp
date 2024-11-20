import React, { useState, useEffect } from 'react';
import { Button, Box, TextField, Typography } from '@mui/material';

import { useUser } from '../../context/UserContext';
import { login } from '../../api/auth';
import { createUser } from '../../api/user';
import FormWindow from '../common/FormWindow';

function LoginWindow({ isOpen, onClose }) {    

    const { refreshUser } = useUser();

    // Whether it is a login or signup window:
    const [isSignUp, setIsSignUp] = useState(false);

    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // Clearing the form details if it is closed:
    useEffect(() => {
      if (!isOpen) {
        setName('');
        setEmail('');
        setPassword('');
        setIsSignUp(false);
      }
    }, [isOpen]);

    const handleSubmit = async (e) => {
        // Preventing default submit behavior which is to refresh the page:
        e.preventDefault(); 

        let result;

        if (isSignUp) {
          result = await createUser(name, email, password);

        } else {
          result = await login(email, password);
        }
        if (result) {
          onClose();
          await refreshUser();
        }
    }; 

    return (
      <FormWindow 
        isOpen={isOpen} 
        onClose={onClose} 
        onSubmit={handleSubmit} 
        title={isSignUp ? 'Sign Up' : 'Log In'} 
        buttonText='Continue'
      >

        {isSignUp && (
          <TextField
            label='Name'
            type='text'
            variant='outlined'
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
            required
          />
        )}  

        <TextField
          label='Email'
          type='email'
          variant='outlined'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          required
        />

        <TextField
          label='Password'
          type='password'
          variant='outlined'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
          required
        />

        <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', mt: 1 }}>
          <Typography variant='normalText' >
            {isSignUp ? 'Already a user?' : 'New to Social App?'}
          </Typography>

          <Button variant="text" onClick={() => setIsSignUp(!isSignUp)} >
            {isSignUp ? 'Log In' : 'Sign Up'}
          </Button>
        </Box>

      </FormWindow>
    );
}

export default LoginWindow;
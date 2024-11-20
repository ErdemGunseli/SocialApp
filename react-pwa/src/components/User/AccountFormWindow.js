import React, { useEffect, useState } from 'react';
import { Box, Button, TextField } from '@mui/material';

import { useUser } from '../../context/UserContext';
import { usePosts } from '../../context/PostContext';
import { login } from '../../api/auth';
import { updateUser, createProfileImage, deleteProfileImage } from '../../api/user';
import FormWindow from '../common/FormWindow';
import ImageUpload from '../common/ImageUpload';


function AccountFormWindow({ isOpen, onClose }){
    const { user, refreshUser } = useUser();
    const { refreshPosts } = usePosts();

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [profileImage, setProfileImage] = useState(null);

    const [editing, setEditing] = useState(false);


    useEffect(() => {
        if (!isOpen) {
            setEditing(false);
        }
    }, [isOpen]);


       // Add this useEffect to update state when user changes
    useEffect(() => {
        setUsername(user?.name || '');
        setEmail(user?.email || '');
        setPassword('')
        setProfileImage({url: `http://localhost:8000/${user?.profile_image?.url}`, file: null});
    }, [user]);

    
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Using value from context since email field may be changed:
        const response = await login(user.email, password);

        if (response.access_token) {
            await updateUser(username, email);

            if (profileImage.file) {
                if (user?.profile_image?.url) {
                    await deleteProfileImage();
                }
                await createProfileImage(profileImage.file);
            }

            await refreshUser();
            // Refreshing posts so user info within posts is updated:
            await refreshPosts();
            setPassword('');
            setEditing(false);
        }
    }

    
    return (
        <FormWindow 
            isOpen={isOpen} 
            onClose={onClose} 
            onSubmit={handleSubmit} 
            title='Account Details' 
            buttonSx={{ display: 'none' }}
            sx={{ maxWidth: 'xs' }}
        >

            <Box>
                <ImageUpload 
                    images={[profileImage]} 
                    setImages={(images) => {
                        setProfileImage(images[0]);
                    }} 
                    maxImages={1} 
                    buttonText='Upload Profile Image' 
                    imageSx={{ height: '200px' }}
                    buttonSx={{ display: editing ? 'flex' : 'none' }}
                    deletable={false}
                    avatar
                    replace
                />

                
            </Box>

            <TextField
                label='Username'
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={!editing}
            />  

            <TextField
                label='Email'
                type='email'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={!editing}
            />

            {editing && 
                <TextField
                    label='Confirm Password'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    type='password'
                />  
            }

            <Box display='flex' justifyContent={editing ? 'space-between' : 'center'}>
                <Button onClick={() => setEditing(!editing)}>
                    {editing ? 'Cancel' : 'Change Account Details'}
                </Button>

            {editing && 
                <Button type='submit' variant='contained'>
                    Save Changes
                </Button>
            }
            </Box>

        </FormWindow>
    );
}

export default AccountFormWindow;
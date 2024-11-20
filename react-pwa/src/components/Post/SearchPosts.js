import React, { useState } from 'react';
import { Box } from '@mui/material';

import { usePosts } from '../../context/PostContext';
import SearchInput from '../common/SearchInput';


function SearchPosts() {
  const { refreshPosts } = usePosts();

  const [title, setTitle] = useState('');

  const handleSubmit = async (e) => {
      e.preventDefault();
      await refreshPosts(title);
    };

  return (
    <Box 
        component="form" 
        onSubmit={handleSubmit}
        sx={{ display: 'flex', alignItems: 'center', width: '100%', maxWidth: '800px', p: 1 }}
    >
      <SearchInput
        value={title}
        setValue={setTitle}
        onSubmit={handleSubmit}
      />
    </Box>
  );
}

export default SearchPosts;

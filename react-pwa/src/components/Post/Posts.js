import React from 'react';
import { Box, Typography } from '@mui/material';

import { usePosts } from '../../context/PostContext';
import Post from './Post';
import FilterPostsButton from './FilterPostsButton';


function Posts() {
  const { posts } = usePosts();


  return (
    <Box sx={{ display: 'flex', flexDirection: 'column' }}>
     
      <FilterPostsButton />

      {/* The 'map' method creates a new array with the results of calling the provided function on every element in the array. */}
      {posts.map(post => (<Post key={post.id} post={post} />))}

      {/* If there are no posts, displaying a message: */}
      {posts.length === 0 && (
        <Typography variant='title' sx={{ marginX: 5, textAlign: 'center' }}>
          No Posts Found
        </Typography>
      )}
    </Box>
  );
}

export default Posts;

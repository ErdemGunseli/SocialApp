import React, { useState, useEffect } from 'react';
import { TextField} from '@mui/material';

import { usePosts } from '../../context/PostContext';
import { createPost, createPostImage } from '../../api/post';
import FormWindow from '../common/FormWindow';
import ImageUpload from '../common/ImageUpload';


// TODO: Editing posts and comments to be added later

// Variant can be 'createPost', 'editPost', 'createComment', 'editComment'
function CreatePostWindow({ isOpen, onClose, onSubmit=()=>{}, post=null, variant='createPost' }){
  const { refreshPosts } = usePosts();
  
  const isEditing = variant.toLowerCase().includes('edit');
  const isPost = variant.toLowerCase().includes('post');


  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [images, setImages] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);


  // Refreshing the fields when the window is opened/closed:
  useEffect(() => {
    if (isOpen) {
      if (isEditing && post) {
        setTitle(post.title);
        setBody(post.body);
        setImages(post.images.map(image => ({
          url: `http://localhost:8000/${image.url}`,
          id: image.id,
        })));
      } else {
        setTitle("");
        setBody("");
        setImages([]);
      }
    } else {
      setTitle("");
      setBody("");
      setImages([]);
    }
    setCurrentIndex(0);
  }, [isOpen, isEditing, post]);


  const handleSubmit = async (e) => {
    e.preventDefault();

    let newPost;
    if (isPost) {
      newPost = await createPost(title, body);
    } else {
      if (post) { // Ensure post is not null
        newPost = await createPost(`Commenting on ${post.title} by ${post.author.name}`, body, post.id);
      } else {
        // Handle the case where post is null
        console.error("Post is null, cannot create comment");
        return;
      }
    }
    
    // Not using 'Promise.all', to ensure the images are uploaded in the correct order:
    // await Promise.all(images.map(image => createPostImage(post.id, image.file)));
    
    for (let image of images) {
      // Accessing the file itself for upload, not the preview URL:
      if (newPost && newPost.id) { // Ensure newPost and newPost.id are not null
        await createPostImage(newPost.id, image.file);
      } else {
        console.error("New post is null or does not have an ID, cannot upload images");
        return;
      }
    }
    onClose();
    await refreshPosts();
    onSubmit();
  }
  
  return (
    <FormWindow 
      isOpen={isOpen} 
      onClose={onClose} 
      onSubmit={handleSubmit} 
      sx={{ maxWidth: 'sm' }}
      title={`${isEditing ? 'Edit' : 'Create'} ${isPost ? 'Post' : 'Comment'}`} 
      buttonText='Post'
    >

      {isPost && (
        <TextField
          label='Title'
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />  
      )}

      <TextField
        label={isPost ? 'Body' : 'Your Comment'}
        value={body}
        onChange={(e) => setBody(e.target.value)}
        multiline
        rows={4}
        required
      />

      <ImageUpload 
        images={images} 
        setImages={setImages} 
        currentIndex={currentIndex} 
        setCurrentIndex={setCurrentIndex} 
        maxImages={4} 
      />

    </FormWindow>
  );
}

export default CreatePostWindow;
  
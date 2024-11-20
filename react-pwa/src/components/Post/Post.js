import React, { useEffect, useState } from 'react';
import { Card, Box, Typography, Button, Avatar, IconButton } from '@mui/material';
import { ThumbUp, ThumbDown, Comment, Edit } from '@mui/icons-material';
import moment from 'moment';

import { useUser } from '../../context/UserContext';
import { getPost, vote } from '../../api/post';
import CreatePostWindow from './CreatePostWindow';
import ImageCarousel from '../common/ImageCarousel';


function Post({ post }) {
    const { user } = useUser();
    const [upvoteCount, setUpvoteCount] = useState(post.upvote_count);
    const [downvoteCount, setDownvoteCount] = useState(post.downvote_count);
    const [currentUserVote, setCurrentUserVote] = useState(post.current_user_vote);

    const [showComments, setShowComments] = useState(false)

    const [commentWindowOpen, setCommentWindowOpen] = useState(false);
    const [editWindowOpen, setEditWindowOpen] = useState(false);

    // Current index for the image carousel:
    const [currentIndex, setCurrentIndex] = useState(0);  
    const [commentCount, setCommentCount] = useState(post.comment_count);

    console.log(post);

    useEffect(() => {
        getPost(post.id).then(post => {
            setCurrentUserVote(post.current_user_vote);
            setCommentCount(post.comment_count)
        });
    }, [user]);

    // Normalize images to full URLs
    const imageUrls = post.images.map(image => `http://localhost:8000/${image.url}`);

    const handleVote = async (voteType) => {
        const response = await vote(post.id, voteType);
        if (response) {
            setUpvoteCount(response.upvote_count);
            setDownvoteCount(response.downvote_count);
            setCurrentUserVote(response.current_user_vote);
        } 
    };

    console.log(post);

    const handleNewComment = () => {
        setCommentCount(commentCount + 1);
    };

    return (
      <Card sx={{ m: 2, p: 2 }}>
        {/* Aligns children within this component to each side of the container */}
            {post.parent_id ? (
                <Box>
                    <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', mb: 0.75 }}>
                        <Avatar src={`http://localhost:8000/${post.author.profile_image?.url}`}  sx={{ mr: 1, width: 30, height: 30}}/>
                        <Typography variant='caption' color='text.secondary'>{post.author.name}</Typography>
        
                        {/* Using dot character for visual separation */}
                        <Typography variant='caption' color='text.secondary'>
                        • {moment(post.created_at).fromNow(true)}
                        </Typography>
                    </Box>
                    <Typography variant='body1' color='text.secondary'>
                        {post.body}
                    </Typography>
                </Box>
            ) : (
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Box>
                        <Typography variant='h5'>{post.title}</Typography>
                        <Typography variant='body1' color='text.secondary'>{post.body}</Typography>
                    </Box>

                    <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center',  ml: 1, mb: 0.5 }}>
                        <Avatar src={`http://localhost:8000/${post.author.profile_image?.url}`}  sx={{ mr: 1, width: 35, height: 35 }}/>
                        <Typography variant='caption' color='text.secondary'>{post.author.name}</Typography>

                        {/* Using dot character for visual separation */}
                        <Typography variant='caption' color='text.secondary'>
                        • {moment(post.created_at).fromNow(true)}
                        </Typography>
                    </Box>
                </Box>
            )}

        {imageUrls.length > 0 && (
            <ImageCarousel
                images={imageUrls}
                currentIndex={currentIndex}
                setCurrentIndex={setCurrentIndex}
            />
        )}

        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>

            <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
            
                {/* Upvote button and counter */}
                <Button 
                    startIcon={<ThumbUp />} 
                    onClick={() => handleVote('up')} 
                    color={currentUserVote === 'up' ? 'primary' : 'inherit'}
                >
                    {upvoteCount}
                </Button>
            
                
                {/* Downvote button and counter */}
                <Button 
                    startIcon={<ThumbDown />} 
                    onClick={() => handleVote('down')} 
                    color={currentUserVote === 'down' ? 'primary' : 'inherit'}
                >
                    {downvoteCount}
                </Button>

                {/* Box with left border for visual separation */}
                <Box sx={{ borderLeft: 1, height: 20, ml: 1, mr: 1 }} />

                {/* Comment button and counter */}
                <Button 
                    startIcon={<Comment />} 
                    onClick={() => setShowComments(!showComments)} 
                    color='inherit'
                >
                    {commentCount}
                </Button>
            </Box>

                {user && user.id === post.author.id && (
                    <IconButton 
                        color='inherit'
                        onClick={() => setEditWindowOpen(true)}
                    >
                        <Edit fontSize='small' />
                    </IconButton>
                )}

            </Box>

            <CreatePostWindow
                variant='editPost'
                isOpen={editWindowOpen}
                onClose={() => setEditWindowOpen(!editWindowOpen)}
                post={post}
            />

            {showComments && (
                <>
                    <Box sx={{ borderBottom: 1, width: '100%', my: 2, borderColor: 'lightgrey' }} />

                    <Button
                        startIcon={<Comment />}
                        variant='text'
                        onClick={() => setCommentWindowOpen(true)}
                    >
                        Reply to {post.author.name}
                    </Button>

                    <CreatePostWindow
                        variant='createComment'
                        isOpen={commentWindowOpen} 
                        onClose={() => setCommentWindowOpen(!commentWindowOpen)} 
                        post={post}
                        onSubmit={handleNewComment}
                    />

                    {post.comments.map(postResponse => (<Post post={postResponse} key={postResponse.id} />))} 
                </>
            )}
      </Card>
    );
}

export default Post;  
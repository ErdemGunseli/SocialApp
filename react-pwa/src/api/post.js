import sendRequest from './api';


export async function createPost(title, body, parent_id=null) {
    return await sendRequest('/post/', {
        method: 'POST' ,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, body, parent_id }),
      });
}

export async function getPost(postId) {
    return await sendRequest(`/post/${postId}`);
}


export async function getPosts(title = '', username = '', orderBy = '', userVote = '', userId = '') {
    const params = new URLSearchParams();
  
    if (title) params.append('title', title);
    if (username) params.append('username', username);
    if (orderBy) params.append('order_by', orderBy);
    if (userVote) params.append('user_vote', userVote);
    if (userId) params.append('user_id', userId);
  
    return await sendRequest(`/post/?${params.toString()}`);
}
  
  
export async function vote(postId, voteType) {
    return await sendRequest(`/post/${postId}/vote/?vote_type=${voteType}`, { method: 'POST' });
}


export async function createPostImage(postId, image) {
    const formData = new FormData();
    formData.append('image', image);

    return await sendRequest(`/post/${postId}/image/`, { method: 'POST', body: formData });
}

export async function getPostImageUrls(postId) {
    const response = await sendRequest(`/post/${postId}/images`);

    // Obtaining the urls from the response objects and adding the base URL:
    return response.map(image => image.url);
}
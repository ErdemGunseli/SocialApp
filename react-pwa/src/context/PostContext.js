import { useState, useEffect, createContext, useContext } from 'react';

import { getPosts } from '../api/post';


// Creating a context for the posts:
const PostContext = createContext();


export const PostProvider = ({ children }) => {
  const [posts, setPosts] = useState([]);


  const refreshPosts = async ( title = '', username = '', orderBy = '', userVote = '', userId = '' ) => {

    const response = await getPosts(title, username, orderBy, userVote, userId);

    setPosts(response || []);
  };

  // Refreshing the user data when the UserProvider mounts:
  useEffect(() => {
    const fetchData = async () => {
      await refreshPosts();
    };
    fetchData();
  }, []);


  return (
    <PostContext.Provider value={{ posts: posts, setPosts: setPosts, refreshPosts: refreshPosts }}>
      {children}
    </PostContext.Provider>
  );
};


// Custom hook to simplify usage slightly
// (Otherwise consumer would need to import useContext and UserContext, now only need useUser)
export const usePosts = () => {
    return useContext(PostContext);
};


export default PostContext;
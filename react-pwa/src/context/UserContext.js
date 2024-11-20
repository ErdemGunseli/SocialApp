import { useState, useEffect, createContext, useContext } from 'react';

import { getCurrentUser } from '../api/user';

// Creating a context for the user data:
const UserContext = createContext();


export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);


  const refreshUser = async () => {
    setUser(null);

    if (!localStorage.getItem('accessToken')) {
      return;
    }

    const response = await getCurrentUser();
    if (response?.id) {
      setUser(response);
    }

    return response;
  };

  const clearUser = () => {
    setUser(null)
  }


  // Refreshing the user data when the UserProvider mounts:
  useEffect(() => {
    const fetchData = async () => {
      await refreshUser();
    };
    fetchData();
  }, []);


  return (
    <UserContext.Provider value={{ user: user, setUser: setUser, refreshUser: refreshUser, clearUser: clearUser}}>
      {children}
    </UserContext.Provider>
  );
};


// Custom hook to simplify usage slightly
// (Otherwise consumer would need to import useContext and UserContext, now only need useUser)
export const useUser = () => {
    return useContext(UserContext);
};


export default UserContext;
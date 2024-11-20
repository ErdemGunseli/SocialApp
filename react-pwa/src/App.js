import { useEffect } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Button } from '@mui/material';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import theme from './themes/theme';
import { UserProvider } from './context/UserContext';
import { PostProvider } from './context/PostContext';
import Header from './components/common/Header';
import Posts from './components/Post/Posts';


// TODO: Ensure ALL backend images return base url

// TODO: Backend should return base URL

// TODO: CreatePostWindow should handle creating posts, comments, and editing posts

// TODO: If the post is user's own, create an editing button

// TODO: Make the editing button work



// FIXME: Image upload not working, create better upload and carousel components

// TODO: Use theme value instead of px

// TODO: Implement themes and dark mode

// TODO: Animations using MUI Transitions

// TODO: Incorporate Aceternity (especially post card)

// TODO: Define strings externally


// TODO: Full review of app code, including backend, ensuring naming is consistent

// TODO: Combine components that have 2 variants, like create post, create comment, etc.

/* Code Review Points:
  1) Can this component be improved in some way?
  2) Can the logic be streamlined or simplified?
  3) Can the JSX be made shorter?
*/


function InstallButton() {
  return (
      <Button variant="text" color="primary">
        Install
      </Button>
  );
}


function App() {

  const showInstallPrompt = (e) => {
    e.preventDefault();
      toast.info('Install Social App?', {
        // Providing an ID to prevent it being duplicated:
        toastId: 'install-prompt',
        position: 'bottom-left',
        autoClose: 5000,
        pauseOnHover: true,
        onClick: () => e.prompt(),
        closeButton: <InstallButton />
      });  
  }

  useEffect(() => {
    window.addEventListener('beforeinstallprompt', showInstallPrompt);
  }, []);



  return (
    <ThemeProvider theme={theme}>
      {/* 'CssBaseline' normalizes CSS across different browsers */}
      <CssBaseline />

      <Box>
          <UserProvider>
            <PostProvider>

              <ToastContainer 
                position='top-left'
                autoClose={2500}
                pauseOnHover
                style={{ zIndex: 9999 }}
              />

              <Header />
              <Posts />

            </PostProvider>
          </UserProvider> 
      </Box>
    </ThemeProvider>
  );
}

export default App;
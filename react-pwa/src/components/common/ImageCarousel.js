import { Box, IconButton, Typography, Avatar } from '@mui/material';
import { ArrowBack, ArrowForward } from '@mui/icons-material';


// A component that cycles through a list of images:
function ImageCarousel({ 
    images, 
    currentIndex, 
    setCurrentIndex, 
    imageSx,
    // Whether to use an avatar or image component:
    avatar = false
}) {

    const handlePrev = () => setCurrentIndex((index) => (index - 1 + images.length) % images.length);
    const handleNext = () => setCurrentIndex((index) => (index + 1) % images.length);

    const avatarSize = imageSx?.height || imageSx?.width || '400px';

    // Ensuring currentIndex is within bounds
    if (currentIndex < 0 || currentIndex >= images.length) {
        return null;
    }

    // Function to get the correct image source
    const getImageSrc = (image) => {
        if (typeof image === 'string') {
            // If image is a string, return it directly
            return image;
        } else if (image.url) {
            // If image is an object with a 'url' property, build the full URL
            return `http://localhost:8000/${image.url}`;
        } else {
            // Handle other cases or return a placeholder image
            return ''; // Or provide a default image URL
        }
    };

    return (
        <Box sx={{position: 'relative', display: 'flex', alignItems: 'center', flexDirection: 'column'}}>

            {images.length > 0 && (
                <Box sx={{ flex: 1, display: 'flex', justifyContent: 'center' }}>

                    {avatar ? 
                        <Avatar
                            src={getImageSrc(images[currentIndex])}
                            alt={`${currentIndex + 1}/${images.length}`}
                            sx={{ width: avatarSize, height: avatarSize, ...imageSx }}
                        /> 
                    :
                        <Box
                            component='img'
                            src={getImageSrc(images[currentIndex])}
                            alt={`${currentIndex + 1}/${images.length}`}
                            sx={{ maxHeight: '400px', maxWidth: '100%', borderRadius: '10px', ...imageSx }}
                        />
                    }
                </Box>
            )}

            {images.length > 1 && (
                <Box sx={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            
                    <IconButton onClick={handlePrev}>
                        <ArrowBack />
                    </IconButton>
                    
                    <Typography>{`${currentIndex + 1}/${images.length}`}</Typography>
                    
                    <IconButton onClick={handleNext}>
                        <ArrowForward />
                    </IconButton>
                </Box>
            )}

        </Box>
    );
}

export default ImageCarousel
import React from 'react';
import { Box, Button, IconButton } from '@mui/material';
import { UploadFile, Delete } from '@mui/icons-material';

import ImageCarousel from './ImageCarousel';

function ImageUpload({
    images,
    setImages,
    maxImages = null,

    currentIndex = 0,
    setCurrentIndex = () => {},

    imageSx,
    avatar = false,

    replace = false,  // Whether existing images should be replaced or added to
    deletable = true,  // Whether the delete button should be shown
    buttonText = 'Add Image',
    buttonSx,
    allowedMimeTypes = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml", "image/bmp"],
}) {
    
    // A function that returns whether the limit has been reached / exceeded:
    const limit = (newImageCount = 0) => {
        let totalCount = newImageCount;

        if (!replace) { 
            totalCount += images.length; 
        }

        return {
            reached: totalCount >= maxImages,
            exceeded: totalCount > maxImages
        };
    };



    const handleFileChange = (event) => {
        const files = [...event.target.files];
        
        if (limit(files.length).exceeded){
            alert(`You can upload a maximum of ${maxImages} images.`);
            return;
        } 

        // Formatting the files to be used in the image carousel:
        const newImages = files.map(file => ({
            url: URL.createObjectURL(file),  // URL for preview
            file  // Actual file for upload
        }));

        let updatedImages;

        if (replace) {
            // Replacing existing images:
            updatedImages = [...newImages];
        } else {
            // Adding new images to existing ones:
            updatedImages = [...images, ...newImages];
        }

        setImages(updatedImages);

        // Moving to the last image:
        setCurrentIndex(updatedImages.length - 1);
    };


    const handleDelete = () => {
        // Excluding the current index:
        const newImages = images.filter((_, index) => index !== currentIndex);
        setImages(newImages);
        setCurrentIndex(prevIndex => (prevIndex > 0 ? prevIndex - 1 : 0));
    };

    
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            {images.length > 0 && (
                <Box sx={{ position: 'relative', display: 'flex', alignItems: 'center', mb: 2 }}>
                    {/* Passing the preview URLs to the ImageCarousel component */}
                    <ImageCarousel 
                        images={images.map(img => img.url)} 
                        currentIndex={currentIndex} 
                        setCurrentIndex={setCurrentIndex} 
                        imageSx={imageSx}        
                        avatar={avatar}
                    />

                    {deletable && (
                        <IconButton
                            onClick={handleDelete}
                            color="error"
                            sx={{ position: 'absolute', top: 10, right: 10 }}
                        >
                            <Delete />
                        </IconButton>
                    )}
                </Box>
            )}

            <Box sx={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
                <input
                    accept={allowedMimeTypes.join(',')}
                    style={{ display: 'none' }}
                    id="upload-button-file"
                    type="file"
                    multiple={maxImages === null || maxImages > 1}
                    onChange={handleFileChange}
                />

                {/* 'htmlFor' is used to associate the label with the input */}
                    <label htmlFor={limit().reached ? null : "upload-button-file"}>
                        <Button
                            component="span"
                            variant="outlined"
                            color="primary"
                            sx={buttonSx}
                            disabled={limit().reached}
                            startIcon={<UploadFile />}
                        >
                            {buttonText}
                    </Button>
                </label>
            </Box>
        </Box>
    );
}

export default ImageUpload;
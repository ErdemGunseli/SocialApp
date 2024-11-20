import { Button, Box, Typography } from '@mui/material';

import Window from './Window';


function FormWindow({ isOpen, onClose, onSubmit,
                        title, titleSx, buttonText, buttonSx, sx,
                        children }) {

    return (
        <Window isOpen={isOpen} onClose={onClose} sx={sx}>
  
          <Typography variant='title' sx={titleSx}>
            {title}
          </Typography>
  
          <Box component='form'
            onSubmit={onSubmit}
            sx={{ display: 'flex', flexDirection: 'column', marginY: 3, gap: 2 }}
          >
            {children}

            <Button type='submit' variant='contained' sx={{ mt: 1, ...buttonSx }}>
                {buttonText}
              </Button>
          </Box>
        </Window>
      );
}

export default FormWindow;
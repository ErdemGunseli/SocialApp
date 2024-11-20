import { Box, Dialog, DialogActions, DialogContent, IconButton } from '@mui/material';
import { Cancel } from '@mui/icons-material';


function Window({ isOpen, onClose, sx, children }){

  // Guard clause to prevent opening multiple windows:
  if (!isOpen) return null;
  
  return (
    <Box sx={{ maxWidth: sx?.maxWidth || 'xs', ...sx }}>
      <Dialog
        open={isOpen}
        onClose={onClose}
        fullWidth
        // Using the maxWidth prop directly
        maxWidth={sx?.maxWidth || 'xs'}
        PaperProps={{ sx: { borderRadius: 3 } }}
      >
        <DialogActions>
          <IconButton onClick={onClose} sx={{ padding: 0 }}>
            <Cancel />
          </IconButton>
        </DialogActions>

        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingX: 2 }}>
          <DialogContent sx={{ width: '100%', padding: 1 }}>
            {children}
          </DialogContent>
        </Box>
      </Dialog>
    </Box>
  );
}

export default Window;
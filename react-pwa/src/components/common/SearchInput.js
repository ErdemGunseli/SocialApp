import { OutlinedInput, InputAdornment } from '@mui/material';
import { Search, Clear } from '@mui/icons-material';

function SearchInput({ value, setValue, onsubmit }) {
  return (
    <OutlinedInput
      fullWidth
      placeholder="Search"
      sx={{ borderRadius: 20 }}
      value={value}
      onChange={(e) => setValue(e.target.value)}
      startAdornment={
        <InputAdornment position="start">
          <Search 
            onClick={onsubmit}
            sx={{ cursor: 'pointer' }}
          />
        </InputAdornment>
      }
      endAdornment={
        value && ( 
          <InputAdornment position="end">
            <Clear 
              onClick={() => setValue('')} 
              sx={{ cursor: 'pointer' }}
            />
          </InputAdornment>
        )
      }
    />
  );
}

export default SearchInput;
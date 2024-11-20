import React, { useState } from 'react';
import { Box, Button, TextField, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import { FilterList } from '@mui/icons-material';

import { usePosts } from '../../context/PostContext';
import { useUser } from '../../context/UserContext';


function FilterPostsButton() {
    const { user } = useUser();
    const { refreshPosts } = usePosts();

    // Whether the post filter menu is open:
    const [menuOpen, setMenuOpen] = useState(false)

    const [username, setUsername] = useState("");
    const [title, setTitle] = useState("");
    const [orderBy, setOrderBy] = useState("");
    const [show, setShow] = useState("");


    const countActiveFilters = () => {
        const filters = [username, title, show === 'all' ? null : show];
        return filters.filter(Boolean).length;
    }

    // Always correct since component is re-rendered when a state variable changes:
    const activeFilterCount = countActiveFilters();

    const resetFilters = async () => {
        setUsername("");
        setTitle("");
        setOrderBy("");
        setShow("");
        // Getting & displaying posts without filters:
        await refreshPosts();
        setMenuOpen(false);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (show === 'up' || show === 'down') {
            await refreshPosts(title, username, orderBy, show, null);
          } else if (!isNaN(show)) {
            // If 'show' is a number, it is a user ID:
            await refreshPosts(title, username, orderBy, null, show );
          } else {
            await refreshPosts(title, username, orderBy);
          }

        setMenuOpen(false);
        countActiveFilters();
    };

    return (
        <Box sx={{ m: 2, maxWidth: 300 }}>
            <Button endIcon={<FilterList />} onClick={() => setMenuOpen(!menuOpen)}>Filter</Button>

            {/* Button to reset filters: */}
            {activeFilterCount > 0 && (
                <Button onClick={resetFilters}>
                    {`${activeFilterCount} Filter${activeFilterCount > 1 ? 's' : ''} - Reset`}
                </Button>
            )}

            {/* Filtering options menu: */}
            {menuOpen && (
                <Box component='form' onSubmit={handleSubmit}
                    sx={{ display: 'flex', flexDirection: 'column', gap: 1, m: 2, mb: 5 }}
                >

                    <FormControl>
                        <InputLabel>Show</InputLabel>
                        <Select
                            value={show}
                            defaultValue={'all'}
                            onChange={(e) => setShow(e.target.value)}
                            label={'Show'}
                        >
                            <MenuItem value={'all'}>All Posts</MenuItem>
                            <MenuItem value={user.id}>Your Posts</MenuItem>
                            <MenuItem value={'up'}>Liked Posts</MenuItem>
                            <MenuItem value={'down'}>Disliked Posts</MenuItem>

                        </Select>
                    </FormControl>

                    <FormControl>
                        <InputLabel>Order By</InputLabel>
                        <Select
                            value={orderBy}
                            onChange={(e) => setOrderBy(e.target.value)}
                            label={'Order By'}
                        >
                            <MenuItem value={'date'}>Post Date</MenuItem>
                            <MenuItem value={'popularity'}>Popularity</MenuItem>
                        </Select>
                    </FormControl>

                    <TextField
                        label='Title'
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />

                    <TextField
                        label='Username'
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />

                    <Button type='submit' variant='contained'>
                        Filter
                    </Button>
                </Box>
            )}
        </Box>
    );
}
export default FilterPostsButton;
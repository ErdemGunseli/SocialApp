import sendRequest from './api';
import { encodeForm } from './api';

  
export async function login(email, password) {
    const response = await sendRequest('/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: encodeForm({ username: email, password: password }),
    });

    // Saving the JWT:
    if (response?.access_token) {
        localStorage.setItem('accessToken', response.access_token);
    }

    return response;
}


export function userLoggedIn() {
  return !!localStorage.getItem('accessToken');
}


export function logout() {
    localStorage.removeItem('accessToken');
    window.location.reload();
}
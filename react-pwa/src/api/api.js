import { toast } from 'react-toastify';


export const BASE_URL = 'http://localhost:8000';


class ApiError extends Error {
    constructor(message, status) {
        super(message)
        this.name = 'ApiError'
        this.status = status
    }
}
// Makes a HTTP request to the specified endpoint and handles the response.
// 'options' can be used to specify the method, headers, body, etc.
async function sendRequest(endpoint, options = {}) {

    // Ensuring the request always has headers (so token can be added):
    if (!options?.headers) { options.headers = {} }

    // Retrieving the token from localStorage and adding to headers:
    const token = localStorage.getItem('accessToken');
    if (token) { options.headers['Authorization'] = `Bearer ${token}`; }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);

        let responseObject = null;
        const contentType = response.headers.get('content-type');
        if (response.status !== 204 && contentType && contentType.includes('application/json')) {
            responseObject = await response.json();
        }

        // If the server returns an error, creating an alert with the message:
        if (!response.ok) {
            const errorMessage = responseObject?.detail || `${response.statusText}` || 'An error has occurred, please try again later.'
            throw new ApiError(errorMessage, response.status);
        }
        
        return responseObject;

    // Catching any client-side errors (e.g. response has no content so '.json()' does not work):
    } catch (error) {
        toast.error(error.message, {
            toastId: 'api-error'
        })
        return null;
    }
}

export default sendRequest;


export function encodeForm(data) {
    return Object.keys(data)
    // Encoding for application/x-www-form-urlencoded
    // 'encodeURIComponent' encodes spaces and special characters etc.
    // Encoding in the form "key1=val1&key2=val2":
    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key]))
    .join('&');
}
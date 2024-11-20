import sendRequest from "./api";
import { login } from "./auth";


export async function createUser(name, email, password) {
    const response = await sendRequest('/user/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });


      if (response) {
        await login(email, password);
      }

      return response;
}


export async function getUser(userId) {
  return await sendRequest(`/user/${userId}`);
}


export async function getCurrentUser() {
  return await sendRequest('/user/');
}


export async function updateUser(name, email) {
    return await sendRequest('/user/', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email }),
    });
}


export async function createProfileImage(image) {
    const formData = new FormData();
    formData.append('image', image);

    return await sendRequest('/user/profile', {
        method: 'POST',
        body: formData,
    });
}

export async function getProfileImageUrl(userId) {

  const image = await sendRequest(`/user/${userId}/profile`);
  if (image) {
      return image.url;
  }

  return null;
}

export async function deleteProfileImage() {
    return await sendRequest('/user/profile', {
        method: 'DELETE',
    });
}
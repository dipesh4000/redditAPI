const API_BASE = 'http://127.0.0.1:8000';

const getToken = () => localStorage.getItem('token');

const handleResponse = async (response) => {
  if (response.status === 401) {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
    throw new Error('Unauthorized');
  }
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }
  return response.json();
};

export const signupUser = async (username, password, email) => {
  const response = await fetch(`${API_BASE}/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, email })
  });
  return handleResponse(response);
};

export const loginUser = async (username, password) => {
  const response = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return handleResponse(response);
};

export const fetchAllPosts = async () => {
  const response = await fetch(`${API_BASE}/`);
  return handleResponse(response);
};

export const fetchLatestPosts = async () => {
  const response = await fetch(`${API_BASE}/posts/latest`);
  return handleResponse(response);
};

export const fetchUserPosts = async (username) => {
  const response = await fetch(`${API_BASE}/users/${username}/posts`);
  return handleResponse(response);
};

export const createPost = async (title, content, subreddit) => {
  const response = await fetch(`${API_BASE}/users/posts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify({ title, content, subreddit })
  });
  return handleResponse(response);
};

export const updatePost = async (postId, title, content, subreddit) => {
  const response = await fetch(`${API_BASE}/users/posts/${postId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify({ title, content, subreddit })
  });
  return handleResponse(response);
};

export const deletePost = async (postId) => {
  const response = await fetch(`${API_BASE}/users/posts/${postId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${getToken()}` }
  });
  if (response.status === 401) {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
    throw new Error('Unauthorized');
  }
  if (!response.ok) throw new Error('Delete failed');
};

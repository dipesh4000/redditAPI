import * as api from './api.js';

const getCurrentUser = () => localStorage.getItem('username');

export const showError = (message) => {
  const errorDiv = document.getElementById('error');
  if (errorDiv) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => errorDiv.style.display = 'none', 5000);
  }
};

export const showLoading = (show) => {
  const loading = document.getElementById('loading');
  if (loading) loading.style.display = show ? 'block' : 'none';
};

export const renderPosts = (posts, container) => {
  const currentUser = getCurrentUser();
  container.innerHTML = posts.map(post => `
    <div class="post-card">
      <h3>${post.title}</h3>
      <p>${post.content}</p>
      <div class="post-meta">
        <span class="subreddit">${post.subreddit}</span> • 
        <span class="username" onclick="window.location.href='profile.html?user=${post.user}'">${post.user}</span>
      </div>
      ${currentUser === post.user ? `
        <div class="post-actions">
          <button onclick="window.editPost(${post.post_id}, '${post.title.replace(/'/g, "\\'")}'', '${post.content.replace(/'/g, "\\'")}'', '${post.subreddit.replace(/'/g, "\\'")}'')">Edit</button>
          <button onclick="window.deletePostHandler(${post.post_id})">Delete</button>
        </div>
      ` : ''}
    </div>
  `).join('');
};

export const handleSignup = async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  try {
    await api.signupUser(username, password, email);
    window.location.href = 'login.html';
  } catch (error) {
    showError(error.message);
  }
};

export const handleLogin = async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  try {
    const data = await api.loginUser(username, password);
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('username', username);
    window.location.href = 'index.html';
  } catch (error) {
    showError(error.message);
  }
};

export const loadAllPosts = async () => {
  showLoading(true);
  try {
    const posts = await api.fetchAllPosts();
    renderPosts(posts, document.getElementById('posts'));
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
};

export const loadLatestPosts = async () => {
  showLoading(true);
  try {
    const posts = await api.fetchLatestPosts();
    renderPosts(posts, document.getElementById('posts'));
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
};

export const handleCreatePost = async (e) => {
  e.preventDefault();
  const title = document.getElementById('post-title').value;
  const content = document.getElementById('post-content').value;
  const subreddit = document.getElementById('post-subreddit').value;
  try {
    await api.createPost(title, content, subreddit);
    e.target.reset();
    loadAllPosts();
  } catch (error) {
    showError(error.message);
  }
};

window.editPost = (id, title, content, subreddit) => {
  document.getElementById('edit-modal').style.display = 'flex';
  document.getElementById('edit-id').value = id;
  document.getElementById('edit-title').value = title;
  document.getElementById('edit-content').value = content;
  document.getElementById('edit-subreddit').value = subreddit;
};

window.closeModal = () => {
  document.getElementById('edit-modal').style.display = 'none';
};

export const handleUpdatePost = async (e) => {
  e.preventDefault();
  const id = document.getElementById('edit-id').value;
  const title = document.getElementById('edit-title').value;
  const content = document.getElementById('edit-content').value;
  const subreddit = document.getElementById('edit-subreddit').value;
  try {
    await api.updatePost(id, title, content, subreddit);
    window.closeModal();
    const params = new URLSearchParams(window.location.search);
    const username = params.get('user');
    if (username) {
      loadUserPosts(username);
    } else {
      loadAllPosts();
    }
  } catch (error) {
    showError(error.message);
  }
};

window.deletePostHandler = async (id) => {
  if (!confirm('Delete this post?')) return;
  try {
    await api.deletePost(id);
    const params = new URLSearchParams(window.location.search);
    const username = params.get('user');
    if (username) {
      loadUserPosts(username);
    } else {
      loadAllPosts();
    }
  } catch (error) {
    showError(error.message);
  }
};

export const loadUserPosts = async (username) => {
  showLoading(true);
  try {
    const posts = await api.fetchUserPosts(username);
    renderPosts(posts, document.getElementById('posts'));
  } catch (error) {
    showError(error.message);
  } finally {
    showLoading(false);
  }
};

export const logout = () => {
  localStorage.clear();
  window.location.href = 'login.html';
};

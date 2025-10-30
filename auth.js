// Auth.js - Client-side authentication using localStorage

// Initialize users in localStorage if not exists
if (!localStorage.getItem('users')) {
    localStorage.setItem('users', JSON.stringify([]));
}

// Get current user
function getCurrentUser() {
    const user = localStorage.getItem('currentUser');
    return user ? JSON.parse(user) : null;
}

// Set current user
function setCurrentUser(user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
}

// Logout
function logout() {
    localStorage.removeItem('currentUser');
    updateNav();
    window.location.href = 'main.html';
}

// Register new user
function register(username, email, password) {
    const users = JSON.parse(localStorage.getItem('users'));
    if (users.find(u => u.username === username || u.email === email)) {
        return false; // User already exists
    }
    users.push({ username, email, password, role: 'user' });
    localStorage.setItem('users', JSON.stringify(users));
    return true;
}

// Login
function login(username, password) {
    const users = JSON.parse(localStorage.getItem('users'));
    const user = users.find(u => u.username === username && u.password === password);
    if (user) {
        setCurrentUser(user);
        updateNav();
        return user;
    }
    return null;
}

// Update navigation based on auth status
function updateNav() {
    const user = getCurrentUser();
    const nav = document.querySelector('nav ul');
    if (!nav) return;

    // Remove existing auth links
    const existingAuth = nav.querySelectorAll('.auth-link');
    existingAuth.forEach(link => link.remove());

    if (user) {
        // Add logout and dashboard links
        const li = document.createElement('li');
        li.className = 'auth-link';
        li.innerHTML = `
            <a href="#" class="button" style="padding:8px 12px;border-radius:8px;background:transparent;border:1px solid rgba(255,255,255,0.2);">Welcome ${user.username}</a>
            <ul>
                <li><a href="${user.role === 'admin' ? 'admin-panel.html' : 'user-dashboard.html'}">Dashboard</a></li>
                <li><a href="#" onclick="logout()">Logout</a></li>
            </ul>
        `;
        nav.appendChild(li);
    } else {
        // Add login/register links
        const li = document.createElement('li');
        li.className = 'auth-link';
        li.innerHTML = `
            <a href="login.html" class="button" style="padding:8px 12px;border-radius:8px;background:transparent;border:1px solid rgba(255,255,255,0.2);">Sign In</a>
        `;
        nav.appendChild(li);
    }
}

// Check if user is admin
function isAdmin() {
    const user = getCurrentUser();
    return user && user.role === 'admin';
}

// Protect admin pages
function protectAdminPage() {
    if (!isAdmin()) {
        alert('Access denied. Admin login required.');
        window.location.href = 'login.html';
    }
}

// Protect user pages
function protectUserPage() {
    const user = getCurrentUser();
    if (!user) {
        alert('Please login first.');
        window.location.href = 'login.html';
    }
}

// Initialize nav on page load
document.addEventListener('DOMContentLoaded', updateNav);

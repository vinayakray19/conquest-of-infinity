/**
 * Navigation utilities - update nav links based on auth status
 */
document.addEventListener('DOMContentLoaded', async function() {
    const navLogin = document.getElementById('navLogin');
    if (!navLogin) return;

    // Check if user is authenticated
    const user = await Auth.checkAuth();
    
    if (user) {
        // User is logged in - show Profile link
        navLogin.href = 'profile.html';
        navLogin.textContent = 'Profile';
    } else {
        // User is not logged in - show Login link
        navLogin.href = 'login.html';
        navLogin.textContent = 'Login';
    }
});


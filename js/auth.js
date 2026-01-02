/**
 * Authentication utilities for managing login/logout and tokens
 */
const Auth = {
    /**
     * Get stored access token
     */
    getToken() {
        return localStorage.getItem('access_token');
    },

    /**
     * Store access token
     */
    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    /**
     * Remove access token (logout)
     */
    removeToken() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return !!this.getToken();
    },

    /**
     * Get authentication headers for API requests
     */
    getAuthHeaders() {
        const token = this.getToken();
        if (!token) {
            return {};
        }
        return {
            'Authorization': `Bearer ${token}`
        };
    },

    /**
     * Login and store token
     */
    async login(username, password) {
        try {
            const apiUrl = API.baseUrl || FrontendConfig.getApiBaseUrl();
            const response = await fetch(`${apiUrl}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }

            const data = await response.json();
            this.setToken(data.access_token);
            localStorage.setItem('username', data.username);
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    /**
     * Logout
     */
    async logout() {
        try {
            const token = this.getToken();
            if (token) {
                const apiUrl = API.baseUrl || FrontendConfig.getApiBaseUrl();
                await fetch(`${apiUrl}/api/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.removeToken();
            window.location.href = 'login.html';
        }
    },

    /**
     * Check current user info
     */
    async checkAuth() {
        const token = this.getToken();
        if (!token) {
            return null;
        }

        try {
            const apiUrl = API.baseUrl || FrontendConfig.getApiBaseUrl();
            const response = await fetch(`${apiUrl}/api/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                this.removeToken();
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('Auth check error:', error);
            this.removeToken();
            return null;
        }
    },

    /**
     * Require authentication - redirect to login if not authenticated
     */
    async requireAuth() {
        const user = await this.checkAuth();
        if (!user) {
            window.location.href = 'login.html';
            return false;
        }
        return true;
    }
};


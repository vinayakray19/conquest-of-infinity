/**
 * Frontend configuration
 */
const FrontendConfig = {
    // API base URL - automatically detects environment
    getApiBaseUrl: function() {
        // Allow override via window.API_BASE_URL
        if (window.API_BASE_URL) {
            return window.API_BASE_URL;
        }
        
        // If opened as file://, we need full URL
        // Check both ports 8000 and 8001
        if (window.location.protocol === 'file:') {
            return 'http://localhost:8001';
        }
        
        // If on localhost, use localhost API
        // Check both ports 8000 and 8001
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            // Default to 8001, but can be overridden
            return 'http://localhost:8001';
        }
        
        // GitHub Pages or other production hosting
        // Using Render API URL
        if (window.location.hostname.includes('github.io')) {
            return 'https://conquest-of-infinity.onrender.com';
        }
        
        // Default production API URL
        return 'https://conquest-of-infinity.onrender.com';
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FrontendConfig;
}


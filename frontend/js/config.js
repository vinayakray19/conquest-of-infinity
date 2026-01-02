/**
 * Frontend configuration
 */
const FrontendConfig = {
    // API base URL - automatically detects environment
    getApiBaseUrl: function() {
        // If opened as file://, we need full URL
        if (window.location.protocol === 'file:') {
            return 'http://localhost:8001';
        }
        // If on localhost, use localhost API
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8001';
        }
        // Production: use relative URLs if API is on same domain
        return '';
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FrontendConfig;
}


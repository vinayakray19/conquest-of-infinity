/**
 * API client for communicating with the backend
 */
const API = {
    baseUrl: FrontendConfig.getApiBaseUrl(),
    
    /**
     * Get all memos
     */
    async getMemos(order = 'desc', limit = 100, skip = 0) {
        const response = await fetch(
            `${this.baseUrl}/api/memos?order=${order}&limit=${limit}&skip=${skip}`
        );
        if (!response.ok) {
            throw new Error(`Failed to fetch memos: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    },
    
    /**
     * Get a memo by number
     */
    async getMemo(memoNumber) {
        const response = await fetch(`${this.baseUrl}/api/memos/${memoNumber}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch memo: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    },
    
    /**
     * Get memo navigation (prev/next)
     */
    async getMemoNavigation(memoNumber) {
        const response = await fetch(`${this.baseUrl}/api/memos/nav/${memoNumber}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch navigation: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    },
    
    /**
     * Create a new memo (requires authentication)
     */
    async createMemo(memoData) {
        const headers = {
            'Content-Type': 'application/json',
            ...Auth.getAuthHeaders()
        };
        const response = await fetch(`${this.baseUrl}/api/memos`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(memoData)
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: response.statusText }));
            throw new Error(error.detail || `Failed to create memo: ${response.status}`);
        }
        return await response.json();
    },
    
    /**
     * Update a memo
     */
    async updateMemo(memoNumber, memoData) {
        const response = await fetch(`${this.baseUrl}/api/memos/${memoNumber}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(memoData)
        });
        if (!response.ok) {
            throw new Error(`Failed to update memo: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    },
    
    /**
     * Delete a memo (requires authentication)
     */
    async deleteMemo(memoNumber) {
        const headers = {
            ...Auth.getAuthHeaders()
        };
        const response = await fetch(`${this.baseUrl}/api/memos/${memoNumber}`, {
            method: 'DELETE',
            headers: headers
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: response.statusText }));
            throw new Error(error.detail || `Failed to delete memo: ${response.status}`);
        }
    },
    
    /**
     * Get statistics
     */
    async getStats() {
        const response = await fetch(`${this.baseUrl}/api/stats`);
        if (!response.ok) {
            throw new Error(`Failed to fetch stats: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    }
};


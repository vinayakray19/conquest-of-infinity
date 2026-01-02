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
     * Create a new memo
     */
    async createMemo(memoData) {
        const response = await fetch(`${this.baseUrl}/api/memos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(memoData)
        });
        if (!response.ok) {
            const error = await response.text();
            throw new Error(`Failed to create memo: ${response.status} ${error}`);
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
     * Delete a memo
     */
    async deleteMemo(memoNumber) {
        const response = await fetch(`${this.baseUrl}/api/memos/${memoNumber}`, {
            method: 'DELETE'
        });
        if (!response.ok) {
            throw new Error(`Failed to delete memo: ${response.status} ${response.statusText}`);
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


/**
 * Utility functions
 */

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format content for display
 */
function formatContent(content) {
    if (!content || content.trim() === '') {
        return '<p>No content available.</p>';
    }
    
    // Normalize <br> tags first
    content = content.replace(/<br\s*\/?>/gi, '<br>');
    
    // If content already contains HTML paragraph tags, preserve the structure
    if (content.includes('<p>') || content.includes('</p>')) {
        // Content already has HTML formatting with <p> tags
        // Just clean up whitespace and ensure proper formatting
        return content.replace(/^\s+|\s+$/gm, '') // trim each line
                      .replace(/\n\s*\n\s*\n+/g, '\n\n') // normalize spacing
                      .trim();
    }
    
    // If content has <br> tags but no <p> tags, split by double newlines and wrap
    if (content.includes('<br>')) {
        // Split by double newlines (paragraphs)
        const sections = content.split(/\n\s*\n/).filter(s => s.trim());
        
        if (sections.length === 0) {
            // Single section
            return `<p>${content.trim()}</p>`;
        }
        
        return sections.map(section => {
            section = section.trim();
            if (!section) return '';
            // Normalize <br> tags
            section = section.replace(/<br\s*\/?>/gi, '<br>');
            return `<p>${section}</p>`;
        }).filter(p => p).join('\n                    ');
    }
    
    // Plain text content - format it properly
    // Split by double newlines (paragraphs)
    const paragraphs = content.split(/\n\s*\n/).filter(p => p.trim());
    
    if (paragraphs.length === 0) {
        // Single paragraph - replace single newlines with <br>
        const singlePara = content.trim();
        if (singlePara.includes('\n')) {
            // Has newlines, convert to <br>
            const withBreaks = singlePara.replace(/\n/g, '<br>');
            // Escape HTML but preserve <br> tags
            const parts = withBreaks.split('<br>');
            const escaped = parts.map(p => escapeHtml(p)).join('<br>');
            return `<p>${escaped}</p>`;
        } else {
            // No newlines, just escape
            return `<p>${escapeHtml(singlePara)}</p>`;
        }
    }
    
    return paragraphs.map(para => {
        para = para.trim();
        if (!para) return '';
        // Replace single newlines with <br> within paragraphs
        if (para.includes('\n')) {
            const withBreaks = para.replace(/\n/g, '<br>');
            // Escape HTML but preserve <br> tags
            const parts = withBreaks.split('<br>');
            const escaped = parts.map(p => escapeHtml(p)).join('<br>');
            return `<p>${escaped}</p>`;
        } else {
            return `<p>${escapeHtml(para)}</p>`;
        }
    }).filter(p => p).join('\n                    ');
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
        return dateString;
    }
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
}

/**
 * Show error message
 */
function showError(container, message, apiUrl = '') {
    if (!container) return;
    container.innerHTML = 
        `<div class="error" style="padding: 2rem; text-align: center;">
            <h2>Error</h2>
            <p>${escapeHtml(message)}</p>
            ${apiUrl ? `<p style="margin-top: 1rem; font-size: 0.9em; color: #666;">API URL: ${apiUrl}</p>` : ''}
            <p style="margin-top: 0.5rem; font-size: 0.9em; color: #666;">
                Make sure the API server is running
            </p>
        </div>`;
}


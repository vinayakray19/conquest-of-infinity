/**
 * Diary listing page functionality
 */

const MEMOS_PER_PAGE = 10;
let currentPage = 1;
let totalMemos = 0;

// Load memos when page loads
document.addEventListener('DOMContentLoaded', async function() {
    // Get page from URL if present
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    if (pageParam) {
        currentPage = parseInt(pageParam) || 1;
    }
    await loadMemos();
});

async function loadMemos() {
    try {
        const skip = (currentPage - 1) * MEMOS_PER_PAGE;
        console.log(`Loading memos from ${API.baseUrl}/api/memos (page ${currentPage}, skip ${skip})`);
        
        // First get total count for pagination
        if (totalMemos === 0) {
            const allMemos = await API.getMemos('desc', 1000, 0);
            totalMemos = allMemos.length;
        }
        
        const memos = await API.getMemos('desc', MEMOS_PER_PAGE, skip);
        console.log(`Loaded ${memos.length} memos (page ${currentPage} of ${Math.ceil(totalMemos / MEMOS_PER_PAGE)})`);
        
        const entriesContainer = document.getElementById('diary-entries');
        if (!entriesContainer) {
            console.error('Diary entries container not found');
            return;
        }
        
        entriesContainer.innerHTML = '';
        
        if (memos.length === 0) {
            entriesContainer.innerHTML = '<p>No memos found.</p>';
            renderPagination();
            return;
        }
        
        if (!Array.isArray(memos)) {
            console.error('Expected array but got:', typeof memos, memos);
            throw new Error('Invalid response format: expected array');
        }
        
        memos.forEach((memo, index) => {
            try {
                const entryDiv = document.createElement('div');
                entryDiv.className = 'entry';
                
                // Validate memo structure
                if (!memo.memo_number || !memo.title || !memo.date) {
                    console.warn('Invalid memo structure:', memo);
                    return;
                }
                
                const formattedDate = formatDate(memo.date);
                
                entryDiv.innerHTML = `
                    <a href="memo.html?number=${memo.memo_number}" class="entry-link">
                        <span class="entry-number">Memo #${memo.memo_number}.</span>
                        <span class="entry-title">${escapeHtml(memo.title)}.</span>
                        <span class="entry-date">${formattedDate}</span>
                    </a>
                `;
                
                entriesContainer.appendChild(entryDiv);
            } catch (err) {
                console.error(`Error processing memo ${index}:`, err, memo);
            }
        });
        
        // Update suggested read link (use first memo of current page)
        const suggestedRead = document.querySelector('.suggested-read');
        if (suggestedRead && memos.length > 0) {
            const firstMemo = memos[0];
            suggestedRead.href = `memo.html?number=${firstMemo.memo_number}`;
            suggestedRead.textContent = firstMemo.title;
        }
        
        // Render pagination
        renderPagination();
        
    } catch (error) {
        console.error('Error loading memos:', error);
        const entriesContainer = document.getElementById('diary-entries');
        if (entriesContainer) {
            showError(entriesContainer, error.message, `${API.baseUrl}/api/memos`);
            // Add retry button
            const retryBtn = document.createElement('button');
            retryBtn.textContent = 'Retry';
            retryBtn.style.cssText = 'margin-top: 1rem; padding: 0.5rem 1rem; cursor: pointer;';
            retryBtn.onclick = () => loadMemos();
            entriesContainer.appendChild(retryBtn);
        }
    }
}

function renderPagination() {
    const totalPages = Math.ceil(totalMemos / MEMOS_PER_PAGE);
    
    // Remove existing pagination
    const existingPagination = document.getElementById('pagination');
    if (existingPagination) {
        existingPagination.remove();
    }
    
    if (totalPages <= 1) {
        return; // No pagination needed
    }
    
    const entriesContainer = document.getElementById('diary-entries');
    if (!entriesContainer) return;
    
    const paginationDiv = document.createElement('div');
    paginationDiv.id = 'pagination';
    paginationDiv.style.cssText = 'margin-top: 2rem; padding: 1.5rem; text-align: center;';
    
    let paginationHTML = '<div style="display: flex; justify-content: center; align-items: center; gap: 1rem; flex-wrap: wrap;">';
    
    // Previous button
    if (currentPage > 1) {
        paginationHTML += `<button onclick="goToPage(${currentPage - 1})" style="padding: 0.5rem 1rem; background: #4a9eff; color: white; border: none; border-radius: 6px; cursor: pointer;">← Previous</button>`;
    } else {
        paginationHTML += `<button disabled style="padding: 0.5rem 1rem; background: #ccc; color: #666; border: none; border-radius: 6px; cursor: not-allowed;">← Previous</button>`;
    }
    
    // Page numbers
    const maxPagesToShow = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
    let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);
    
    if (endPage - startPage < maxPagesToShow - 1) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }
    
    if (startPage > 1) {
        paginationHTML += `<button onclick="goToPage(1)" style="padding: 0.5rem 1rem; background: #f0f0f0; border: 1px solid #ddd; border-radius: 6px; cursor: pointer;">1</button>`;
        if (startPage > 2) {
            paginationHTML += `<span style="padding: 0.5rem;">...</span>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        if (i === currentPage) {
            paginationHTML += `<button disabled style="padding: 0.5rem 1rem; background: #4a9eff; color: white; border: none; border-radius: 6px; font-weight: bold;">${i}</button>`;
        } else {
            paginationHTML += `<button onclick="goToPage(${i})" style="padding: 0.5rem 1rem; background: #f0f0f0; border: 1px solid #ddd; border-radius: 6px; cursor: pointer;">${i}</button>`;
        }
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationHTML += `<span style="padding: 0.5rem;">...</span>`;
        }
        paginationHTML += `<button onclick="goToPage(${totalPages})" style="padding: 0.5rem 1rem; background: #f0f0f0; border: 1px solid #ddd; border-radius: 6px; cursor: pointer;">${totalPages}</button>`;
    }
    
    // Next button
    if (currentPage < totalPages) {
        paginationHTML += `<button onclick="goToPage(${currentPage + 1})" style="padding: 0.5rem 1rem; background: #4a9eff; color: white; border: none; border-radius: 6px; cursor: pointer;">Next →</button>`;
    } else {
        paginationHTML += `<button disabled style="padding: 0.5rem 1rem; background: #ccc; color: #666; border: none; border-radius: 6px; cursor: not-allowed;">Next →</button>`;
    }
    
    paginationHTML += '</div>';
    paginationHTML += `<div style="margin-top: 1rem; color: #666; font-size: 0.9rem;">Page ${currentPage} of ${totalPages} (${totalMemos} memos total)</div>`;
    
    paginationDiv.innerHTML = paginationHTML;
    entriesContainer.appendChild(paginationDiv);
}

// Make function globally accessible for onclick handlers
window.goToPage = function(page) {
    currentPage = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
    loadMemos();
    // Update URL without reload
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.history.pushState({ page }, '', url);
};


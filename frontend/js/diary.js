/**
 * Diary listing page functionality
 */

// Load memos when page loads
document.addEventListener('DOMContentLoaded', async function() {
    await loadMemos();
});

async function loadMemos() {
    try {
        console.log(`Loading memos from ${API.baseUrl}/api/memos`);
        const memos = await API.getMemos('desc', 100, 0);
        console.log(`Loaded ${memos.length} memos`);
        
        const entriesContainer = document.getElementById('diary-entries');
        if (!entriesContainer) {
            console.error('Diary entries container not found');
            return;
        }
        
        entriesContainer.innerHTML = '';
        
        if (memos.length === 0) {
            entriesContainer.innerHTML = '<p>No memos found.</p>';
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
        
        // Update suggested read link
        const suggestedRead = document.querySelector('.suggested-read');
        if (suggestedRead && memos.length > 12) {
            // Find memo #13 or closest
            const memo13 = memos.find(m => m.memo_number === 13) || memos[Math.floor(memos.length / 2)];
            if (memo13) {
                suggestedRead.href = `memo.html?number=${memo13.memo_number}`;
                suggestedRead.textContent = memo13.title;
            }
        }
        
    } catch (error) {
        console.error('Error loading memos:', error);
        const entriesContainer = document.getElementById('diary-entries');
        if (entriesContainer) {
            showError(entriesContainer, error.message, `${API.baseUrl}/api/memos`);
            // Add retry button
            const retryBtn = document.createElement('button');
            retryBtn.textContent = 'Retry';
            retryBtn.style.cssText = 'margin-top: 1rem; padding: 0.5rem 1rem; cursor: pointer;';
            retryBtn.onclick = loadMemos;
            entriesContainer.appendChild(retryBtn);
        }
    }
}


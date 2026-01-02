/**
 * Individual memo page functionality
 */

// Load memo when page loads
document.addEventListener('DOMContentLoaded', async function() {
    await loadMemo();
});

async function loadMemo() {
    try {
        // Get memo number from URL query parameter
        const urlParams = new URLSearchParams(window.location.search);
        const memoNumber = urlParams.get('number');
        
        if (!memoNumber) {
            const contentDiv = document.querySelector('.content');
            if (contentDiv) {
                showError(contentDiv, 'Memo number not specified.');
            }
            return;
        }
        
        console.log(`Loading memo #${memoNumber}`);
        
        // Load memo and navigation
        let memo, nav;
        try {
            [memo, nav] = await Promise.all([
                API.getMemo(memoNumber),
                API.getMemoNavigation(memoNumber).catch(err => {
                    console.warn('Navigation failed:', err);
                    return { previous: null, next: null, current: null };
                })
            ]);
        } catch (fetchError) {
            console.error('Network error:', fetchError);
            throw new Error(`Failed to connect to API. Make sure the server is running at ${API.baseUrl}`);
        }
        
        console.log('Memo loaded:', memo);
        console.log('Navigation:', nav);
        
        // Validate memo data
        if (!memo.memo_number || !memo.title) {
            throw new Error('Invalid memo data received from API');
        }
        
        // Update page title
        document.title = `Memo #${memo.memo_number}: ${memo.title} - A Digital Diary`;
        
        // Update header
        const h1 = document.querySelector('h1');
        const h2 = document.querySelector('h2');
        const dateP = document.querySelector('.article-date');
        
        if (h1) h1.textContent = `Memo #${memo.memo_number}`;
        if (h2) h2.textContent = memo.title;
        if (dateP) dateP.textContent = formatDate(memo.date);
        
        // Update content
        const contentDiv = document.querySelector('.article-content');
        if (!contentDiv) {
            throw new Error('Content container not found');
        }
        
        if (memo.content && memo.content.trim()) {
            console.log('Formatting content, length:', memo.content.length);
            const formatted = formatContent(memo.content);
            console.log('Formatted content preview:', formatted.substring(0, 200));
            contentDiv.innerHTML = formatted;
        } else {
            console.warn('No content for memo:', memo.memo_number);
            contentDiv.innerHTML = '<p>No content available for this memo.</p>';
        }
        
        // Update navigation
        const navDiv = document.querySelector('.article-navigation');
        if (!navDiv) {
            console.warn('Navigation container not found');
        } else {
            let navHTML = '';
            
            if (nav.previous) {
                navHTML += `<a href="memo.html?number=${nav.previous.memo_number}" class="nav-button prev">← Previous Memo</a>`;
            } else {
                navHTML += '<span></span>';
            }
            
            if (nav.next) {
                navHTML += `<a href="memo.html?number=${nav.next.memo_number}" class="nav-button next">Next Memo →</a>`;
            }
            
            navDiv.innerHTML = navHTML;
        }
        
    } catch (error) {
        console.error('Error loading memo:', error);
        const contentDiv = document.querySelector('.content');
        if (contentDiv) {
            showError(contentDiv, error.message, API.baseUrl);
            // Add back link
            const backLink = document.createElement('p');
            backLink.style.marginTop = '1rem';
            backLink.innerHTML = '<a href="diary.html">← Back to Diary</a>';
            contentDiv.appendChild(backLink);
        }
    }
}


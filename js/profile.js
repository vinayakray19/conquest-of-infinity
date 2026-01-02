/**
 * Profile page functionality
 */

// Profile state
let currentUser = null;
let currentPageProfile = 1;
let totalMemosProfile = 0;
const MEMOS_PER_PAGE_PROFILE = 10;

// Initialize profile page
document.addEventListener('DOMContentLoaded', async function() {
    const authenticated = await Auth.requireAuth();
    if (!authenticated) {
        return; // Redirect to login
    }

    // Get current user info
    currentUser = await Auth.checkAuth();
    if (currentUser) {
        console.log('Logged in as:', currentUser.username);
    }

    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('date');
    if (dateInput) {
        dateInput.value = today;
    }

    // Set username in personal info
    const usernameDisplay = document.getElementById('usernameDisplay');
    if (currentUser && usernameDisplay) {
        usernameDisplay.value = currentUser.username;
    }

    // Load saved personal info
    loadPersonalInfo();

    // Load existing memos (first page)
    await loadPosts(1);

    // Setup sidebar navigation
    setupSidebarNavigation();

    // Setup event listeners
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function() {
            if (confirm('Are you sure you want to logout?')) {
                await Auth.logout();
            }
        });
    }

    // Save personal info button
    const savePersonalInfoBtn = document.getElementById('savePersonalInfo');
    if (savePersonalInfoBtn) {
        savePersonalInfoBtn.addEventListener('click', function() {
            const email = document.getElementById('email').value;
            const bio = document.getElementById('bio').value;
            const messageContainer = document.getElementById('personalInfoMessage');
            
            // For now, just save to localStorage (can be extended to API)
            if (email) localStorage.setItem('user_email', email);
            if (bio) localStorage.setItem('user_bio', bio);
            
            showMessageInContainer(messageContainer, 'Personal information saved successfully!', 'success');
            
            // Note: This is a placeholder. In a full implementation, you'd:
            // 1. Create a user profile endpoint in the API
            // 2. Store email/bio in the database
            // 3. Update the user model to include these fields
        });
    }

    // Form submission
    const addPostForm = document.getElementById('addPostForm');
    if (addPostForm) {
        addPostForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            await handleFormSubmission();
        });
    }
}

// Setup sidebar navigation
function setupSidebarNavigation() {
    const navLinks = document.querySelectorAll('.nav-link-sidebar');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links and sections
            document.querySelectorAll('.nav-link-sidebar').forEach(l => l.classList.remove('active'));
            document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link and corresponding section
            this.classList.add('active');
            const sectionId = this.dataset.section;
            const section = document.getElementById(sectionId);
            if (section) {
                section.classList.add('active');
            }
        });
    });
}

// Load saved personal info from localStorage
function loadPersonalInfo() {
    const email = localStorage.getItem('user_email');
    const bio = localStorage.getItem('user_bio');
    
    const emailInput = document.getElementById('email');
    const bioInput = document.getElementById('bio');
    
    if (email && emailInput) emailInput.value = email;
    if (bio && bioInput) bioInput.value = bio;
}

// Show message in container
function showMessageInContainer(container, message, type) {
    if (!container) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.textContent = message;
    container.innerHTML = '';
    container.appendChild(messageDiv);
    
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}

// Handle form submission
async function handleFormSubmission() {
    const titleInput = document.getElementById('title');
    const dateInput = document.getElementById('date');
    const contentInput = document.getElementById('content');
    const messageContainer = document.getElementById('messageContainer');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!titleInput || !dateInput || !contentInput || !messageContainer || !submitBtn) {
        console.error('Required form elements not found');
        return;
    }
    
    const title = titleInput.value.trim();
    const dateValue = dateInput.value;
    const content = contentInput.value.trim();
    
    // Clear previous messages
    messageContainer.innerHTML = '';
    
    if (!title || !dateValue || !content) {
        showMessage('Please fill in all required fields.', 'error');
        return;
    }
    
    // Convert date to proper format
    const date = new Date(dateValue + 'T00:00:00');
    const dateStr = date.toISOString().split('T')[0];
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating...';
    
    try {
        // Get next memo number
        const memos = await API.getMemos('desc', 1, 0);
        const nextMemoNumber = memos.length > 0 ? memos[0].memo_number + 1 : 1;
        
        const memoData = {
            memo_number: nextMemoNumber,
            title: title,
            content: content,
            date: dateStr
        };
        
        const createdMemo = await API.createMemo(memoData);
        
        showMessage(`Memo created successfully! Memo #${createdMemo.memo_number}: "${createdMemo.title}"`, 'success');
        
        // Reset form
        const form = document.getElementById('addPostForm');
        if (form) {
            form.reset();
            dateInput.value = new Date().toISOString().split('T')[0];
        }
        
        // Show preview
        showMemoPreview(createdMemo);
        
        // Reset total count and reload posts list (go to first page to show new memo)
        totalMemosProfile = 0;
        currentPageProfile = 1;
        await loadPosts(1);
        
        // Scroll to the posts section
        const postsSection = document.querySelector('.posts-section');
        if (postsSection) {
            postsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
    } catch (error) {
        console.error('Error creating post:', error);
        showMessage(`Failed to create memo: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create Memo';
    }
}

// Navigate to page (global function for onclick handlers)
window.goToPageProfile = async function(page) {
    if (!page || page < 1) {
        console.error('Invalid page number:', page);
        return;
    }
    console.log(`[Pagination] Navigating to page ${page}`);
    currentPageProfile = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
    await loadPosts(page);
};

// Load and display existing memos
async function loadPosts(page = 1) {
    const postsList = document.getElementById('postsList');
    const postsLoading = document.getElementById('postsLoading');
    
    if (!postsList || !postsLoading) {
        console.error('Posts list or loading element not found');
        return;
    }
    
    currentPageProfile = page;
    postsLoading.style.display = 'block';
    postsList.style.display = 'none';
    postsList.innerHTML = '';
    
    try {
        // Get total count first (only if not already set or if we're on page 1)
        if (totalMemosProfile === 0 || page === 1) {
            const allMemos = await API.getMemos('desc', 1000, 0);
            totalMemosProfile = allMemos.length;
        }
        
        const skip = (page - 1) * MEMOS_PER_PAGE_PROFILE;
        const memos = await API.getMemos('desc', MEMOS_PER_PAGE_PROFILE, skip);
        
        postsLoading.style.display = 'none';
        postsList.style.display = 'block';
        postsList.innerHTML = '';
        
        if (memos.length === 0 && page === 1) {
            postsList.innerHTML = '<div class="empty-state">No memos yet. Create your first memo above!</div>';
            return;
        }
        
        memos.forEach(memo => {
            const li = document.createElement('li');
            li.className = 'post-item';
            
            const date = new Date(memo.date);
            const formattedDate = date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
            
            li.innerHTML = `
                <div class="post-info">
                    <h3>Memo #${memo.memo_number}: ${escapeHtml(memo.title)}</h3>
                    <div class="post-date">${formattedDate}</div>
                </div>
                <div class="post-actions">
                    <a href="memo.html?number=${memo.memo_number}" class="btn-secondary">View</a>
                </div>
            `;
            
            postsList.appendChild(li);
        });
        
        // Render pagination
        renderPaginationProfile();
        
    } catch (error) {
        console.error('Error loading memos:', error);
        postsLoading.innerHTML = '<div class="error-message">Failed to load memos. Please refresh the page.</div>';
    }
}

// Render pagination controls
function renderPaginationProfile() {
    const totalPages = Math.ceil(totalMemosProfile / MEMOS_PER_PAGE_PROFILE);
    const postsSection = document.querySelector('.posts-section');
    if (!postsSection) return;
    
    // Remove existing pagination
    const existingPagination = document.getElementById('profilePagination');
    if (existingPagination) {
        existingPagination.remove();
    }
    
    if (totalPages <= 1) {
        return; // No pagination needed
    }
    
    const paginationDiv = document.createElement('div');
    paginationDiv.id = 'profilePagination';
    paginationDiv.style.cssText = 'margin-top: 2rem; padding: 1.5rem; text-align: center; border-top: 1px solid #eee;';
    
    let paginationHTML = '<div style="display: flex; justify-content: center; align-items: center; gap: 0.5rem; flex-wrap: wrap;">';
    
    // Previous button
    if (currentPageProfile > 1) {
        paginationHTML += `<button onclick="window.goToPageProfile(${currentPageProfile - 1})" class="btn-secondary" style="min-width: 100px; cursor: pointer;">← Previous</button>`;
    } else {
        paginationHTML += `<button disabled class="btn-secondary" style="min-width: 100px; opacity: 0.5; cursor: not-allowed;">← Previous</button>`;
    }
    
    // Page info
    paginationHTML += `<span style="padding: 0 1rem; color: #666; font-weight: 500;">Page ${currentPageProfile} of ${totalPages}</span>`;
    
    // Next button
    if (currentPageProfile < totalPages) {
        paginationHTML += `<button onclick="window.goToPageProfile(${currentPageProfile + 1})" class="btn-secondary" style="min-width: 100px; cursor: pointer;">Next →</button>`;
    } else {
        paginationHTML += `<button disabled class="btn-secondary" style="min-width: 100px; opacity: 0.5; cursor: not-allowed;">Next →</button>`;
    }
    
    paginationHTML += '</div>';
    paginationHTML += `<div style="margin-top: 0.5rem; color: #999; font-size: 0.85rem;">Showing ${((currentPageProfile - 1) * MEMOS_PER_PAGE_PROFILE) + 1}-${Math.min(currentPageProfile * MEMOS_PER_PAGE_PROFILE, totalMemosProfile)} of ${totalMemosProfile} memos</div>`;
    
    paginationDiv.innerHTML = paginationHTML;
    postsSection.appendChild(paginationDiv);
}

// Show message
function showMessage(message, type) {
    const messageContainer = document.getElementById('messageContainer');
    if (!messageContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.textContent = message;
    messageContainer.innerHTML = '';
    messageContainer.appendChild(messageDiv);
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// Show memo preview
function showMemoPreview(memo) {
    const messageContainer = document.getElementById('messageContainer');
    if (!messageContainer) return;
    
    const previewDiv = document.createElement('div');
    previewDiv.className = 'memo-preview';
    previewDiv.innerHTML = `
        <h3>Preview: Memo #${memo.memo_number}</h3>
        <p><strong>Title:</strong> ${escapeHtml(memo.title)}</p>
        <p><strong>Date:</strong> ${new Date(memo.date).toLocaleDateString()}</p>
        <p><strong>Content:</strong> ${escapeHtml(memo.content).substring(0, 100)}${memo.content.length > 100 ? '...' : ''}</p>
        <p><a href="memo.html?number=${memo.memo_number}">View full memo →</a></p>
    `;
    messageContainer.appendChild(previewDiv);
}


/**
 * Profile page functionality
 */

// Profile state
let currentUser = null;

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
        
        // Form submitted successfully - preview is shown above
        
    } catch (error) {
        console.error('Error creating post:', error);
        showMessage(`Failed to create memo: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create Memo';
    }
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


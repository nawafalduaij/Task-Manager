// API server URL
const API_URL = 'http://localhost:8000';

// When page loads, setup everything
window.onload = function() {
    setupTabs();
    setupFilters();
    loadTasks();
    loadUsers();
};

// Tab switching
function setupTabs() {
    const buttons = document.querySelectorAll('.tab-btn');
    
    buttons.forEach(btn => {
        btn.onclick = function() {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            const tabName = btn.dataset.tab;
            document.getElementById(tabName + 'Tab').classList.add('active');
        };
    });
}

// Filter setup
function setupFilters() {
    document.getElementById('statusFilter').onchange = loadTasks;
    document.getElementById('priorityFilter').onchange = loadTasks;
    document.getElementById('roleFilter').onchange = loadUsers;
}

// Load Tasks
async function loadTasks() {
    const tasksDiv = document.getElementById('tasksList');
    tasksDiv.innerHTML = '<div class="loading">Loading...</div>';
    
    try {
        const status = document.getElementById('statusFilter').value;
        const priority = document.getElementById('priorityFilter').value;
        
        let url = API_URL + '/tasks/?';
        if (status) url += 'status=' + status + '&';
        if (priority) url += 'priority=' + priority + '&';
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.tasks.length === 0) {
            tasksDiv.innerHTML = '<div class="empty-state">No tasks found</div>';
        } else {
            tasksDiv.innerHTML = data.tasks.map(task => `
                <div class="task-card">
                    <div class="task-title">${task.title}</div>
                    <div class="task-description">${task.description || 'No description'}</div>
                    <div class="task-meta">
                        <span class="badge badge-priority-${task.priority}">${task.priority}</span>
                        <span class="badge badge-status-${task.status}">${task.status}</span>
                    </div>
                    <div class="assigned-to">Assigned: ${task.assigned_to || 'Unassigned'}</div>
                    <div class="task-info">Task ID: ${task.id}</div>
                </div>
            `).join('');
        }
    } catch (error) {
        tasksDiv.innerHTML = '<div class="error-message">Error: ' + error.message + '</div>';
    }
}

// Load Users
async function loadUsers() {
    const usersDiv = document.getElementById('usersList');
    usersDiv.innerHTML = '<div class="loading">Loading...</div>';
    
    try {
        const role = document.getElementById('roleFilter').value;
        
        let url = API_URL + '/users/?';
        if (role) url += 'role=' + role;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.users.length === 0) {
            usersDiv.innerHTML = '<div class="empty-state">No users found</div>';
        } else {
            usersDiv.innerHTML = data.users.map(user => `
                <div class="user-card">
                    <div class="user-name">${user.username}</div>
                    <div class="user-details">Email: ${user.profile.email}</div>
                    <div class="user-details">Phone: ${user.profile.phone}</div>
                    <div class="task-meta">
                        <span class="badge badge-role">${user.role}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        usersDiv.innerHTML = '<div class="error-message">Error: ' + error.message + '</div>';
    }
}

// Task Modal
function openTaskModal() {
    document.getElementById('taskModal').classList.add('active');
    document.getElementById('taskForm').reset();
}

function closeTaskModal() {
    document.getElementById('taskModal').classList.remove('active');
}

async function handleTaskSubmit(event) {
    event.preventDefault();
    
    const taskData = {
        title: document.getElementById('taskTitle').value,
        description: document.getElementById('taskDescription').value,
        priority: document.getElementById('taskPriority').value,
        status: document.getElementById('taskStatus').value,
        assigned_to: document.getElementById('taskAssignedTo').value || ''
    };
    
    try {
        const response = await fetch(API_URL + '/tasks/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            // Extract the actual error message
            let errorMsg = 'Validation failed';
            if (error.detail && Array.isArray(error.detail)) {
                errorMsg = error.detail.map(e => e.msg).join(', ');
            } else if (error.detail) {
                errorMsg = error.detail;
            }
            throw new Error(errorMsg);
        }
        
        closeTaskModal();
        loadTasks();
        alert('Task created successfully!');
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// User Modal
function openUserModal() {
    document.getElementById('userModal').classList.add('active');
    document.getElementById('userForm').reset();
}

function closeUserModal() {
    document.getElementById('userModal').classList.remove('active');
}

async function handleUserSubmit(event) {
    event.preventDefault();
    
    const userData = {
        username: document.getElementById('username').value,
        role: document.getElementById('userRole').value,
        profile: {
            email: document.getElementById('userEmail').value,
            phone: document.getElementById('userPhone').value,
            address: document.getElementById('userAddress').value || ''
        }
    };
    
    try {
        const response = await fetch(API_URL + '/users/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            // Extract the actual error message
            let errorMsg = 'Validation failed';
            if (error.detail && Array.isArray(error.detail)) {
                errorMsg = error.detail.map(e => e.msg).join(', ');
            } else if (error.detail) {
                errorMsg = error.detail;
            }
            throw new Error(errorMsg);
        }
        
        closeUserModal();
        loadUsers();
        alert('User created successfully!');
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Close modals when clicking outside
window.onclick = function(event) {
    const taskModal = document.getElementById('taskModal');
    const userModal = document.getElementById('userModal');
    
    if (event.target === taskModal) closeTaskModal();
    if (event.target === userModal) closeUserModal();
}

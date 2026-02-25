/**
 * Career Assistant AI Agent - Frontend Application
 * Handles chat interaction, API calls, and UI updates.
 */

const API_BASE = '';

// ===== Test Cases =====
const TEST_CASES = {
    1: {
        name: "HR Manager",
        email: "hr@techcorp.com",
        subject: "Interview Invitation",
        message: `Dear Burak,

We have reviewed your application for the Software Engineer position at TechCorp and are impressed with your experience in Python, FastAPI, and AI systems.

We would like to invite you for a technical interview next Monday at 10:00 AM (Turkey time). The interview will be conducted via Google Meet and will last approximately 1 hour. It will include a technical discussion about your RAG system project and a short coding exercise.

Please confirm your availability at your earliest convenience.

Best regards,
Sarah Johnson
HR Manager, TechCorp`
    },
    2: {
        name: "Tech Lead",
        email: "techlead@startup.io",
        subject: "Technical Question",
        message: `Hi Burak,

I saw your profile and I'm interested in your experience with AI and backend development. I have a few technical questions:

1. Can you explain how you implemented the RAG system at SAN TSG? What embedding model did you use and how did you handle document chunking?
2. What's your experience with FastAPI middleware and dependency injection?
3. Have you worked with any CI/CD pipelines for deploying Python applications?

Looking forward to your response.

Best,
Alex Chen
Tech Lead at StartupIO`
    },
    3: {
        name: "Recruiter",
        email: "recruiter@bigcorp.com",
        subject: "Job Offer - Salary Discussion",
        message: `Dear Burak,

Congratulations! After careful evaluation, we would like to extend a job offer for the position of Junior AI Engineer at BigCorp.

We need to discuss your salary expectations. Based on our internal bands, the position offers between $150,000 - $200,000 annually plus stock options and a signing bonus. We also need you to sign a 2-year non-compete agreement.

Could you share your expected compensation package? Also, our legal team needs to discuss the intellectual property assignment clause in the contract.

Best regards,
Michael Brown
Senior Recruiter, BigCorp`
    }
};

// ===== Load Test Case =====
function loadTestCase(num) {
    const tc = TEST_CASES[num];
    document.getElementById('senderName').value = tc.name;
    document.getElementById('senderEmail').value = tc.email;
    document.getElementById('subject').value = tc.subject;
    document.getElementById('messageInput').value = tc.message;
    document.getElementById('messageInput').focus();
}

// ===== Send Message =====
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    if (!message) return;

    const senderName = document.getElementById('senderName').value || 'Employer';
    const senderEmail = document.getElementById('senderEmail').value || 'employer@company.com';
    const subject = document.getElementById('subject').value || 'General Inquiry';

    // Disable send button
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;

    // Add employer message to chat
    addMessage('employer', message, senderName);
    messageInput.value = '';

    // Show loading overlay
    showLoading();

    try {
        const response = await fetch(`${API_BASE}/api/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sender_name: senderName,
                sender_email: senderEmail,
                subject: subject,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        hideLoading();

        // Add agent response to chat
        addAgentResponse(data);

        // Update history
        loadHistory();

    } catch (error) {
        hideLoading();
        addMessage('agent', `❌ Error: ${error.message}. Please check that the server is running and your API key is configured.`, '🤖');
    } finally {
        sendBtn.disabled = false;
    }
}

// ===== Add Message to Chat =====
function addMessage(type, text, senderName) {
    const chatMessages = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type === 'employer' ? 'employer-message' : 'agent-message'}`;

    const avatar = type === 'employer' ? '👤' : '<img src="/static/avatar.jpg" alt="Burak" class="avatar-img">';

    msgDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-bubble">
                <p style="white-space: pre-wrap;">${escapeHtml(text)}</p>
            </div>
        </div>
    `;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ===== Add Agent Response =====
function addAgentResponse(data) {
    const chatMessages = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message agent-message';

    const unknown = data.unknown_detection;

    // Build unknown question alert
    let unknownHtml = '';
    if (unknown && unknown.is_unknown) {
        unknownHtml = `
            <div class="unknown-alert">
                <span class="unknown-alert-icon">⚠️</span>
                <div class="unknown-alert-content">
                    <h4>Human Intervention Required</h4>
                    <p><strong>Category:</strong> ${unknown.category.replace(/_/g, ' ')}</p>
                    <p>${unknown.reason}</p>
                </div>
            </div>
        `;
    }

    msgDiv.innerHTML = `
        <div class="message-avatar"><img src="/static/avatar.jpg" alt="Burak" class="avatar-img"></div>
        <div class="message-content">
            <div class="message-bubble">
                <p style="white-space: pre-wrap;">${escapeHtml(data.generated_response)}</p>
                ${unknownHtml}
            </div>
        </div>
    `;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ===== Thinking Animation (Modern LLM-style) =====
let thinkingElement = null;
let thinkingInterval = null;

function showLoading() {
    const chatMessages = document.getElementById('chatMessages');

    // Create thinking message bubble
    thinkingElement = document.createElement('div');
    thinkingElement.className = 'message agent-message thinking-message';
    thinkingElement.innerHTML = `
        <div class="message-avatar"><img src="/static/avatar.jpg" alt="Burak" class="avatar-img"></div>
        <div class="message-content">
            <div class="message-bubble thinking-bubble">
                <div class="thinking-status" id="thinkingStatus">Thinking</div>
                <div class="thinking-dots">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                </div>
            </div>
        </div>
    `;

    chatMessages.appendChild(thinkingElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Cycle through status texts
    const statuses = ['Analyzing message', 'Generating response', 'Evaluating quality', 'Finalizing'];
    let idx = 0;
    thinkingInterval = setInterval(() => {
        idx = (idx + 1) % statuses.length;
        const statusEl = document.getElementById('thinkingStatus');
        if (statusEl) statusEl.textContent = statuses[idx];
    }, 2500);
}

function hideLoading() {
    if (thinkingElement) {
        thinkingElement.remove();
        thinkingElement = null;
    }
    if (thinkingInterval) {
        clearInterval(thinkingInterval);
        thinkingInterval = null;
    }
}

// ===== History Panel =====
function toggleHistory() {
    const panel = document.getElementById('historyPanel');
    panel.classList.toggle('open');
    if (panel.classList.contains('open')) {
        loadHistory();
    }
}

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/api/history`);
        const data = await response.json();

        const historyList = document.getElementById('historyList');

        if (!data.conversations || data.conversations.length === 0) {
            historyList.innerHTML = `
                <div class="empty-history">
                    <p>No conversations yet.</p>
                    <p class="hint">Send a message to get started!</p>
                </div>
            `;
            return;
        }

        historyList.innerHTML = data.conversations.map(conv => {
            const scoreClass = conv.evaluation_score >= 7 ? 'score-high' : conv.evaluation_score >= 5 ? 'score-medium' : 'score-low';
            const time = new Date(conv.timestamp).toLocaleString();

            return `
                <div class="history-item">
                    <div class="history-item-header">
                        <span class="history-item-id">#${conv.id}</span>
                        <span class="history-item-score ${scoreClass}">${conv.evaluation_score}/10</span>
                    </div>
                    <div class="history-item-preview">${escapeHtml(conv.employer_message)}</div>
                    <div class="history-item-time">
                        ${time}
                        ${conv.is_unknown ? ' • ⚠️ Unknown' : ''}
                        ${conv.revision_count > 0 ? ` • 🔄 ${conv.revision_count} rev` : ''}
                    </div>
                </div>
            `;
        }).reverse().join('');

    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// ===== Utility =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== Keyboard shortcut =====
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('messageInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            sendMessage();
        }
    });
});

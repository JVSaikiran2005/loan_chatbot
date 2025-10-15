class ChatInterface {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.isLoading = false;
        this.currentInputType = 'text';
        
        this.initializeElements();
        this.bindEvents();
        this.updateLoanInfo();
    }
    
    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.inputOptions = document.getElementById('inputOptions');
        this.fileUploadSection = document.getElementById('fileUploadSection');
        this.downloadSection = document.getElementById('downloadSection');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.toastContainer = document.getElementById('toastContainer');
        this.fileInput = document.getElementById('fileInput');
        this.downloadButton = document.getElementById('downloadButton');
        
        // Loan info elements
        this.loanAmount = document.getElementById('loanAmount');
        this.interestRate = document.getElementById('interestRate');
        this.tenure = document.getElementById('tenure');
        this.emi = document.getElementById('emi');
        this.loanStatus = document.getElementById('loanStatus');
    }
    
    bindEvents() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // File upload events
        this.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        this.downloadButton.addEventListener('click', () => this.downloadSanctionLetter());
        
        // Input option buttons
        document.querySelectorAll('.option-button').forEach(button => {
            button.addEventListener('click', (e) => {
                this.setInputType(e.target.dataset.type);
            });
        });
    }
    
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        
        // Show loading
        this.setLoading(true);
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            // Add bot response
            this.addMessage(data.response, 'bot');
            
            // Handle special responses
            this.handleSpecialResponse(data);
            
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            this.showToast('Error occurred while processing your request', 'error');
        } finally {
            this.setLoading(false);
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.textContent = content;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        messageContent.appendChild(messageText);
        messageContent.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    handleSpecialResponse(data) {
        // Handle different input types
        if (data.requires_input) {
            this.showInputOptions(data.input_type);
        } else {
            this.hideInputOptions();
        }
        
        // Handle file upload requirement
        if (data.response.includes('salary slip') || data.response.includes('upload')) {
            this.showFileUpload();
        } else {
            this.hideFileUpload();
        }
        
        // Handle download section
        if (data.status === 'completed' || data.response.includes('sanction letter')) {
            this.showDownloadSection();
        } else {
            this.hideDownloadSection();
        }
        
        // Update loan status
        this.updateLoanStatus(data.status);
    }
    
    showInputOptions(inputType) {
        this.inputOptions.style.display = 'flex';
        this.currentInputType = inputType;
        
        // Update input placeholder and type
        switch(inputType) {
            case 'number':
                this.messageInput.placeholder = 'Enter a number...';
                this.messageInput.type = 'number';
                break;
            case 'phone':
                this.messageInput.placeholder = 'Enter 10-digit phone number...';
                this.messageInput.type = 'tel';
                break;
            default:
                this.messageInput.placeholder = 'Type your message here...';
                this.messageInput.type = 'text';
        }
    }
    
    hideInputOptions() {
        this.inputOptions.style.display = 'none';
        this.messageInput.placeholder = 'Type your message here...';
        this.messageInput.type = 'text';
    }
    
    setInputType(type) {
        this.currentInputType = type;
        
        // Update active button
        document.querySelectorAll('.option-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-type="${type}"]`).classList.add('active');
        
        // Update input
        this.showInputOptions(type);
    }
    
    showFileUpload() {
        this.fileUploadSection.style.display = 'block';
    }
    
    hideFileUpload() {
        this.fileUploadSection.style.display = 'none';
    }
    
    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        // Validate file type
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
            this.showToast('Please upload a PDF, JPG, or PNG file', 'error');
            return;
        }
        
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            this.showToast('File size should be less than 5MB', 'error');
            return;
        }
        
        this.setLoading(true);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('session_id', this.sessionId);
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showToast('File uploaded successfully!', 'success');
                this.addMessage(`File uploaded: ${file.name}`, 'user');
                
                // Continue the conversation
                setTimeout(() => {
                    this.sendMessage();
                }, 1000);
            } else {
                this.showToast(data.error || 'Upload failed', 'error');
            }
            
        } catch (error) {
            console.error('Upload error:', error);
            this.showToast('Upload failed. Please try again.', 'error');
        } finally {
            this.setLoading(false);
        }
    }
    
    showDownloadSection() {
        this.downloadSection.style.display = 'block';
    }
    
    hideDownloadSection() {
        this.downloadSection.style.display = 'none';
    }
    
    async downloadSanctionLetter() {
        try {
            const response = await fetch(`/api/download/${this.sessionId}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `sanction_letter_${this.sessionId}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                this.showToast('Sanction letter downloaded successfully!', 'success');
            } else {
                this.showToast('Download failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showToast('Download failed. Please try again.', 'error');
        }
    }
    
    updateLoanStatus(status) {
        const statusMap = {
            'initial': 'Getting Started',
            'sales': 'Collecting Information',
            'verification': 'Verifying Details',
            'underwriting': 'Processing Application',
            'sanction': 'Generating Documents',
            'completed': 'Approved'
        };
        
        this.loanStatus.textContent = statusMap[status] || 'In Progress';
        
        // Update status indicator
        const statusIndicator = document.getElementById('statusIndicator');
        if (status === 'completed') {
            statusIndicator.textContent = 'Completed';
            statusIndicator.style.background = '#27ae60';
        } else {
            statusIndicator.textContent = 'Processing';
            statusIndicator.style.background = '#f39c12';
        }
    }
    
    updateLoanInfo() {
        // This would be updated based on conversation data
        // For now, showing default values
        this.loanAmount.textContent = 'Not specified';
        this.interestRate.textContent = 'TBD';
        this.tenure.textContent = 'Not specified';
        this.emi.textContent = 'TBD';
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        this.loadingOverlay.style.display = loading ? 'flex' : 'none';
        this.sendButton.disabled = loading;
        
        if (loading) {
            this.messageInput.disabled = true;
        } else {
            this.messageInput.disabled = false;
            this.messageInput.focus();
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    getCurrentTime() {
        return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'error' ? 'exclamation-circle' : 'info-circle';
        
        toast.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${message}</span>
        `;
        
        this.toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }
    
    // Add typing indicator
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        
        return typingDiv;
    }
    
    hideTypingIndicator(typingElement) {
        if (typingElement) {
            typingElement.remove();
        }
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
});

// Add some utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-IN').format(number);
}


document.addEventListener('DOMContentLoaded', () => {
    const displayArea = document.getElementById('display-area');
    const messageInput = document.getElementById('message-input');
    const submitButton = document.getElementById('submit-btn');
    const header = document.getElementById('main-header');
    let lastScroll = 0;

    // Handle header visibility on scroll
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > lastScroll && currentScroll > 60) {
            header.classList.add('hidden');
        } else {
            header.classList.remove('hidden');
        }
        lastScroll = currentScroll;
    });

    function createMessageBubble(text, isUser = false) {
        if (isUser) {
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble user-message';
            return bubble;
        } else {
            const container = document.createElement('div');
            container.className = 'bot-message-container';
            
            const avatar = document.createElement('div');
            avatar.className = 'bot-avatar';
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble bot-message';
            
            container.appendChild(avatar);
            container.appendChild(bubble);
            return container;
        }
    }

    async function animateText(element, text) {
        const words = text.split(' ');
        for (let i = 0; i < words.length; i++) {
            const span = document.createElement('span');
            span.textContent = words[i];
            // Add space after word if it's not the last word
            if (i < words.length - 1) {
                span.textContent += ' ';
            }
            span.className = 'typing-animation';
            element.appendChild(span);
            await new Promise(resolve => setTimeout(resolve, 50));
        }
    }

    // Add auto-scroll functionality
    function scrollToBottom() {
        const displayArea = document.getElementById('display-area');
        displayArea.scrollTop = displayArea.scrollHeight;
    }

    // Set up observer for auto-scroll
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(displayArea, { 
        childList: true, 
        subtree: true 
    });

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        try {
            // Add user message
            const userBubble = createMessageBubble(message, true);
            userBubble.textContent = message;
            displayArea.appendChild(userBubble);
            messageInput.value = '';
            scrollToBottom(); // Add scroll after user message

            // Show loading
            submitButton.disabled = true;
            const botContainer = createMessageBubble('...', false);
            const botBubble = botContainer.querySelector('.bot-message');
            displayArea.appendChild(botContainer);

            const formData = new FormData();
            formData.append('mssg', message);
            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            botBubble.textContent = '';
            await animateText(botBubble, data.response);
        } catch (error) {
            console.error('Error:', error);
            const errorContainer = createMessageBubble('Error processing request', false);
            const errorBubble = errorContainer.querySelector('.bot-message');
            errorBubble.textContent = 'Error processing request';
            displayArea.appendChild(errorContainer);
        } finally {
            submitButton.disabled = false;
            scrollToBottom(); // Add scroll after bot response
        }
    }

    submitButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const displayArea = document.getElementById('display-area');
    const messageInput = document.getElementById('message-input');
    const submitButton = document.getElementById('submit-btn');
    const header = document.getElementById('main-header');
    let lastScroll = 0;

    // Add dropdown functionality
    const headerNav = document.querySelector('.header-nav');
    const firstNavBtn = headerNav.querySelector('.nav-btn');
    
    firstNavBtn.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            headerNav.classList.toggle('responsive');
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!headerNav.contains(e.target)) {
            headerNav.classList.remove('responsive');
        }
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            headerNav.classList.remove('responsive');
        }
    });

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
        const bubble = document.createElement('div');
        bubble.className = `message-bubble ${isUser ? 'user-message' : 'bot-message'}`;
        return bubble;
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

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        try {
            // Add user message
            const userBubble = createMessageBubble(message, true);
            userBubble.textContent = message;
            displayArea.appendChild(userBubble);
            messageInput.value = '';
            displayArea.scrollTop = displayArea.scrollHeight;

            // Show loading
            submitButton.disabled = true;
            const botBubble = createMessageBubble('...');
            displayArea.appendChild(botBubble);

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
            const errorBubble = createMessageBubble('Error processing request', false);
            displayArea.appendChild(errorBubble);
        } finally {
            submitButton.disabled = false;
            displayArea.scrollTop = displayArea.scrollHeight;
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

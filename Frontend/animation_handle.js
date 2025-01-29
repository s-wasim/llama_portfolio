document.addEventListener('DOMContentLoaded', () => {
    const popup = document.getElementById('welcome-popup');
    const closeBtn = document.getElementById('close-popup');
    const mainContent = document.getElementById('main-content');
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const dynamicText = document.getElementById('dynamic-text');

    // Function to handle sending message
    const sendMessage = () => {
        const text = userInput.value.trim();
        if (text) {
            dynamicText.textContent = text;
            userInput.value = '';
            
            // Auto-adjust text size based on content length
            const textLength = text.length;
            if (textLength > 200) {
                dynamicText.style.fontSize = '1rem';
            } else if (textLength > 100) {
                dynamicText.style.fontSize = '1.2rem';
            } else {
                dynamicText.style.fontSize = '1.5rem';
            }
        }
    };

    // Handle popup closing
    closeBtn.addEventListener('click', () => {
        popup.style.opacity = '0';
        popup.style.transform = 'scale(0.5)';
        popup.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        setTimeout(() => {
            popup.classList.add('hidden');
            mainContent.classList.remove('hidden');
            // Add entrance animation for main content
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(20px)';
            requestAnimationFrame(() => {
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
                mainContent.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            });
        }, 500);
    });

    // Handle send button click
    sendButton.addEventListener('click', sendMessage);

    // Handle enter key
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent new line
            sendMessage();
        }
    });
});

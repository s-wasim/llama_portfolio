document.addEventListener('DOMContentLoaded', () => {
    const hamburgerBtn = document.querySelector('.hamburger-btn');
    const sidePanel = document.querySelector('.side-panel');

    hamburgerBtn.addEventListener('click', () => {
        hamburgerBtn.classList.toggle('open');
        sidePanel.classList.toggle('open');
        document.body.classList.toggle('no-scroll');
    });

    // Close panel when clicking outside and remove no-scroll
    document.addEventListener('click', (e) => {
        if (!hamburgerBtn.contains(e.target) && 
            !sidePanel.contains(e.target) && 
            sidePanel.classList.contains('open')) {
            hamburgerBtn.classList.remove('open');
            sidePanel.classList.remove('open');
            document.body.classList.remove('no-scroll');
        }
    });

    const displayArea = document.getElementById('display-area');
    const messageInput = document.getElementById('message-input');
    const submitButton = document.getElementById('submit-btn');
    const header = document.getElementById('main-header');
    let lastScroll = 0;

    // Update header visibility on scroll
    window.addEventListener('scroll', () => {
        if (window.innerWidth > 768) {  // Only for desktop
            const currentScroll = window.pageYOffset;
            if (currentScroll > lastScroll && currentScroll > 60) {
                header.classList.add('hidden');
            } else {
                header.classList.remove('hidden');
            }
            lastScroll = currentScroll;
        }
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

    // Add navigation functionality
    const navButtons = document.querySelectorAll('.nav-btn');
    
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const sectionId = button.getAttribute('data-section');
            const section = document.getElementById(sectionId);
            section.scrollIntoView({ behavior: 'smooth' });
            
            // Close side panel if open
            if (sidePanel.classList.contains('open')) {
                hamburgerBtn.classList.remove('open');
                sidePanel.classList.remove('open');
                document.body.classList.remove('no-scroll');
            }
        });
    });

    loadWorkHistory();
});

async function loadWorkHistory() {
    try {
        const response = await fetch('/work-history');
        const data = await response.json();
        const workSection = document.querySelector('#work .section-content');
        
        let html = '<div class="timeline">';
        
        data.forEach((company, index) => {
            html += `
                <div class="timeline-item company">
                    <div class="timeline-marker"></div>
                    <div class="company-content">
                        <h3>${company.name}</h3>
                        <p class="role">${company.role}</p>
                    </div>
                </div>
            `;
            
            company.projects.forEach((project, pIndex) => {
                const isEven = pIndex % 2 === 0;
                html += `
                    <div class="timeline-item project ${isEven ? 'left' : 'right'}">
                        <div class="timeline-marker"></div>
                        <div class="project-content">
                            <h4>${project.name}</h4>
                            <div class="project-details">
                                ${project.details.map(detail => `<p>${detail}</p>`).join('')}
                            </div>
                        </div>
                    </div>
                `;
            });
        });
        
        html += '</div>';
        workSection.innerHTML = html;

        // Set up scroll-based timeline animation
        const timeline = document.querySelector('.timeline');
        const updateTimelineProgress = () => {
            const timelineRect = timeline.getBoundingClientRect();
            const timelineStart = timelineRect.top;
            const viewportMidpoint = window.innerHeight / 2;
            
            // Calculate progress based on viewport midpoint
            let progress;
            if (timelineStart > viewportMidpoint) {
                progress = 0;
            } else if (timelineStart < -timelineRect.height) {
                progress = 100;
            } else {
                const visiblePortion = viewportMidpoint - timelineStart;
                progress = (visiblePortion / timelineRect.height) * 100;
                progress = Math.min(Math.max(progress, 0), 100);
            }
            
            timeline.style.setProperty('--timeline-progress', `${progress}%`);
        };

        // Initial update
        updateTimelineProgress();

        // Update on scroll
        window.addEventListener('scroll', updateTimelineProgress);
        window.addEventListener('resize', updateTimelineProgress);

        // Setup intersection observer for individual items
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const elementRect = entry.boundingClientRect;
                const viewportMiddle = window.innerHeight / 2;
                const elementMiddle = elementRect.top + (elementRect.height / 2);
                
                if (entry.isIntersecting && Math.abs(elementMiddle - viewportMiddle) < 150) { // Increased threshold
                    // Add a small delay before adding the visible class
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, 100);
                    observer.unobserve(entry.target);
                }
            });
        }, { 
            threshold: [0, 0.2, 0.4, 0.6, 0.8], // More threshold points
            rootMargin: '-45% 0px -45% 0px' // Slightly adjusted trigger area
        });

        document.querySelectorAll('.timeline-item').forEach(item => {
            observer.observe(item);
        });
    } catch (error) {
        console.error('Error loading work history:', error);
    }
}
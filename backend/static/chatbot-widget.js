window.Fobi = (function () {
    let config = {};
    let chatbotId = '';
    let apiBaseUrl = '';

    function init(options) {
        config = options.config || {};
        chatbotId = options.chatbotId;
        apiBaseUrl = options.apiBaseUrl;

        createWidget();
    }

    function createWidget() {
        // Create container
        const container = document.createElement('div');
        container.id = `fobi-widget-${chatbotId}`;
        container.style.position = 'fixed';
        container.style.zIndex = '9999';
        container.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';

        // Position
        if (config.position === 'bottom-left') {
            container.style.bottom = '20px';
            container.style.left = '20px';
        } else {
            container.style.bottom = '20px';
            container.style.right = '20px';
        }

        // Toggle Button
        const button = document.createElement('button');
        button.style.width = '60px';
        button.style.height = '60px';
        button.style.borderRadius = '50%';
        button.style.backgroundColor = config.primaryColor || '#7c3aed';
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.cursor = 'pointer';
        button.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        button.style.display = 'flex';
        button.style.alignItems = 'center';
        button.style.justifyContent = 'center';
        button.style.transition = 'transform 0.2s';

        // Icon
        button.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`;

        // Chat Window (IFrame)
        const iframeContainer = document.createElement('div');
        iframeContainer.style.position = 'absolute';
        iframeContainer.style.bottom = '80px';
        iframeContainer.style.right = '0'; // align right relative to container
        if (config.position === 'bottom-left') {
            iframeContainer.style.left = '0';
            iframeContainer.style.right = 'auto';
        }
        iframeContainer.style.width = '350px';
        iframeContainer.style.height = '500px';
        iframeContainer.style.backgroundColor = 'white';
        iframeContainer.style.borderRadius = '12px';
        iframeContainer.style.boxShadow = '0 8px 32px rgba(0,0,0,0.15)';
        iframeContainer.style.display = 'none'; // Hidden by default
        iframeContainer.style.overflow = 'hidden';
        iframeContainer.style.opacity = '0';
        iframeContainer.style.transform = 'translateY(20px)';
        iframeContainer.style.transition = 'opacity 0.3s, transform 0.3s';

        const iframe = document.createElement('iframe');
        iframe.src = `${apiBaseUrl}/embed/${chatbotId}`;
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = 'none';

        iframeContainer.appendChild(iframe);
        container.appendChild(iframeContainer);
        container.appendChild(button);
        document.body.appendChild(container);

        // Toggle logic
        let isOpen = false;
        button.onclick = () => {
            isOpen = !isOpen;
            if (isOpen) {
                iframeContainer.style.display = 'block';
                // Small delay to allow display:block to apply before transition
                setTimeout(() => {
                    iframeContainer.style.opacity = '1';
                    iframeContainer.style.transform = 'translateY(0)';
                }, 10);
                button.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`;
            } else {
                iframeContainer.style.opacity = '0';
                iframeContainer.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    iframeContainer.style.display = 'none';
                }, 300);
                button.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`;
            }
        };
    }

    return {
        init: init
    };
})();

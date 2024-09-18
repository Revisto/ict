document.addEventListener('DOMContentLoaded', function() {
    var scriptTag = document.querySelector('script[src="http://127.0.0.1:5000/static/js/widget.js"]');
    
    if (scriptTag) {
        var campaignId = scriptTag.getAttribute('data-campaign-id');
        var gameId = scriptTag.getAttribute('data-game-id');

        var widgetIcon = document.createElement('div');
        widgetIcon.style.position = 'fixed';
        widgetIcon.style.bottom = '20px';
        widgetIcon.style.right = '20px';
        widgetIcon.style.width = '50px';
        widgetIcon.style.height = '50px';
        widgetIcon.style.backgroundColor = '#f00';
        widgetIcon.style.borderRadius = '50%';
        widgetIcon.style.cursor = 'pointer';
        widgetIcon.style.zIndex = '1000';
        document.body.appendChild(widgetIcon);

        widgetIcon.addEventListener('click', function() {
            var overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
            overlay.style.zIndex = '1001';
            document.body.appendChild(overlay);

            var gameContainer = document.createElement('div');
            gameContainer.style.position = 'fixed';
            gameContainer.style.top = '50%';
            gameContainer.style.left = '50%';
            gameContainer.style.transform = 'translate(-50%, -50%)';
            gameContainer.style.width = '80%';
            gameContainer.style.height = '80%';
            gameContainer.style.backgroundColor = '#fff';
            gameContainer.style.padding = '20px';
            gameContainer.style.zIndex = '1002';
            document.body.appendChild(gameContainer);

            var iframe = document.createElement('iframe');
            iframe.src = `http://127.0.0.1:5000/popup/${campaignId}/${gameId}`;
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.border = 'none';
            gameContainer.appendChild(iframe);

            overlay.addEventListener('click', function() {
                document.body.removeChild(overlay);
                document.body.removeChild(gameContainer);
            });
        });
    } else {
        console.error('Script tag with src "http://127.0.0.1:5000/static/js/widget.js" not found.');
    }
});
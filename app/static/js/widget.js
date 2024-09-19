// static/js/widget.js
document.addEventListener('DOMContentLoaded', function() {
    // Generate or retrieve UUID at the very beginning
    var userId = localStorage.getItem('user_uuid');
    console.log('User UUID:', userId);
    if (!userId) {
        userId = generateUUID();
        localStorage.setItem('user_uuid', userId);
        console.log('Generated new user UUID:', userId);
    }

    var scriptTag = document.querySelector('script[src="https://ict.revisto.lol/static/js/widget.js"]');
    
    if (scriptTag) {
        var context = scriptTag.getAttribute('data-context');
        var campaignId = scriptTag.getAttribute('data-campaign-id');
        var gameId = scriptTag.getAttribute('data-game-id');

        if (context !== 'game') {
            var widgetIcon = document.createElement('div');
            widgetIcon.style.position = 'fixed';
            widgetIcon.style.bottom = '20px';
            widgetIcon.style.right = '20px';
            widgetIcon.style.width = '50px';
            widgetIcon.style.height = '50px';
            widgetIcon.style.background = 'linear-gradient(45deg, #800080, #ff00ff)';
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
                // border radius
                gameContainer.style.borderRadius = '30px';
                document.body.appendChild(gameContainer);

                fetch(`https://ict.revisto.lol/popup/${campaignId}/${gameId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('user_uuid')}`
                    }
                })
                .then(response => response.text())
                .then(html => {
                    var iframe = document.createElement('iframe');
                    iframe.style.width = '100%';
                    iframe.style.height = '100%';
                    iframe.style.border = 'none';
                    iframe.srcdoc = html;
                    gameContainer.appendChild(iframe);

                })
                .catch(error => {
                    console.error('Error fetching the popup content:', error);
                });
                
                overlay.addEventListener('click', function() {
                    document.body.removeChild(overlay);
                    document.body.removeChild(gameContainer);
                });
            });
        }
    } else {
        console.error('Script tag with src "https://ict.revisto.lol/static/js/widget.js" not found.');
    }
});

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function getCoupon(campaignId) {
    fetch(`https://ict.revisto.lol/game/get_coupon/${campaignId}`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('user_uuid')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.coupon_code) {
                alert(`You won a coupon: ${data.coupon_code}`);
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}

function addScore(campaignId, scoreIncrement) {
    fetch(`https://ict.revisto.lol/game/add_score/${campaignId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('user_uuid')}`
        },
        body: JSON.stringify({ score_increment: scoreIncrement })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        alert(`Total Score: ${data.score}`);
        // Refresh the score after successful score update
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Failed to update score: ${error.message}`);
    });
}

function getUserScore(campaignId) {
    fetch(`https://ict.revisto.lol/game/get_user_score/${campaignId}`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('user_uuid')}`
        }
    })
        .then(response => response.json())
        .then(data => {
            var userScoreElement = document.getElementById('userScore');
            if (userScoreElement) {
                userScoreElement.textContent = data.score;
            } else {
                console.error('User score element not found.');
            }
        })
        .catch(error => console.error('Error:', error));
}
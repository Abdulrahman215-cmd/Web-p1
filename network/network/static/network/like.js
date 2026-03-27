document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId;
            // the csrftoken in this and headers was because of cs50 ai
            const csrfToken = button.dataset.csrfToken;
            fetch(`/toggle_like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector(`#like-count-${postId}`).innerHTML = data.like_count;
                const img = button.querySelector('img');
                if (data.liked) {
                    img.style.transform = 'rotate(180deg)';
                } else {
                    img.style.transform = 'rotate(0deg)';
                }
            });
        };
    });
});
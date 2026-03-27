document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach(button => {
        button.addEventListener('click', send);
    });
});

function send() {
    console.log("Edit button clicked");
    this.className = 'edit btn btn-primary';
    this.style.display = 'none';
    // i learned that i can use closest and replacechild because of cs50 ai
    const postDiv = this.closest('.post1');
    // instead of document cs50ai helped me and i used postDiv, i was having trouble until i used it
    const bodyP = postDiv.querySelector('.body');
    const textarea = document.createElement('textarea');
    textarea.value = bodyP.innerText;
    postDiv.replaceChild(textarea, bodyP);

    const saveButton = document.createElement('button');
    saveButton.innerText = 'Save';
    saveButton.id = 'save-button'; 
    saveButton.className = 'btn btn-primary'; 
    saveButton.disabled = true;
    // i never knew i can use styling in js
    saveButton.style.cssText = 'float: right;';
    this.parentElement.appendChild(saveButton);

    const originalText = textarea.value;

    textarea.addEventListener('input', function() {
        if (textarea.value === originalText) {
            saveButton.disabled = true;
        } else if (textarea.value.length === 0) {
            saveButton.disabled = true;
        } else {
            saveButton.disabled = false;
        }
    });

    saveButton.onclick = function() {
        console.log("Save button clicked");
        const updatedText = textarea.value;
        const postId = postDiv.dataset.postId;

        fetch(`/update_post/${postId}/`, {
            method: 'PUT',
            body: JSON.stringify({
                newPost: updatedText
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(result => {
            console.log(result);
            postDiv.querySelector('.edit').style.display = 'block';
            const newBodyP = document.createElement('p');
            newBodyP.className = 'body';
            newBodyP.innerText = updatedText;
            postDiv.replaceChild(newBodyP, textarea);
            saveButton.remove();
        })
    };
};
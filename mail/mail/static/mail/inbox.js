document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = function() {
    sendEmail();
    return false;
}; 

  // By default, load the inbox
  load_mailbox('inbox');


});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#inside-email').style.display = 'none';
  

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#inside-email').style.display = 'none';
  
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  // Fetch emails for the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
          const emailDiv = document.createElement('div');
          emailDiv.innerHTML = `<div class="sent-text"><span class="sender">${email.sender}</span> <span class="subject"> ${email.subject}</span> <span class="sendtime">${email.timestamp}</span></div>`;
          if (email.read) {
            emailDiv.style.backgroundColor = 'rgb(238, 238, 238)';
        } else {
            emailDiv.style.backgroundColor = 'white';
        }
        // the code 'email.id' and 'email_id' was through the help of cs50 ai and helping me i should use more then just email_id and the difference between them.
          emailDiv.addEventListener('click', () => inmail(email.id, mailbox));
          document.querySelector('#emails-view').append(emailDiv);
      });
  });
}

function sendEmail() {
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    // Load the sent mailbox
    load_mailbox('sent');
  });
}

function recieveEmail() {

  fetch('/emails/inbox')
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      load_mailbox('inbox');

      // ... do something else with emails ...
  });   
  }

  function inmail(email_id, mailbox) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#inside-email').style.display = 'block';
  
    fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    
    console.log(email);

    let = buttonText = '';
    if (email.archived) {
      buttonText = 'Unarchive';
    } else {
      buttonText = 'Archive';
    }
    let reply = 'Reply';
    document.querySelector('#inside-email').innerHTML = `
    <h3>${email.subject}</h3>
    <p><strong>From:</strong> ${email.sender}</p>
    <p><strong>To:</strong> ${email.recipients}</p>
    <p><strong>Timestamp:</strong> ${email.timestamp}</p>
    <hr>
    <p class="email-body">${email.body}</p>
  `;
  // finding out that needing setTimeout to make my code work was because of cs50 ai, just the word setTimeout and 0, nothing more in these fewlines
  setTimeout(() => {
    document.querySelector('#reply-inmail').addEventListener('click', () => Replying(email));
  }, 0);

  // this two lines || was because of cs50 ai
if (mailbox === 'inbox' || mailbox === 'archive') {
  document.querySelector('#inside-email').innerHTML += `
    <button id="reply-inmail" class="btn btn-sm btn-outline-primary">${reply}</button>
    <button id="archive-inmail" class="btn btn-sm btn-outline-primary">${buttonText}</button>
  `; 

  setTimeout(() => {
    if (email.archived) {
      document.querySelector('#archive-inmail').classList.remove('btn-outline-primary');
      document.querySelector('#archive-inmail').classList.add('btn-outline-danger');
    } else {
      document.querySelector('#archive-inmail').classList.remove('btn-outline-danger');
      document.querySelector('#archive-inmail').classList.add('btn-outline-primary');
    }
  }, 0);

  document.querySelector('#archive-inmail').addEventListener('click', () => {
    inmail(email_id);
    archived(email_id, !email.archived);
  });
}

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
    read: true
    })
    });
  })
}

  function archived(email_id, archive) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: archive
        })
    })
    .then(() => {
        load_mailbox('inbox');
    });
}
  
function Replying(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#inside-email').style.display = 'none';

  document.querySelector('#compose-recipients').value = email.sender;

  let subject = email.subject;
  // ! and startsWith was thanks to cs50 ai, i had the idea, but i couldnt think of something resembling this code
  if (!subject.startsWith("Re:")) {
    subject = "Re: " + subject;
  }
  document.querySelector('#compose-subject').value = subject;

  document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n\n`;
}
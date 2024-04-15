function sleep_1(ms) 
{
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Get references to elements
const messageList = document.querySelector('.table');
const mailItem = document.getElementById('inboxTable');
const messageModal = document.getElementById('message-modal');
const messageContent = document.getElementById('message-content');



const inboxItemHandler = document.querySelector('#inboxItemHandler');

// Function to handle opening the modal
function openModal(messageId) {
//   fetch(`/get_message/${messageId}`)
//     .then(response => response.text())
//     .then(messageText => {
//       messageContent.innerHTML = messageText;
//       messageModal.style.display = 'block';
//     });
    fetch(`/mail/${messageId}`)
            .then(response => response.json())
            .then(data => {
                console.log(messageId)
                document.getElementById('message-from').innerHTML = 'From: ' + data.From;
                document.getElementById('message-date').innerHTML = 'Date: ' + data.Date_n;
                document.getElementById('message-subject').innerHTML = 'Subject: ' + data.Subject;
                document.getElementById('message-content').innerHTML = 'Body: ' + data.Body; // Assuming your message object has a 'content' field
                document.getElementById('message-modal').style.display = 'block';
            })
            .catch(error => console.error('Error fetching message details:', error));


    inboxItemHandler.style.display = 'none';
    messageModal.style.display = 'block';
    messageModal.style.animation =  "swipe-in 1.5s ease"
    // messageContent.innerHTML = messageId;
}

// Function to close the modal
function closeModal() {
  messageModal.style.animation =  "swipe-out 1.5s ease"
  sleep_1(900).then(() => { 
    inboxItemHandler.style.animation =  "show-up 0.9s ease"
    messageModal.style.display = 'none';
    inboxItemHandler.style.display = 'block';
});
  
}

// // (Later) Add event listeners to message anchors
// const messageAnchors = messageList.querySelectorAll('a');
// messageAnchors.forEach(anchor => {
//     anchor.addEventListener('click', (event) => {
//         event.preventDefault(); // Prevent default navigation
//         // const messageId = anchor.dataset.messageId; 
        
//         //testing purpose
//         const messageId = 'x';

//         openModal(messageId);
//     });
// });


document.addEventListener('DOMContentLoaded', function() {
        const messageButtons = document.querySelectorAll('.openMsg');
        messageButtons.forEach(button => {
            button.addEventListener('click', function() {
                const messageId = this.getAttribute('data-message-id');
                console.log(messageId)
                openModal(messageId);
            });
        });
});

function dummyMail(){
    var htmlLine = '<tr class="Inbox_messagesRecieved">' +
                            '<td>' +
                                '<a href="#" class="openMsg">mail </a>' +
                            '</td>' +
                        '</tr>';
    mailItem.innerHTML += htmlLine;
}

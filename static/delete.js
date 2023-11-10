// delete.js file
function confirmDelete(userId) {
    if (window.confirm('Are you sure you want to delete this user?')) {
        // Make an AJAX call to the server
        $.ajax({
            url: '/delete-user', // URL to the Flask route
            type: 'POST',
            data: { user_id: userId }, // Data to be sent to the server
            success: function(response) {
                // This function is called if the server returns a successful response
                if (response.status === 'success') {
                    alert('User deleted successfully.');
                    // Remove the user's row from the HTML table without reloading the page
                    $('#user-row-' + userId).remove(); // Assuming your user rows have IDs like 'user-row-X'
                } else {
                    // If the server response indicates failure, alert the user
                    alert('Error: ' + response.message);
                }
            },
            error: function() {
                // This function is called if the server-side script returned an error
                alert('There was an error deleting the user.');
            }
        });
    }
}

function DeleteChat(chatroomId) {
    if (window.confirm('Are you sure you want to delete this chatroom?')) {
        $.post('/delete-chatroom', { chatroom_id: chatroomId }, function(data) {
            if (data.status === 'success') {
                alert(data.message); // Alert the success message
                // Remove the chatroom from the DOM or update the UI accordingly
                 $('#chatroom-row-' + chatroomId).remove();
            } else {
                alert(data.message); // Alert the failure message
            }
        }, 'json').fail(function() {
            alert('There was an error processing your request.');
        });
    }
}



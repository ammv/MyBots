import emoji

MESSAGES = {
    'start': 
emoji.emojize('''
Hi\! Now I'll teach you how to play the *Stone Game*\\.

Here there are 7 stones :rock:\.
\You can take turns taking 1, 3 or 4 stones\.
The winner is the one who takes the last stone\.
Good luck\!
''', language='alias'),
    'help':
emoji.emojize('''
Here there are 7 stones :rock:
\You can take turns taking 1, 3 or 4 stones\.
The winner is the one who takes the last stone\.

To play with computer tap to: *Computer 🤖*\\
To play with user tap to: *User 👤*\

To return to menu use: /stop

Good luck\!
''', language='alias'),
    'input_stones': {
        'init': 'Enter the initial number of stones \(at least 7\)',
        'input_error': 'Incorrect input, try again',
        'too_much_error': 'You can\'t go like that right now\!'
    },   
    'start_game': {
        'computer': 'You started the game against the computer\!',
        'user': 'You started the game againt the #user#\!'
    },
    'not_state': "We couldn't track where you were before that\. Therefore, we will transfer you to the menu\!",
    'win': {
        'you': 'You win\!',
        'user': '#user# win\!',
        'computer': 'Computer win\!'
    },
    'stop': {
        'user': '#user# have stopped game\!'
    },
    'menu': {
        'input_error': 'Unknown command\! Use the keyboard below\!',
        'back': 'You are moved to the menu\!',
        'back_error': 'You are already on the menu\!'
    },
    'rooms': {
        'help': 'Enter the number of the desired room to enter it and start the game\!',
        'input_title': 'Enter the name of the room \(no more than 16 characters\)',
        'input_title_error': 'If the title is too long or too short, think of another title\!',
        'wait_other_user': 'You have created a room, now wait for another user to come to you\!',
        'room_num_error': 'Invalid room number\!',
        'invalid_room': 'The room no longer exists\!',
        'please_wait': 'Please wait for another user or enter \\stop\!',
        'wait_step': 'Wait for the other user\'s step\!',
        'user_joined': '#user# joined the room\!',
        'you_joined': 'You joined the room\!',
        'user_stop': '#user# stopped the game\!',
        'host_stop': 'host stopped the game\!',
        'first_step': '#user# goes first\!',
        'error_join': 'You can\'t join the room\!',
        'user_play_again': '#user# wants to play again\!'
    }
}

STEPS = {1: emoji.emojize(':one:', language='alias'),
    3: emoji.emojize(':three:', language='alias'),
    4: emoji.emojize(':four:', language='alias')}
    
EMOJI = {v: k for k, v in STEPS.items()}
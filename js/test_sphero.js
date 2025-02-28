const { sendRollCommand, disconnectSphero } = require('./sphero_api');

// Wait for connection, then send a command
setTimeout(() => {
    sendRollCommand(90, 100, 2); // Move forward at speed 100 for 2s
    setTimeout(() => {
        disconnectSphero(); // Disconnect after movement
    }, 3000);
}, 5000);

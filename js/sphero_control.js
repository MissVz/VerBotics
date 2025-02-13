const { scanner } = require('spherov2.js');

const executeCommand = async (command) => {
    const sphero = await scanner.findSpheroMini();
    if (!sphero) {
        console.log("Sphero Mini not found!");
        return;
    }

    const { direction, speed, duration } = command;

    console.log(`Executing: Move ${direction}° at speed ${speed} for ${duration}s`);

    await sphero.rollTime(speed, direction, duration * 1000, []); // Convert seconds to milliseconds
};

// Example command received from GPT-4
const testCommand = {
    "direction": 0,  // Forward (0°)
    "speed": 100,     // Max speed
    "duration": 2     // 2 seconds
};

executeCommand(testCommand);

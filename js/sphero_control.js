// const { scanner } = require('spherov2.js');

// const executeCommand = async (command) => {
//     const sphero = await scanner.findSpheroMini();
//     if (!sphero) {
//         console.log("Sphero Mini not found!");
//         return;
//     }

//     const { direction, speed, duration } = command;

//     console.log(`Executing: Move ${direction}° at speed ${speed} for ${duration}s`);

//     await sphero.rollTime(speed, direction, duration * 1000, []); // Convert seconds to milliseconds
// };

// // Example command received from GPT-4
// const testCommand = {
//     "direction": 0,  // Forward (0°)
//     "speed": 100,     // Max speed
//     "duration": 2     // 2 seconds
// };

// executeCommand(testCommand);

const fs = require('fs');
const path = require('path');
const { scanner } = require('spherov2');

// Define the path to sphero_command.json inside assets folder
const COMMAND_FILE = path.join(__dirname, "..", "assets", "sphero_command.json");

const executeCommand = async () => {
    // Find and connect to Sphero Mini
    const sphero = await scanner.findSpheroMini();
    if (!sphero) {
        console.log("❌ Sphero Mini not found!");
        return;
    }

    try {
        // Read the JSON command file
        const rawData = fs.readFileSync(COMMAND_FILE);
        const command = JSON.parse(rawData);

        // Extract movement parameters
        const { angle, speed, duration } = command.parameters;

        console.log(`🚀 Executing: Move ${angle}° at speed ${speed} for ${duration}s`);

        // Send command to Sphero
        await sphero.rollTime(speed, angle, duration * 1000, []);
        console.log("✅ Command executed successfully!");

    } catch (error) {
        console.error("❌ Error reading or executing Sphero command:", error);
    }
};

// Run the function
executeCommand();
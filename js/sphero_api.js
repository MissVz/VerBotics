const noble = require('noble-winrt');

// Sphero Mini UUIDs (used for communication)
const SPHERO_SERVICE_UUID = '00010001574f4f2053706865726f2121';
const SPHERO_RX_CHAR_UUID = '8667556c-9a37-4c91-84ed-54ee27d90049';  // Write commands to this
const SPHERO_TX_CHAR_UUID = '00010003574f4f2053706865726f2121'; // Read responses from this

let sphero;
let rxCharacteristic;

// Scan and connect to Sphero Mini
noble.on('stateChange', async (state) => {
    if (state === 'poweredOn') {
        console.log('🔍 Scanning for Sphero Mini...');
        setTimeout(() => {
            noble.startScanning([SPHERO_SERVICE_UUID], false);
        }, 3000);  // Wait 3 seconds before scanning       
    } else {
        noble.stopScanning();
    }
});

noble.on('discover', async (peripheral) => {
    console.log(`🔍 Detected Device: ${peripheral.advertisement.localName || 'Unknown'} - ID: ${peripheral.id}`);

    if (!peripheral.advertisement.localName || !peripheral.advertisement.localName.includes('Sphero')) {
        console.log('🔄 Ignoring non-Sphero devices...');
        return;
    }

    console.log(`✅ Found Sphero Mini: ${peripheral.advertisement.localName}`);
    noble.stopScanning();

    peripheral.connect((error) => {
        if (error) {
            console.error('❌ Connection error:', error);
            return;
        }

        console.log('🔗 Connected to Sphero Mini!');

        // Discover services and characteristics
        peripheral.discoverAllServicesAndCharacteristics((err, services, characteristics) => {
            if (err) {
                console.error('❌ Service discovery error:', err);
                return;
            }

            console.log('🔎 Available Services and Characteristics:');
            characteristics.forEach((char) => {
                console.log(`🔹 UUID: ${char.uuid}`);
            });

            rxCharacteristic = characteristics.find(c => c.uuid === SPHERO_RX_CHAR_UUID);
            if (!rxCharacteristic) {
                console.error('❌ RX Characteristic not found. Please check UUIDs.');
                return;
            }

            console.log('✅ Ready to send commands!');
            sphero = peripheral;
        });
    });
});

// Function to send a roll command to Sphero
function sendRollCommand(angle, speed, duration) {
    if (!rxCharacteristic) {
        console.error('❌ Sphero Mini not ready for commands.');
        return;
    }

    // Construct roll command (hex format)
    const rollCommand = Buffer.from([
        0x8D, 0x0D, 0x00, 0x00, angle, speed, 0x00, 0x00, duration, 0x00
    ]);

    console.log(`🚀 Sending: Roll ${angle}° at speed ${speed} for ${duration}s`);

    rxCharacteristic.write(rollCommand, false, (err) => {
        if (err) {
            console.error('❌ Error sending command:', err);
        } else {
            console.log('✅ Command sent successfully!');
        }
    });
}

// Function to disconnect
function disconnectSphero() {
    if (sphero) {
        sphero.disconnect((err) => {
            if (err) {
                console.error('❌ Error disconnecting:', err);
            } else {
                console.log('🔌 Sphero Mini disconnected.');
            }
        });
    }
}

// Export functions
module.exports = { sendRollCommand, disconnectSphero };

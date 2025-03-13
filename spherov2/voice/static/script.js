let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const statusDiv = document.getElementById('status');
const transcribedTextElem = document.getElementById('transcribedText');
const commandOutputElem = document.getElementById('commandOutput');

recordButton.addEventListener('click', async () => {
  // Start recording audio using getUserMedia and MediaRecorder
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      statusDiv.textContent = "Recording...";
      audioChunks = [];
      mediaRecorder.addEventListener('dataavailable', event => {
        audioChunks.push(event.data);
      });
      mediaRecorder.addEventListener('stop', onRecordingStop);
      recordButton.disabled = true;
      stopButton.disabled = false;
    } catch (error) {
      console.error('Error accessing microphone:', error);
      statusDiv.textContent = "Microphone access denied.";
    }
  } else {
    alert("getUserMedia is not supported in your browser.");
  }
});

stopButton.addEventListener('click', () => {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
    statusDiv.textContent = "Processing recording...";
    recordButton.disabled = false;
    stopButton.disabled = true;
  }
});

function onRecordingStop() {
  const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
  // Create a FormData object to send the audio file to your backend
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recorded_audio.wav');

  // Call your backend endpoint (e.g., '/process_audio') to handle transcription and command generation.
  fetch('/process_audio', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // Expected response: { transcription: "spoken text", command: { ... } }
    transcribedTextElem.textContent = data.transcription;
    commandOutputElem.textContent = JSON.stringify(data.command, null, 2);
    statusDiv.textContent = "Done.";
  })
  .catch(error => {
    console.error('Error processing audio:', error);
    statusDiv.textContent = "Error processing audio.";
  });
}
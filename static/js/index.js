// transcription_app/static/transcription_app/js/full-screen-audio-visualizer.js
function FullScreenAudioVisualizer() {
  // Create audio context
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();

  // Create analyzer
  const analyser = audioContext.createAnalyser();
  analyser.fftSize = 256;

  // Create data array for visualization
  const dataArray = new Uint8Array(analyser.frequencyBinCount);

  // Get references to canvas and context
  const canvas = document.getElementById("audioVisualizer");
  const ctx = canvas.getContext("2d");

  this.init = function () {
    // Connect analyzer to microphone source
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        const microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);
      });
  };

  this.start = function () {
    // Start visualizing sound
    analyser.connect(audioContext.destination);
    this.draw();
  };

  this.stop = function () {
    // Stop visualizing sound and clear canvas
    analyser.disconnect();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

  this.draw = function () {
    // Get frequency data
    analyser.getByteFrequencyData(dataArray);

    // Clear canvas and set fill style
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "rgba(255, 255, 255, 0.2)";

    // Draw bars
    for (let i = 0; i < dataArray.length; i++) {
      const barHeight = dataArray[i] * 2;
      const x = i * 3;
      const y = canvas.height - barHeight;
      ctx.fillRect(x, y, 2, barHeight);
    }

    // Request next frame for animation
    requestAnimationFrame(this.draw.bind(this));
  };
}

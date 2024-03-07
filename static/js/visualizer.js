// transcription_app/static/transcription_app/js/visualizer.js
function FullScreenAudioVisualizer() {
    var audioContext = new (window.AudioContext || window.webkitAudioContext)();
    var analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    var dataArray = new Uint8Array(analyser.frequencyBinCount);
    var canvas = document.getElementById("audioVisualizer");
    var ctx = canvas.getContext("2d");

    this.init = function() {
        // Connect analyser to the microphone source
        navigator.mediaDevices.getUserMedia({ audio: true }).then(function(stream) {
            var microphone = audioContext.createMediaStreamSource(stream);
            microphone.connect(analyser);
        });
    };

    this.start = function() {
        // Start visualizing sound
        analyser.connect(audioContext.destination);
        this.draw();
    };

    this.stop = function() {
        // Stop visualizing sound
        analyser.disconnect();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    };

    this.draw = function() {
        // Draw the full-screen audio visualizer
        analyser.getByteFrequencyData(dataArray);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgba(33, 150, 243, 0.5)"; // Lighter shade of blue

        for (var i = 0; i < dataArray.length; i++) {
            var barHeight = dataArray[i] / 2;
            var x = i * 4;
            var y = canvas.height - barHeight;

            ctx.fillRect(x, y, 2, barHeight);
        }

        requestAnimationFrame(this.draw.bind(this));
    };
}

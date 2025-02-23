<template>
  <div>
    <video ref="video" autoplay playsinline></video>
    <canvas ref="canvas"></canvas>
    <div v-if="feedback">{{ feedback }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

// Ensure Pose, POSE_CONNECTIONS, Camera, drawConnectors, and drawLandmarks are globally available via the CDN
const { Pose, POSE_CONNECTIONS, Camera, drawConnectors, drawLandmarks } = window;

const route = useRoute();
const selectedExercise = ref(route.query.exercise || "squat");
const video = ref(null);
const canvas = ref(null);
const feedback = ref("");
let socket = null;

const loadVideo = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: true,
  });
  video.value.srcObject = stream;
  return new Promise((resolve) => {
    video.value.onloadedmetadata = () => {
      resolve(video.value);
    };
  });
};

const startDetection = async () => {
  socket = new WebSocket(`ws://127.0.0.1:8001/api/video/ws/exercise-detection/?exercise_type=${selectedExercise.value}`);

  socket.onopen = () => {
    console.log("WebSocket connection established");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received feedback:", data);
    feedback.value = data.feedback;
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed. Reconnecting...");
    setTimeout(startDetection, 1000); // Reconnect after 1 second
  };

  const pose = new Pose({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
  });

  pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: true,
    smoothSegmentation: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
  });

  pose.onResults(onResults);

  const camera = new Camera(video.value, {
    onFrame: async () => {
      await pose.send({ image: video.value });
    },
    width: 640,
    height: 480,
  });
  camera.start();
};

const onResults = (results) => {
  const ctx = canvas.value.getContext("2d");
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);
  ctx.drawImage(results.image, 0, 0, canvas.value.width, canvas.value.height);

  if (results.poseLandmarks) {
    drawConnectors(ctx, results.poseLandmarks, POSE_CONNECTIONS, {
      color: "#00FF00",
      lineWidth: 4,
    });
    drawLandmarks(ctx, results.poseLandmarks, {
      color: "#FF0000",
      lineWidth: 2,
    });

    // Draw feedback text on the canvas
    ctx.font = "20px Arial";
    ctx.fillStyle = "red";
    ctx.fillText(feedback.value, 10, 30);

    // Send the frame to the server for processing
    if (socket.readyState === WebSocket.OPEN) {
      const frame = canvas.value.toDataURL('image/jpeg');
      console.log("Sending frame:", frame); // Debugging statement
      socket.send(frame);
    }
  }
};

onMounted(async () => {
  await loadVideo();
  startDetection();
});
</script>

<style scoped>
video, canvas {
  position: absolute;
  top: 0;
  left: 0;
}
</style>
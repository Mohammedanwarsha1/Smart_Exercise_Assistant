<script setup>
/*
import { ref } from "vue";
import { useRouter } from "vue-router";

const EXERCISES = ["squat", "plank", "bicep_curl", "lunge"];
const selectedExercise = ref(EXERCISES[0]);
const router = useRouter();

const startDetection = () => {
  router.push({ name: "Webcam", query: { exercise: selectedExercise.value } });
};
*/
/*

import { ref } from "vue";

const EXERCISES = ["squat", "plank", "bicep_curl", "lunge"];
const selectedExercise = ref(EXERCISES[0]);

const startDetection = () => {
  // Redirect to Flask (localhost:5000) with selected exercise
  window.location.href = "http://localhost:5000";
};
*/
import { onMounted } from "vue";

onMounted(() => {
  window.location.href = "http://localhost:5000"; // Auto-redirect on component load
},500);



</script>



<template>
  <div>
     
  </div>
</template>

<style scoped>
/* Add your styles here */
</style>

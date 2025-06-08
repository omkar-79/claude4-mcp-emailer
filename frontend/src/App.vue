<script setup lang="ts">
import CsvUploader from './components/CsvUploader.vue'
</script>

<template>
  <div class="app">
    <h1>CSV File Uploader</h1>
    <CsvUploader />
  </div>
</template>

<style scoped>
.app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
}
</style>

<template>
  <div class="test-connection">
    <h2>Test Backend Connection</h2>
    <button @click="testConnection" class="test-button">
      Test Connection
    </button>
    <div v-if="message" class="message" :class="{ 'error': isError }">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const message = ref('')
const isError = ref(false)

const testConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/test', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    message.value = data.message
    isError.value = false
  } catch (error) {
    message.value = 'Error connecting to backend: ' + error.message
    isError.value = true
  }
}
</script>

<style scoped>
.test-connection {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.test-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin: 20px 0;
}

.test-button:hover {
  background-color: #45a049;
}

.message {
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
  background-color: #e8f5e9;
  color: #2e7d32;
}

.message.error {
  background-color: #ffebee;
  color: #c62828;
}
</style> 
<template>
  <div class="api-examples">
    <h2>API Request Examples</h2>
    
    <!-- GET Request Example -->
    <div class="example-section">
      <h3>1. Simple GET Request</h3>
      <button @click="makeGetRequest" class="api-button">Test GET</button>
      <div v-if="getResponse" class="response">
        {{ getResponse }}
      </div>
    </div>

    <!-- GET with Parameters -->
    <div class="example-section">
      <h3>2. GET with Parameters</h3>
      <input v-model="name" placeholder="Enter name" class="input-field" />
      <input v-model="age" type="number" placeholder="Enter age" class="input-field" />
      <button @click="makeGetWithParams" class="api-button">Greet User</button>
      <div v-if="getParamsResponse" class="response">
        {{ getParamsResponse }}
      </div>
    </div>

    <!-- POST Request Example -->
    <div class="example-section">
      <h3>3. POST Request</h3>
      <input v-model="messageContent" placeholder="Enter message" class="input-field" />
      <input v-model="priority" type="number" placeholder="Priority (1-5)" class="input-field" />
      <button @click="makePostRequest" class="api-button">Send Message</button>
      <div v-if="postResponse" class="response">
        {{ postResponse }}
      </div>
    </div>

    <!-- Headers Example -->
    <div class="example-section">
      <h3>4. Check Headers</h3>
      <button @click="checkHeaders" class="api-button">Check Headers</button>
      <div v-if="headersResponse" class="response">
        {{ headersResponse }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// State variables
const getResponse = ref('')
const getParamsResponse = ref('')
const postResponse = ref('')
const headersResponse = ref('')
const name = ref('')
const age = ref('')
const messageContent = ref('')
const priority = ref(1)

// API base URL
const API_URL = 'http://localhost:8000/api'

// 1. Simple GET request
const makeGetRequest = async () => {
  try {
    const response = await fetch(`${API_URL}/test`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
    const data = await response.json()
    getResponse.value = data
  } catch (error) {
    getResponse.value = { error: error.message }
  }
}

// 2. GET request with parameters
const makeGetWithParams = async () => {
  try {
    const url = new URL(`${API_URL}/greet/${name.value}`)
    if (age.value) {
      url.searchParams.append('age', age.value)
    }
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
    const data = await response.json()
    getParamsResponse.value = data
  } catch (error) {
    getParamsResponse.value = { error: error.message }
  }
}

// 3. POST request
const makePostRequest = async () => {
  try {
    const response = await fetch(`${API_URL}/message`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: messageContent.value,
        priority: parseInt(priority.value) || 1
      })
    })
    const data = await response.json()
    postResponse.value = data
  } catch (error) {
    postResponse.value = { error: error.message }
  }
}

// 4. Check headers
const checkHeaders = async () => {
  try {
    const response = await fetch(`${API_URL}/headers`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    })
    const data = await response.json()
    headersResponse.value = data
  } catch (error) {
    headersResponse.value = { error: error.message }
  }
}
</script>

<style scoped>
.api-examples {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.example-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 30px;
}

h3 {
  color: #42b983;
  margin-bottom: 15px;
}

.api-button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 10px 0;
}

.api-button:hover {
  background-color: #3aa876;
}

.input-field {
  padding: 8px;
  margin: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.response {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-family: monospace;
}
</style> 
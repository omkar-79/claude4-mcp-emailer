<template>
  <div class="main-content">
    <h2 class="text-lg bold mb-2">Create New Campaign</h2>
    <div class="card mb-2" v-if="step === 1">
      <label class="bold mb-1">Upload CSV File</label>
      <input type="file" accept=".csv" @change="onFileChange" class="mb-2" />
      <div v-if="fileName" class="text-sm mb-2">Selected file: {{ fileName }}</div>
      <label class="bold mb-1">Campaign Details</label>
      <textarea v-model="details" rows="4" placeholder="Describe your campaign or the data..." class="mb-2" style="width:100%;"></textarea>
      <button @click="analyze" :disabled="!csvFile || !details.trim() || loading">Analyze</button>
      <div v-if="loading" class="text-sm mt-1">Analyzing with Claude LLM...</div>
      <div v-if="error" class="text-sm mt-1" style="color:#c53030;">{{ error }}</div>
    </div>

    <div v-if="step === 2">
      <div class="card mb-2 analysis-card" v-if="llmResponse">
        <h3 class="bold mb-1">LLM Analysis Summary</h3>
        <div class="llm-response-text">{{ llmResponse }}</div>
      </div>
      <div class="card mb-2">
        <h3 class="bold mb-1 mt-2">Data Summary & Customer Selection</h3>
        <div class="mb-1 text-sm">Total Records: {{ csvRows.length }}</div>
        <div class="mb-2 text-sm">Columns: {{ csvHeaders.join(', ') }}</div>
        <div class="mb-2">
          <label class="bold mb-1">Select customers to generate emails for:</label>
          <table style="width:100%; margin-bottom: 10px;">
            <thead>
              <tr>
                <th>Select</th>
                <th v-for="header in csvHeaders" :key="header">{{ header }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, idx) in csvRows.slice(0, 5)" :key="idx">
                <td><input type="checkbox" v-model="selectedRows" :value="idx" /></td>
                <td v-for="header in csvHeaders" :key="header">{{ row[header] }}</td>
              </tr>
            </tbody>
          </table>
          <button @click="generateEmails" :disabled="selectedRows.length === 0">Generate Emails</button>
        </div>
      </div>
    </div>

    <div class="card" v-if="step === 3">
      <h3 class="bold mb-1">Generated Emails</h3>
      <div v-if="generatedEmails.length === 0" class="text-sm">Generating emails...</div>
      <div v-else>
        <div v-for="(email, idx) in generatedEmails" :key="idx" class="mb-2 p-1" style="background:#f4f7fa; border-radius:6px;">
          <div class="bold mb-1">Customer #{{ idx + 1 }}</div>
          <div class="text-sm">{{ email }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const step = ref(1)
const csvFile = ref<File | null>(null)
const fileName = ref('')
const details = ref('')
const csvHeaders = ref<string[]>([])
const csvRows = ref<any[]>([])
const selectedRows = ref<number[]>([])
const generatedEmails = ref<string[]>([])
const llmResponse = ref('')
const contextId = ref('')
const loading = ref(false)
const error = ref('')
const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

function onFileChange(e: Event) {
  const files = (e.target as HTMLInputElement).files
  if (files && files.length > 0) {
    csvFile.value = files[0]
    fileName.value = files[0].name
    // Parse CSV for preview
    const reader = new FileReader()
    reader.onload = (e) => {
      const text = e.target?.result as string
      const rows = text.split('\n').filter(r => r.trim())
      csvHeaders.value = rows[0].split(',').map(h => h.trim())
      csvRows.value = rows.slice(1).map(row => {
        const values = row.split(',').map(v => v.trim())
        const obj: Record<string, string> = {}
        csvHeaders.value.forEach((h, i) => { obj[h] = values[i] || '' })
        return obj
      })
    }
    reader.readAsText(files[0])
  } else {
    csvFile.value = null
    fileName.value = ''
    csvHeaders.value = []
    csvRows.value = []
  }
}

async function analyze() {
  if (!csvFile.value || !details.value.trim()) return
  loading.value = true
  error.value = ''
  llmResponse.value = ''
  console.log('[DEBUG] Starting LLM analysis request...')
  try {
    const formData = new FormData()
    formData.append('file', csvFile.value)
    formData.append('details', details.value)
    console.log('[DEBUG] Sending request to /api/analyze-campaign/')
    const requestUrl = `${backendUrl}/api/analyze-campaign/`
    console.log('[DEBUG] Full request URL:', requestUrl)
    console.log('[DEBUG] Request payload:', {
      file: csvFile.value.name,
      details: details.value
    })
    const response = await fetch(requestUrl, {
      method: 'POST',
      body: formData
    })
    console.log('[DEBUG] Response status:', response.status)
    if (!response.ok) {
      const err = await response.json().catch(() => ({}))
      console.error('[DEBUG] Error response:', err)
      console.error('[DEBUG] Response headers:', Object.fromEntries(response.headers.entries()))
      throw new Error(err.detail || 'Failed to analyze campaign')
    }
    const data = await response.json()
    console.log('[DEBUG] LLM response data:', data)
    llmResponse.value = data.llm_response
    contextId.value = data.context_id
    step.value = 2
  } catch (err: any) {
    error.value = err.message || 'Failed to analyze campaign.'
    console.error('[DEBUG] Analyze error:', err)
  } finally {
    loading.value = false
    console.log('[DEBUG] LLM analysis request finished.')
  }
}

function generateEmails() {
  // Simulate LLM email generation for selected customers
  generatedEmails.value = selectedRows.value.map(idx =>
    `Hi ${csvRows.value[idx][csvHeaders.value[0]]}, this is your personalized campaign email!`
  )
  step.value = 3
}
</script>

<style scoped>
textarea {
  font-family: inherit;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  padding: 10px;
  margin-bottom: 10px;
  resize: vertical;
}
input[type="file"] {
  margin-bottom: 10px;
}
.analysis-card {
  background: #e6f0fa;
  border-left: 5px solid #3182ce;
}
.llm-response-text {
  color: #2a4365;
  font-size: 1.08rem;
  white-space: pre-line;
}
</style>

<template>
  <div class="main-content">
    <h2 class="text-lg bold mb-2">Create New Campaign</h2>
    
    <!-- Step 1: File Upload & Analysis -->
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

    <!-- Step 2: Analysis Results & Customer ID Column Selection -->
    <div v-if="step === 2">
      <div class="card mb-2 analysis-card" v-if="llmResponse">
        <h3 class="bold mb-1">LLM Analysis Summary</h3>
        <div class="llm-response-text">{{ llmResponse }}</div>
      </div>
      
      <div class="card mb-2">
        <h3 class="bold mb-1">Select Customer ID Column</h3>
        <div class="mb-1 text-sm">Total Records: {{ csvRows.length }}</div>
        <div class="mb-2 text-sm">Available Columns: {{ csvHeaders.join(', ') }}</div>
        
        <label class="bold mb-1">Which column contains the Customer ID?</label>
        <select v-model="selectedIdColumn" class="mb-2" style="width:100%; padding:8px; border-radius:6px; border:1px solid #cbd5e1;">
          <option value="">-- Select Customer ID Column --</option>
          <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
        </select>
        
        <button @click="proceedToCustomerSelection" :disabled="!selectedIdColumn">Continue to Customer Selection</button>
      </div>
    </div>

    <!-- Step 3: Customer Selection -->
    <div v-if="step === 3">
      <div class="card mb-2">
        <h3 class="bold mb-1">Select Customers for Email Generation</h3>
        <div class="mb-2 text-sm">Select customers to generate personalized marketing emails:</div>
        
        <div class="customer-list mb-2" style="max-height: 400px; overflow-y: auto;">
          <div v-for="(row, idx) in csvRows" :key="idx" class="customer-item mb-1 p-2" style="background:#f8f9fa; border-radius:4px; border:1px solid #e9ecef;">
            <label style="display:flex; align-items:center; cursor:pointer;">
              <input type="checkbox" v-model="selectedCustomers" :value="idx" style="margin-right:10px;" />
              <div>
                <strong>{{ selectedIdColumn }}: {{ row[selectedIdColumn] }}</strong>
                <div class="text-sm" style="color:#6c757d;">
                  {{ Object.entries(row).slice(0, 3).map(([k, v]) => `${k}: ${v}`).join(' | ') }}
                  <span v-if="csvHeaders.length > 3">...</span>
                </div>
              </div>
            </label>
          </div>
        </div>
        
        <div class="mb-2">
          <button @click="selectAll" class="mr-1">Select All</button>
          <button @click="clearSelection">Clear Selection</button>
        </div>
        
        <div class="mb-2 text-sm">Selected: {{ selectedCustomers.length }} customers</div>
        <button @click="generateEmails" :disabled="selectedCustomers.length === 0 || generatingEmails">
          {{ generatingEmails ? 'Generating Emails...' : 'Generate Marketing Emails' }}
        </button>
      </div>
    </div>

    <!-- Step 4: Generated Emails -->
    <div class="card" v-if="step === 4">
      <h3 class="bold mb-1">Generated Marketing Emails</h3>
      <div v-if="generatedEmails.length === 0" class="text-sm">Generating personalized emails...</div>
      <div v-else>
        <div class="mb-2 text-sm">{{ generatedEmails.length }} emails generated successfully!</div>
        <div v-for="(email, idx) in generatedEmails" :key="idx" class="email-card mb-2 p-2" style="background:#f4f7fa; border-radius:6px; border:1px solid #e2e8f0;">
          <div class="bold mb-1" style="color:#2d3748;">
            Customer: {{ email.customer_id }}
          </div>
          <div class="email-content" style="white-space: pre-line; color:#4a5568;">{{ email.content }}</div>
        </div>
        <button @click="resetCampaign" class="mt-2">Create New Campaign</button>
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
const selectedIdColumn = ref('')
const selectedCustomers = ref<number[]>([])
const generatedEmails = ref<any[]>([])
const llmResponse = ref('')
const contextId = ref('')
const loading = ref(false)
const generatingEmails = ref(false)
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

function proceedToCustomerSelection() {
  if (!selectedIdColumn.value) return
  step.value = 3
}

function selectAll() {
  selectedCustomers.value = csvRows.value.map((_, idx) => idx)
}

function clearSelection() {
  selectedCustomers.value = []
}

async function generateEmails() {
  if (selectedCustomers.value.length === 0) return
  
  generatingEmails.value = true
  error.value = ''
  console.log('[DEBUG] Starting email generation...')
  
  try {
    // Prepare selected customer data
    const selectedCustomerData = selectedCustomers.value.map(idx => csvRows.value[idx])
    
    const payload = {
      customers: selectedCustomerData,
      headers: csvHeaders.value,
      customer_id_column: selectedIdColumn.value,
      campaign_details: details.value,
      context_id: contextId.value
    }
    
    console.log('[DEBUG] Email generation payload:', payload)
    
    const response = await fetch(`${backendUrl}/api/generate-emails/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    
    console.log('[DEBUG] Email generation response status:', response.status)
    
    if (!response.ok) {
      const err = await response.json().catch(() => ({}))
      console.error('[DEBUG] Email generation error response:', err)
      throw new Error(err.detail || 'Failed to generate emails')
    }
    
    const data = await response.json()
    console.log('[DEBUG] Email generation response data:', data)
    
    generatedEmails.value = data.emails
    step.value = 4
    
  } catch (err: any) {
    error.value = err.message || 'Failed to generate emails.'
    console.error('[DEBUG] Email generation error:', err)
  } finally {
    generatingEmails.value = false
  }
}

function resetCampaign() {
  step.value = 1
  csvFile.value = null
  fileName.value = ''
  details.value = ''
  csvHeaders.value = []
  csvRows.value = []
  selectedIdColumn.value = ''
  selectedCustomers.value = []
  generatedEmails.value = []
  llmResponse.value = ''
  contextId.value = ''
  error.value = ''
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

.customer-item:hover {
  background: #e9ecef !important;
}

.email-card {
  border-left: 4px solid #38a169;
}

.email-content {
  font-size: 0.95rem;
  line-height: 1.5;
}

.mr-1 {
  margin-right: 8px;
}

.mt-2 {
  margin-top: 16px;
}
</style>

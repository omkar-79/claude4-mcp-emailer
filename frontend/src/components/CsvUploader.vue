<template>
  <div class="csv-uploader">
    <div class="upload-section">
      <div class="file-input-container">
        <label for="csv-file" class="file-label">
          <span class="file-icon">📁</span>
          Choose CSV File
        </label>
        <input
          id="csv-file"
          type="file"
          accept=".csv"
          @change="handleFileUpload"
          class="file-input"
        />
        <span v-if="selectedFile" class="file-name">{{ selectedFile.name }}</span>
      </div>
      <button @click="uploadFile" class="upload-button" :disabled="!selectedFile">
        Upload CSV
      </button>
    </div>

    <div v-if="csvData.length > 0" class="data-analysis-section">
      <div class="data-details">
        <h3>Data Analysis Details</h3>
        <div class="details-container">
          <textarea
            v-model="dataDetails"
            placeholder="Please provide details about your customer data. Like what the attributes mean and what the data is about."
            class="details-textarea"
            rows="6"
          ></textarea>
          <div class="data-summary">
            <h4>Data Summary</h4>
            <p>Total Records: {{ csvData.length }}</p>
            <p>Columns: {{ headers.join(', ') }}</p>
          </div>
        </div>
        <button 
          @click="analyzeData" 
          class="analyze-button"
          :disabled="!dataDetails.trim()"
        >
          Analyze Data
        </button>
      </div>

      <div class="table-container">
        <h3>Preview Data</h3>
        <table>
          <thead>
            <tr>
              <th v-for="header in headers" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in csvData.slice(0, 5)" :key="index">
              <td v-for="header in headers" :key="header">{{ row[header] }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="csvData.length > 5" class="preview-note">
          Showing first 5 rows of {{ csvData.length }} total records
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const csvData = ref<any[]>([])
const headers = ref<string[]>([])
const selectedFile = ref<File | null>(null)
const dataDetails = ref('')

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

const uploadFile = () => {
  if (!selectedFile.value) {
    alert('Please select a CSV file first')
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target?.result as string
    const rows = text.split('\n')
    
    // Get headers from first row
    headers.value = rows[0].split(',').map(header => header.trim())
    
    // Process data rows
    csvData.value = rows.slice(1).map(row => {
      const values = row.split(',').map(value => value.trim())
      const rowData: { [key: string]: string } = {}
      headers.value.forEach((header, index) => {
        rowData[header] = values[index] || ''
      })
      return rowData
    })
  }
  
  reader.readAsText(selectedFile.value)
}

const analyzeData = () => {
  // This function will be implemented later to handle the actual analysis
  console.log('Analysis requested with details:', dataDetails.value)
  console.log('Data to analyze:', csvData.value)
}
</script>

<style scoped>
.csv-uploader {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.upload-section {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.file-input-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.file-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.file-label:hover {
  background-color: #e0e0e0;
}

.file-icon {
  font-size: 1.2em;
}

.file-input {
  display: none;
}

.file-name {
  color: #666;
  font-size: 0.9em;
}

.upload-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.upload-button:hover:not(:disabled) {
  background-color: #45a049;
}

.upload-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.data-analysis-section {
  margin-top: 30px;
}

.data-details {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.details-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.details-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
  font-size: 0.9em;
}

.data-summary {
  background-color: white;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.data-summary h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.data-summary p {
  margin: 5px 0;
  color: #666;
}

.analyze-button {
  padding: 12px 24px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.analyze-button:hover:not(:disabled) {
  background-color: #1976D2;
}

.analyze-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.table-container {
  overflow-x: auto;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f5f5f5;
}

.preview-note {
  margin-top: 10px;
  color: #666;
  font-style: italic;
  text-align: center;
}

@media (max-width: 768px) {
  .details-container {
    grid-template-columns: 1fr;
  }
  
  .upload-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .file-input-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .upload-button {
    width: 100%;
  }
}
</style> 
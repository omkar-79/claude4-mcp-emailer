<template>
  <div class="main-content">
    <div class="mb-2">
      <h2 class="text-lg bold mb-1">Account Information</h2>
    </div>
    <div class="card mb-2">
      <div class="mb-1"><span class="bold">Username:</span> <span>{{ user?.username }}</span></div>
      <div class="mb-1"><span class="bold">Email:</span> <span>{{ user?.email }}</span></div>
      <div><span class="bold">Member Since:</span> <span>{{ user?.created_at ? user.created_at.split('T')[0] : '' }}</span></div>
    </div>
    <div class="card">
      <h3 class="bold mb-1">Change Password</h3>
      <form @submit.prevent="handleChangePassword">
        <div class="mb-1">
          <label for="currentPassword">Current Password</label>
          <input id="currentPassword" v-model="currentPassword" type="password" required />
        </div>
        <div class="mb-1">
          <label for="newPassword">New Password</label>
          <input id="newPassword" v-model="newPassword" type="password" required />
        </div>
        <div class="mb-1">
          <label for="confirmPassword">Confirm New Password</label>
          <input id="confirmPassword" v-model="confirmPassword" type="password" required />
        </div>
        <button type="submit" class="mb-1">Change Password</button>
      </form>
      <div v-if="error" class="text-sm">{{ error }}</div>
      <div v-if="success" class="text-sm">{{ success }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const error = ref('')
const success = ref('')

onMounted(() => {
  const userData = sessionStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  } else {
    router.push('/login')
  }
})

const handleChangePassword = () => {
  if (newPassword.value !== confirmPassword.value) {
    error.value = 'New passwords do not match.'
    success.value = ''
    return
  }
  // Simulate password change
  setTimeout(() => {
    error.value = ''
    success.value = 'Password changed successfully!'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  }, 1000)
}
</script>

<style scoped>
</style> 
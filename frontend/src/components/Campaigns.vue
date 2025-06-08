<template>
  <div class="main-content">
    <div class="mb-2">
      <h2 class="text-lg bold mb-1">Email Campaigns</h2>
      <router-link to="/new-campaign">
        <button class="mb-1">+ Create New Campaign</button>
      </router-link>
    </div>
    <div class="card">
      <p class="text-sm">No campaigns yet. Start by creating a new campaign!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)

onMounted(() => {
  const userData = sessionStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
</style> 
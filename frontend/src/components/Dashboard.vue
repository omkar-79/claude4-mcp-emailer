<template>
  <div class="main-content">
    <div class="mb-2">
      <h2 class="text-lg bold mb-1">Welcome, {{ user?.username }}!</h2>
      <p class="text-md">Manage your email campaigns</p>
    </div>

    <div class="card mb-2">
      <h3 class="bold mb-1">Quick Actions</h3>
      <router-link to="/newcampaign">
        <button class="mb-1">+ Create New Campaign</button>
      </router-link>
      
    </div>
    <div class="card">
      <h3 class="bold mb-1">Recent Activity</h3>
      <p class="text-sm">No recent activity</p>
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
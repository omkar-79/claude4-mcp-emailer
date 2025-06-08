<template>
  <div class="campaigns">
    <nav class="navbar">
      <div class="navbar-brand">
        <h1>Email Campaign Manager</h1>
      </div>
      <div class="navbar-menu">
        <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
        <router-link to="/campaigns" class="nav-item">Campaigns</router-link>
        <div class="nav-item dropdown">
          <button class="dropdown-trigger">
            {{ user?.username }}
            <span class="dropdown-arrow">▼</span>
          </button>
          <div class="dropdown-menu">
            <router-link to="/profile" class="dropdown-item">Profile</router-link>
            <button @click="handleLogout" class="dropdown-item">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <div class="campaigns-header">
        <h2>Email Campaigns</h2>
        <button class="create-button">
          <span class="icon">+</span>
          Create New Campaign
        </button>
      </div>

      <div class="campaigns-grid">
        <div class="empty-state">
          <p>No campaigns yet. Create your first campaign to get started!</p>
        </div>
      </div>
    </main>
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

const handleLogout = () => {
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.campaigns {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.navbar {
  background-color: #ffffff;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-item {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: #f5f7fa;
}

.dropdown {
  position: relative;
}

.dropdown-trigger {
  background: none;
  border: none;
  color: #2c3e50;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
}

.dropdown-arrow {
  font-size: 0.8rem;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: none;
  min-width: 150px;
}

.dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown-item {
  display: block;
  padding: 0.75rem 1rem;
  color: #2c3e50;
  text-decoration: none;
  transition: background-color 0.3s;
}

.dropdown-item:hover {
  background-color: #f5f7fa;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.campaigns-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.campaigns-header h2 {
  margin: 0;
  color: #2c3e50;
}

.create-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #3aa876;
}

.icon {
  font-size: 1.2rem;
}

.campaigns-grid {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  text-align: center;
  color: #666;
}

.empty-state p {
  margin: 0;
  font-size: 1.1rem;
}
</style> 
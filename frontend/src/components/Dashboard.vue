<template>
  <div class="dashboard">
    <!-- Navbar -->
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

    <!-- Main Content -->
    <main class="main-content">
      <div class="dashboard-header">
        <h2>Welcome, {{ user?.username }}!</h2>
        <p>Manage your email campaigns and track their performance.</p>
      </div>

      <div class="dashboard-grid">
        <!-- Quick Stats -->
        <div class="stats-card">
          <h3>Campaign Stats</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-value">0</span>
              <span class="stat-label">Active Campaigns</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">0</span>
              <span class="stat-label">Total Recipients</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">0%</span>
              <span class="stat-label">Avg. Open Rate</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="actions-card">
          <h3>Quick Actions</h3>
          <div class="action-buttons">
            <button class="action-button primary">
              <span class="icon">+</span>
              Create New Campaign
            </button>
            <button class="action-button secondary">
              <span class="icon">📊</span>
              View Analytics
            </button>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="activity-card">
          <h3>Recent Activity</h3>
          <div class="activity-list">
            <p class="empty-state">No recent activity</p>
          </div>
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
.dashboard {
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

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h2 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.dashboard-header p {
  color: #666;
  margin: 0;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.stats-card,
.actions-card,
.activity-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-card h3,
.actions-card h3,
.activity-card h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #42b983;
}

.stat-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.25rem;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-button.primary {
  background-color: #42b983;
  color: white;
}

.action-button.primary:hover {
  background-color: #3aa876;
}

.action-button.secondary {
  background-color: #f5f7fa;
  color: #2c3e50;
}

.action-button.secondary:hover {
  background-color: #e4e7eb;
}

.icon {
  font-size: 1.2rem;
}

.activity-list {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  color: #666;
  font-style: italic;
}
</style> 
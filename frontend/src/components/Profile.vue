<template>
  <div class="profile">
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
      <div class="profile-container">
        <h2>Profile Settings</h2>
        
        <div class="profile-section">
          <h3>Account Information</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Username</label>
              <p>{{ user?.username }}</p>
            </div>
            <div class="info-item">
              <label>Email</label>
              <p>{{ user?.email }}</p>
            </div>
            <div class="info-item">
              <label>Member Since</label>
              <p>{{ formatDate(user?.created_at) }}</p>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <h3>Change Password</h3>
          <form @submit.prevent="handlePasswordChange" class="password-form">
            <div class="form-group">
              <label for="current-password">Current Password</label>
              <input
                id="current-password"
                v-model="passwordForm.currentPassword"
                type="password"
                required
              />
            </div>
            <div class="form-group">
              <label for="new-password">New Password</label>
              <input
                id="new-password"
                v-model="passwordForm.newPassword"
                type="password"
                required
              />
            </div>
            <div class="form-group">
              <label for="confirm-password">Confirm New Password</label>
              <input
                id="confirm-password"
                v-model="passwordForm.confirmPassword"
                type="password"
                required
              />
            </div>
            <button type="submit" class="submit-button">Update Password</button>
          </form>
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
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

onMounted(() => {
  const userData = sessionStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  } else {
    router.push('/login')
  }
})

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const handlePasswordChange = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('New passwords do not match')
    return
  }
  
  // TODO: Implement password change functionality
  alert('Password change functionality to be implemented')
}

const handleLogout = () => {
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.profile {
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
  max-width: 800px;
  margin: 0 auto;
}

.profile-container {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-container h2 {
  color: #2c3e50;
  margin: 0 0 2rem 0;
}

.profile-section {
  margin-bottom: 2rem;
}

.profile-section h3 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-item label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.info-item p {
  margin: 0;
  color: #2c3e50;
  font-weight: 500;
}

.password-form {
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #3aa876;
}
</style> 
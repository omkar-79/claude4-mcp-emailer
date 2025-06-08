<template>
  <div class="page">
    <nav class="navbar">
      <div class="navbar-content">
        <router-link to="/" class="navbar-logo">

          <span class="navbar-title">Email Buddy AI</span>
        </router-link>
        <div class="navbar-links">
          <router-link to="/dashboard" class="navbar-link">Dashboard</router-link>
          <router-link to="/campaigns" class="navbar-link">Campaigns</router-link>
          <router-link to="/profile" class="navbar-link">Profile</router-link>
          <button @click="handleLogout" class="navbar-btn">Logout</button>
        </div>
      </div>
    </nav>
    <main class="main-content container">
      <slot></slot>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isMobileMenuOpen = ref(false)

const isAuthenticated = computed(() => {
  return !!sessionStorage.getItem('token')
})

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const handleLogout = () => {
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  width: 100%;
  background: linear-gradient(270deg, #3182ce, #63b3ed, #3182ce);
  background-size: 600% 600%;
  animation: gradientMove 8s ease infinite;
  box-shadow: 0 2px 12px rgba(44, 62, 80, 0.07);
  padding: 0;
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
}

.navbar-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.logo-img {
  height: 38px;
  width: 38px;
  margin-right: 12px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(49, 130, 206, 0.08);
}

.navbar-title {
  color: #fff;
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 18px;
}

.navbar-link {
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  padding: 8px 14px;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
}

.navbar-link:hover {
  background: rgba(255,255,255,0.13);
  color: #e3e8ee;
}

.navbar-btn {
  background: #fff;
  color: #3182ce;
  border: none;
  border-radius: 6px;
  padding: 8px 18px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-left: 10px;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 4px rgba(49, 130, 206, 0.08);
}

.navbar-btn:hover {
  background: #3182ce;
  color: #fff;
}

.main-content {
  flex: 1;
  width: 100%;
  padding: var(--spacing-xl) 0;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .mobile-menu-button {
    display: flex;
  }
  .nav-links {
    display: none;
  }
  .nav-links.mobile-menu {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--surface-color);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-md);
    z-index: 1000;
  }
  .nav-links.mobile-menu .nav-link {
    padding: var(--spacing-md);
    width: 100%;
    text-align: center;
  }
  .nav-links.mobile-menu .btn {
    width: 100%;
    margin-top: var(--spacing-sm);
  }
  .main-content {
    padding: var(--spacing-md) 0;
  }
}
</style> 
<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>{{ isLogin ? 'Login' : 'Sign Up' }}</h2>
      
      <!-- Error message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Success message -->
      <div v-if="success" class="success-message">
        {{ success }}
      </div>

      <!-- Login Form -->
      <form v-if="isLogin" @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="loginForm.username"
            type="text"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="loginForm.password"
            type="password"
            required
            class="form-input"
          />
        </div>
        <button type="submit" class="auth-button">Login</button>
      </form>

      <!-- Signup Form -->
      <form v-else @submit.prevent="handleSignup" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="signupForm.email"
            type="email"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label for="signup-username">Username</label>
          <input
            id="signup-username"
            v-model="signupForm.username"
            type="text"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label for="signup-password">Password</label>
          <input
            id="signup-password"
            v-model="signupForm.password"
            type="password"
            required
            class="form-input"
          />
        </div>
        <button type="submit" class="auth-button">Sign Up</button>
      </form>

      <!-- Toggle between login and signup -->
      <p class="toggle-text">
        {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
        <a href="#" @click.prevent="toggleAuth" class="toggle-link">
          {{ isLogin ? 'Sign Up' : 'Login' }}
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLogin = ref(true)
const error = ref('')
const success = ref('')

const loginForm = reactive({
  username: '',
  password: ''
})

const signupForm = reactive({
  email: '',
  username: '',
  password: ''
})

const toggleAuth = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  success.value = ''
}

const handleLogin = async () => {
  try {
    const formData = new FormData()
    formData.append('username', loginForm.username)
    formData.append('password', loginForm.password)

    const response = await fetch('http://localhost:8000/api/token', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('Login failed')
    }

    const data = await response.json()
    sessionStorage.setItem('token', data.access_token)

    // Get user info
    const userResponse = await fetch('http://localhost:8000/api/users/me', {
      headers: {
        'Authorization': `Bearer ${data.access_token}`
      }
    })
    const userData = await userResponse.json()
    sessionStorage.setItem('user', JSON.stringify(userData))

    success.value = 'Login successful!'
    error.value = ''

    // Clear form
    loginForm.username = ''
    loginForm.password = ''

    // Redirect to dashboard
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Invalid username or password'
    success.value = ''
  }
}

const handleSignup = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(signupForm)
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Signup failed')
    }

    success.value = 'Signup successful! Please login.'
    error.value = ''
    signupForm.email = ''
    signupForm.username = ''
    signupForm.password = ''
    isLogin.value = true
  } catch (err) {
    console.error('Signup error:', err)
    error.value = err.message || 'Failed to sign up. Please try again.'
    success.value = ''
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.auth-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.auth-button {
  background-color: #42b983;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.auth-button:hover {
  background-color: #3aa876;
}

.toggle-text {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.toggle-link {
  color: #42b983;
  text-decoration: none;
}

.toggle-link:hover {
  text-decoration: underline;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.success-message {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style> 
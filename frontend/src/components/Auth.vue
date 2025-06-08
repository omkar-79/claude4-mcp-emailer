<template>
  <div class="auth-container">
    <div class="auth-box card">
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
        <button type="submit" class="btn btn-primary">Login</button>
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
        <button type="submit" class="btn btn-primary">Sign Up</button>
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

<script setup lang="ts">
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
  min-height: calc(100vh - 64px);
  padding: var(--spacing-xl);
}

.auth-box {
  width: 100%;
  max-width: 400px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-group label {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  background: #f9fafb;
  transition: border-color 0.2s;
}
.form-input:focus {
  border-color: #3182ce;
  outline: none;
  background: #fff;
}

.btn {
  background: linear-gradient(90deg, #3182ce 0%, #63b3ed 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(49, 130, 206, 0.08);
}
.btn:hover {
  background: linear-gradient(90deg, #2563eb 0%, #4299e1 100%);
}

.toggle-text {
  text-align: center;
  margin-top: var(--spacing-lg);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}
.toggle-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  margin-left: var(--spacing-xs);
}
.toggle-link:hover {
  text-decoration: underline;
}

.error-message {
  background: var(--error-color);
  color: white;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-sm);
}
.success-message {
  background: var(--success-color);
  color: white;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-sm);
}

@media (max-width: 640px) {
  .auth-container {
    padding: var(--spacing-md);
  }
  
  .auth-box {
    padding: var(--spacing-md);
  }
}
</style> 
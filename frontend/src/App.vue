<script setup lang="ts">
import Layout from './components/Layout.vue'
import './assets/global.css'
// The router-view will handle all the routing and component rendering
</script>

<template>
  <Layout>
    <router-view></router-view>
  </Layout>
</template>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.6;
  color: #2c3e50;
}

button {
  font-family: inherit;
}
</style>

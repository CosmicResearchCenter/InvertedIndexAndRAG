<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="container">
    <nav class="glass-nav">
      <ul>
        <li v-for="(route, index) in [
          { path: '/', icon: 'ChatDotRound', text: '智能问答' },
          { path: '/manager', icon: 'Folder', text: '知识库管理' },
          { path: '/settings', icon: 'Setting', text: '设置' }
        ]" :key="index">
          <RouterLink :to="route.path">
            <el-icon class="nav-icon"><component :is="route.icon" /></el-icon>
            <span>{{ route.text }}</span>
          </RouterLink>
        </li>
      </ul>
    </nav>

    <main>
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%);
}

.glass-nav {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  padding: 1rem;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
  justify-content: center;
  gap: 2rem;
}

li {
  margin: 0 2rem;
}

li a {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #2c3e50;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}

li a:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
  border: 1px solid rgba(82, 156, 255, 0.3);
  box-shadow: 0 4px 20px rgba(82, 156, 255, 0.1);
}

li a.router-link-active {
  background: rgba(82, 156, 255, 0.1);
  border: 1px solid rgba(82, 156, 255, 0.3);
  font-weight: 500;
  color: #409EFF;
  box-shadow: 0 0 20px rgba(82, 156, 255, 0.1);
}

.nav-icon {
  font-size: 1.2em;
  color: #409EFF;
  filter: drop-shadow(0 0 4px rgba(82, 156, 255, 0.3));
}

main {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

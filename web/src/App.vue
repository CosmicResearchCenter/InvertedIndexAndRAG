<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="container">
    <nav>
      <ul>
        <li>
          <RouterLink to="/">
            <el-icon><ChatDotRound /></el-icon>
            智能问答
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/manager">
            <el-icon><Folder /></el-icon>
            知识库管理
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/settings">
            <el-icon><Setting /></el-icon>
            设置
          </RouterLink>
        </li>
      </ul>
    </nav>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh; 
  overflow: hidden;
}

nav {
  background: linear-gradient(to right, #2c3e50, #3498db);
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
  justify-content: center;
}

li {
  margin: 0 2rem;
}

li a {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

li a:hover {
  background: rgba(255,255,255,0.1);
  transform: translateY(-2px);
}

li a.router-link-active {
  background: rgba(255,255,255,0.2);
  font-weight: 500;
}

.el-icon {
  margin-right: 4px;
}

main {
  flex: 1; /* 占据剩余空间 */
  overflow-y: auto; /* 内容溢出时滚动 */
}
</style>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="container">
    <nav>
      <ul>
        <li>
          <RouterLink to="/">智能问答</RouterLink>
        </li>
        <li>
          <RouterLink to="/manager">知识库管理</RouterLink>
        </li>
        <li>
          <RouterLink to="/settings">设置</RouterLink>
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
  background-color: #f5f5f5;
  padding: 1rem;
  border-bottom: 1px solid #ddd;
}

ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin-right: 1rem;
}

li a {
  text-decoration: none;
  color: #333;
}

li a.router-link-active {
  font-weight: bold;
  color: #007bff;
}

main {
  flex: 1; /* 占据剩余空间 */
  overflow-y: auto; /* 内容溢出时滚动 */
}
</style>

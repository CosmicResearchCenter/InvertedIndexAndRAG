<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-content">
        <h2>欢迎登录</h2>
        <div class="form-group">
          <el-input 
            v-model="username" 
            placeholder="用户名" 
            class="input-field"
            :prefix-icon="User"
          />
        </div>
        <div class="form-group">
          <el-input 
            v-model="password" 
            type="password" 
            placeholder="密码" 
            class="input-field"
            :prefix-icon="Lock"
            @keyup.enter="login"
          />
        </div>
        <el-button 
          type="primary" 
          @click="login" 
          class="login-button"
          :loading="loading"
        >
          {{ loading ? '登录中...' : '登 录' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { User, Lock } from '@element-plus/icons-vue'

const username = ref('');
const password = ref('');
const loading = ref(false);
const router = useRouter();

const login = async () => {
  if (!username.value || !password.value) {
    ElMessage.warning('请输入用户名和密码');
    return;
  }
  
  loading.value = true;
  try {
    if (username.value === 'admin' && password.value === 'admin') {
      await new Promise(resolve => setTimeout(resolve, 800)); // 模拟请求延迟
      ElMessage.success('登录成功');
      router.push('/');
    } else {
      ElMessage.error('用户名或密码错误');
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  /* background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); */
  position: relative;
  overflow: hidden;
}

.login-box {
  position: relative;
  margin-top: -200px;
  width: 90%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 2.5rem;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1;
  animation: fadeIn 0.5s ease-out;
}

.login-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

h2 {
  color: #fff;
  font-size: 1.8rem;
  margin: 0 0 1rem;
  text-align: center;
  letter-spacing: 2px;
}

.form-group {
  position: relative;
}

.input-field {
  --el-input-bg-color: rgba(255, 255, 255, 0.1) !important;
  --el-input-text-color: #fff !important;
  --el-input-border-color: rgba(255, 255, 255, 0.2) !important;
  --el-input-hover-border-color: rgba(255, 255, 255, 0.4) !important;
}

.input-field :deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: none;
  border-radius: 12px;
  padding: 8px 15px;
}

.input-field :deep(.el-input__inner) {
  color: #fff;
}

.input-field :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.6);
}

.login-button {
  height: 48px;
  font-size: 1.1rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #00c6fb 0%, #005bea 100%);
  border: none;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 198, 251, 0.4);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-box {
    width: 85%;
    padding: 2rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  .login-button {
    height: 44px;
  }
}

@media (max-width: 480px) {
  .login-box {
    width: 90%;
    padding: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
}
</style>

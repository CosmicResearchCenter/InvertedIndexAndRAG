<template>
  <el-container class="chat-container" :class="{ 'dark-mode': isDarkMode }">
    <!-- 左侧用户列表 -->
    <el-aside class="chat-aside">
      <div class="aside-header">
        <el-input v-model="searchUser" placeholder="搜索用户..." prefix-icon="Search" />
        <el-switch v-model="isDarkMode" class="theme-switch" size="small" />
      </div>
      <div class="user-list custom-scrollbar">
        <div v-for="user in filteredUsers" :key="user.id"
          class="user-item"
          :class="{ active: currentUserId === user.id }"
          @click="handleUserClick(user.id)">
          <el-avatar :size="32" :src="user.avatar">{{ user.username.charAt(0) }}</el-avatar>
          <span class="username">{{ user.username }}</span>
        </div>
      </div>
    </el-aside>

    <!-- 中间对话列表 -->
    <el-main class="chat-main">
      <div v-if="currentUserId" class="conversation-list">
        <div v-for="conv in userConversations" :key="conv.id"
          class="conversation-item"
          :class="{ active: currentConvId === conv.id }"
          @click="handleConversationClick(conv.id)">
          <div class="conv-title">{{ conv.title }}</div>
          <div class="conv-time">{{ formatDate(conv.created_at) }}</div>
        </div>
      </div>
      <div v-else class="no-selection">
        请选择用户查看对话记录
      </div>
    </el-main>

    <!-- 右侧聊天记录 -->
    <el-aside class="chat-aside-right">
      <div v-if="currentConvId" class="message-list">
        <div v-for="msg in conversationMessages" :key="msg.id" class="message-item"
          :class="{ 'user-message': msg.role === 'user', 'assistant-message': msg.role === 'assistant' }">
          <div class="message-header">
            <span class="role">{{ msg.role === 'user' ? '用户' : 'AI' }}</span>
            <span class="time">{{ formatTime(msg.created_at) }}</span>
          </div>
          <div class="message-content">{{ msg.content }}</div>
        </div>
      </div>
      <div v-else class="no-selection">
        请选择对话查看详细记录
      </div>
    </el-aside>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { getRequest } from '@/utils/http';

const searchUser = ref('');
const currentUserId = ref('');
const currentConvId = ref('');
const users = ref<any[]>([]);
const userConversations = ref<any[]>([]);
const conversationMessages = ref<any[]>([]);
const isDarkMode = ref(false);

// 示例数据
const mockUsers = [
  { id: '1', username: '张三', avatar: '' },
  { id: '2', username: '李四', avatar: '' },
  { id: '3', username: '王五', avatar: '' }
];

const mockConversations = [
  { id: '1', title: '关于项目进度的讨论', created_at: '2024-01-15T10:00:00' },
  { id: '2', title: '技术方案探讨', created_at: '2024-01-16T14:30:00' }
];

const mockMessages = [
  { 
    id: '1', 
    role: 'user', 
    content: '这个项目预计什么时候能完成？', 
    created_at: '2024-01-15T10:00:00' 
  },
  { 
    id: '2', 
    role: 'assistant', 
    content: '根据目前的进度,预计下周三可以完成全部开发工作。后续还需要进行测试和部署,整体项目计划在月底前完成。', 
    created_at: '2024-01-15T10:01:00' 
  },
  { 
    id: '3', 
    role: 'user', 
    content: '好的,那测试阶段大概需要多久？', 
    created_at: '2024-01-15T10:02:00' 
  },
  { 
    id: '4', 
    role: 'assistant', 
    content: '测试阶段预计需要3-5个工作日,包括功能测试和性能测试。如果发现重大问题可能会需要更多时间。', 
    created_at: '2024-01-15T10:03:00' 
  }
];

// 过滤用户列表
const filteredUsers = computed(() => {
  return users.value.filter(user =>
    user.username.toLowerCase().includes(searchUser.value.toLowerCase())
  );
});

// 获取用户列表
async function fetchUsers() {
  try {
    // ���果 API 可用就使用真实数据
    const baseURL = import.meta.env.VITE_APP_BASE_URL;
    const response = await getRequest<any>(baseURL + '/v1/api/admin/users');
    users.value = response.data;
  } catch (error) {
    // 如果 API 不可用就使用示例数据
    users.value = mockUsers;
    console.log('Using mock data');
  }
}

// 获取用户的对话列表
async function handleUserClick(userId: string) {
  currentUserId.value = userId;
  currentConvId.value = '';
  try {
    const baseURL = import.meta.env.VITE_APP_BASE_URL;
    const response = await getRequest<any>(baseURL + `/v1/api/admin/users/${userId}/conversations`);
    userConversations.value = response.data;
  } catch (error) {
    userConversations.value = mockConversations;
  }
}

// 获取对话详细记录
async function handleConversationClick(convId: string) {
  currentConvId.value = convId;
  try {
    const baseURL = import.meta.env.VITE_APP_BASE_URL;
    const response = await getRequest<any>(baseURL + `/v1/api/admin/conversations/${convId}/messages`);
    conversationMessages.value = response.data;
  } catch (error) {
    conversationMessages.value = mockMessages;
  }
}

// 格式化日期
function formatDate(date: string) {
  return new Date(date).toLocaleDateString();
}

// 格式化时间
function formatTime(date: string) {
  return new Date(date).toLocaleTimeString();
}

// 页面加载时获取用户列表
onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.chat-container {
  height: 100vh;
  background: var(--bg-color, #f5f7fa);
  transition: all 0.3s ease;
}

.chat-container.dark-mode {
  --bg-color: #1a1a1a;
  --card-bg: #242424;
  --text-color: #fff;
  --border-color: #333;
  color: var(--text-color);
}

.chat-aside{
  width: 20% !important;  /* 改为20% */
  background: var(--card-bg, #fff);
  border-right: 1px solid var(--border-color, #eee);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border-radius: 16px;
  margin: 12px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.aside-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-color, #eee);
  display: flex;
  gap: 12px;
  align-items: center;
}

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.chat-aside-right {
  width: 50% !important;  /* 改为20% */
  background: rgba(248, 249, 250, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  margin: 12px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.chat-main {
  width: 25% !important;  /* 改为45% */
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  margin: 12px;
  padding: 20px;
}

.search-box {
  margin-bottom: 20px;
}

.user-item, .conversation-item {
  display: flex;
  align-items: center;
  padding: 12px;
  margin: 8px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.user-item:hover, .conversation-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.user-item.active, .conversation-item.active {
  background: #0245a3;
  color: white;
}

.username {
  margin-left: 12px;
}

.message-item {
  margin: 16px 0;
  padding: 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.user-message {
  background: #e3f2fd;
}

.assistant-message {
  background: #f5f5f5;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
  color: #666;
}

.message-content {
  white-space: pre-wrap;
  word-break: break-word;
}

.no-selection {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #999;
}

@media screen and (max-width: 768px) {
  .chat-aside,
  .chat-aside-right,
  .chat-main {
    width: 100% !important;
    margin: 6px;
  }
  
  .el-container {
    flex-direction: column;
  }
}
</style>

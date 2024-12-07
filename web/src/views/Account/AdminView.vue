<script setup lang="ts">
import { ref, computed } from 'vue'
import type { TabsPaneContext } from 'element-plus'

const activeName = ref('users')
const handleClick = (tab: TabsPaneContext) => {
  console.log(tab.props.name)
}

// 用户数据
const users = ref([
  { id: 1, username: 'user1', email: 'user1@example.com', created_at: '2024-01-01' },
  { id: 2, username: 'user2', email: 'user2@example.com', created_at: '2024-01-02' }
])

// 对话数据
const conversations = ref([
  { id: 1, user_id: 1, title: '对话1', created_at: '2024-01-01', message_count: 10 },
  { id: 2, user_id: 2, title: '对话2', created_at: '2024-01-02', message_count: 5 }
])

// 知识库数据
const knowledgeBases = ref([
  { id: 1, user_id: 1, name: '知识库1', doc_count: 5, created_at: '2024-01-01' },
  { id: 2, user_id: 2, name: '知识库2', doc_count: 3, created_at: '2024-01-02' }
])

// 计算统计数据
const statistics = computed(() => ({
  totalUsers: users.value.length,
  totalConversations: conversations.value.length,
  totalKnowledgeBases: knowledgeBases.value.length
}))

// 搜索关键词
const searchQuery = ref('')

// 过滤后的数据
const filteredUsers = computed(() => {
  return users.value.filter(user => 
    user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <div class="admin-container">
    <div class="admin-header">
      <h1>系统管理控制台</h1>
      <el-row :gutter="20" class="statistics-cards">
        <el-col :span="8">
          <el-card class="statistic-card">
            <div class="statistic-value">{{ statistics.totalUsers }}</div>
            <div class="statistic-label">总用户数</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="statistic-card">
            <div class="statistic-value">{{ statistics.totalConversations }}</div>
            <div class="statistic-label">总对话数</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="statistic-card">
            <div class="statistic-value">{{ statistics.totalKnowledgeBases }}</div>
            <div class="statistic-label">知识库数量</div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="admin-content">
      <el-tabs v-model="activeName" class="main-tabs" @tab-click="handleClick">
        <el-tab-pane label="用户管理" name="users">
          <div class="table-operations">
            <el-input
              v-model="searchQuery"
              placeholder="搜索用户名或邮箱"
              prefix-icon="Search"
              class="search-input"
            />
          </div>
          <el-table :data="filteredUsers" style="width: 100%" class="custom-table">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" width="120" />
            <el-table-column prop="email" label="邮箱" width="180" />
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="对话管理" name="conversations">
          <el-table :data="conversations" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="user_id" label="用户ID" width="80" />
            <el-table-column prop="title" label="对话标题" width="180" />
            <el-table-column prop="message_count" label="消息数" width="100" />
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" @click="handleView(scope.row)">查看</el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="知识库管理" name="knowledge">
          <el-table :data="knowledgeBases" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="user_id" label="用户ID" width="80" />
            <el-table-column prop="name" label="知识库名称" width="180" />
            <el-table-column prop="doc_count" label="文档数" width="100" />
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" @click="handleView(scope.row)">查看</el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.admin-header {
  margin-bottom: 24px;
}

h1 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 24px;
  font-weight: 600;
}

.statistics-cards {
  margin-bottom: 24px;
}

.statistic-card {
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  color: white;
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.statistic-card:hover {
  transform: translateY(-5px);
}

.statistic-value {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 8px;
}

.statistic-label {
  font-size: 14px;
  opacity: 0.9;
}

.admin-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.main-tabs {
  padding: 20px;
}

.table-operations {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 300px;
}

.custom-table {
  :deep(.el-table__header) {
    background-color: #f5f7fa;
  }
  
  :deep(.el-button) {
    padding: 6px 16px;
    border-radius: 4px;
  }
}

@media (max-width: 768px) {
  .statistics-cards {
    .el-col {
      margin-bottom: 16px;
    }
  }
  
  .search-input {
    width: 100%;
  }
}
</style>

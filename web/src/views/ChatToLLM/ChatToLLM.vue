<template>
    <div class="chat-container">
        <el-container>
            <el-aside width="300px" class="chat-aside">
                <el-card class="chat-list">
                    <p v-for="o in 6" :key="o" class="chat-item">{{ 'Chat Room ' + o }}</p>
                </el-card>
            </el-aside>
            <el-main class="chat-main">
                <el-card class="chat-content">
                    <div class="message-container" ref="messageContainer">
                        <p v-for="o in 10" :key="o" class="message-item">{{ 'Message ' + o }}</p>
                    </div>
                    <div class="input-area">
                        <el-input v-model="textarea1" class="input-box" autosize type="textarea"
                            placeholder="Type your message..." />
                        <el-button type="primary" circle @click="sendMessage">Send</el-button>
                    </div>
                </el-card>
            </el-main>
        </el-container>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, nextTick } from 'vue';
const textarea1 = ref('');
const messageContainer = ref(null);

const sendMessage = () => {
    if (textarea1.value.trim()) {
        // 发送消息的逻辑
        console.log('Message sent:', textarea1.value);
        textarea1.value = ''; // 清空输入框
        scrollToBottom(); // 发送消息后滚动到底部
    }
};

const scrollToBottom = () => {
    nextTick(() => {
        messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    });
};

onMounted(() => {
    scrollToBottom(); // 初始化时滚动到底部
});
</script>

<style scoped>
.chat-container {
    height: 100vh;
    display: flex;
}

.chat-aside {
    background-color: #f9fafc;
    box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.chat-list {
    height: 100%;
    overflow-y: auto;
    padding: 20px;
}

.chat-item {
    padding: 10px 0;
    cursor: pointer;
    transition: background-color 0.2s;
}

.chat-item:hover {
    background-color: #f0f2f5;
}

.chat-main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: #ffffff;
    padding: 20px;
    box-shadow: -2px 0 6px rgba(0, 0, 0, 0.1);
}

.chat-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
}

.message-container {
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 8px;
    margin-bottom: 20px;
}

.message-item {
    padding: 10px;
    background-color: #ffffff;
    border-radius: 6px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.input-area {
    display: flex;
    align-items: center;
    gap: 10px;
}

.input-box {
    flex-grow: 1;
}

.el-button {
    height: 40px;
    width: 40px;
}
</style>
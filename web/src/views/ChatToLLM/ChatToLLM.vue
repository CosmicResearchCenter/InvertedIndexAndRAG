<template>
    <el-container>
        <!-- 左侧对话列表 -->
        <el-aside class="chat-aside">
            <div class="chat-list">
                <ChatLogItem
                    class="chat-log-item"
                    v-for="item in conversionsList"
                    :key="item.conversation_id"
                    :title="String(item.conversationName)"
                    @click="handleItemClick(item.conversation_id)"
                    :active="currentConversationId === item.conversation_id" />
            </div>
            <el-button type="primary" @click="createConversation" class="create-button">新建对话</el-button>
        </el-aside>

        <!-- 主聊天界面 -->
        <el-main class="chat-main">
            <div class="chat-content" ref="chatContent">
                <div class="message-container" v-for="item in conversionMessage" :key="item.id">
                    <div class="message-item-user">
                        <MessageItem_User :message="String(item.query)" />
                    </div>
                    <div class="message-item-assistant">
                        <MessageItem_Assistant :message="String(item.answer)" />
                    </div>
                </div>
            </div>

            <!-- 输入区域 -->
            <div class="input-area">
                <el-input
                    v-model="message"
                    class="input-box"
                    autosize
                    type="textarea"
                    placeholder="Type your message..." />
                <el-button type="primary" @click="sendMessage">Send</el-button>
            </div>
        </el-main>

        <!-- 右侧知识库菜单 -->
        <el-aside class="chat-aside-right">
            <div class="knowledge-base-list">
                <KnowledgeBaseItem
                    v-for="item in knowledgebaseList"
                    :key="item.id"
                    class="knowledge-base-item"
                    :checked="choosedKnowledgeBaseId === item.id"
                    :knowledgeBaseName="String(item.knowledgeBaseName)"
                    :knowledgeBaseId="String(item.id)"
                    @click="choosedKnowledgeBaseId = item.id" />
            </div>
        </el-aside>
    </el-container>
</template>

<script lang="ts" setup>
import { ref, onMounted, nextTick } from 'vue';
import MessageItem_User from "@/components/MessageItem_User.vue";
import MessageItem_Assistant from "@/components/MessageItem_Assistant.vue";
import ChatLogItem from '@/components/ChatLogItem.vue';
import KnowledgeBaseItem from '@/components/KnowledgeBaseItem.vue';
import { getRequest, postRequest } from '@/utils/http';

const conversionsList = ref([]);
const conversionMessage = ref([]);
const knowledgebaseList = ref([]);
const choosedKnowledgeBaseId = ref('');
const message = ref('');
const currentConversationId = ref('');
const chatContent = ref(null);

async function sendMessage() {
    if (message.value === '') return;
    const data:any = await postRequest<any>('http://localhost:9988/v1/api/mark/chat/chat-message', {
        "conversation_id": currentConversationId.value,
        "message": message.value,
        "user_id": "mark"
    });
    conversionMessage.value.push(data.data);
    message.value = '';
    scrollToBottom();
}

function scrollToBottom() {
    nextTick(() => {
        if (chatContent.value) {
            chatContent.value.scrollTop = chatContent.value.scrollHeight;
        }
    });
}

async function getConversionsList() {
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/chat/chat-message/mark');
    conversionsList.value = data.data;
}

async function handleItemClick(conversation_id: string) {
    choosedKnowledgeBaseId.value = conversation_id;
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/chat/chat-history/' + conversation_id);
    conversionMessage.value = data.data;
    currentConversationId.value = conversation_id;
    scrollToBottom();
}

async function getKnowledgeBaseList() {
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/knowledgebase');
    knowledgebaseList.value = data.data;
}

async function createConversation() {
    const knowledge_base_id = knowledgebaseList.value[0]?.id || '';
    const user_id = "mark";
    const data = await postRequest<any>('http://localhost:9988/v1/api/mark/chat/create-conversation', {
        "knowledge_base_id": knowledge_base_id,
        "user_id": user_id
    });
    getConversionsList();
    handleItemClick(data.data.conversation_id);
}

onMounted(() => {
    getConversionsList();
    scrollToBottom();
    getKnowledgeBaseList();
});
</script>

<style scoped>
.chat-aside, .chat-aside-right {
    height: 100%;
    padding: 10px;
    background-color: #f7f7f7;
    border-right: 1px solid #e0e0e0;
    overflow-y: auto;
}

.chat-list {
    height: calc(100vh - 60px);
    overflow-y: auto;
}

.chat-log-item {
    margin: 8px;
    cursor: pointer;
}

.create-button {
    margin-top: 10px;
    width: 100%;
}

.chat-main {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.chat-content {
    flex-grow: 1;
    padding: 10px;
    overflow-y: auto;
    background-color: #fafafa;
    scroll-behavior: smooth;
}

.message-container {
    display: flex;
    flex-direction: column;
}

.message-item-user, .message-item-assistant {
    margin: 8px;
}

.message-item-user {
    align-self: flex-end;
}

.message-item-assistant {
    align-self: flex-start;
}

.input-area {
    display: flex;
    padding: 10px;
    background-color: #fff;
    border-top: 1px solid #e0e0e0;
    align-items: center;
    gap: 10px;
}

.input-box {
    flex-grow: 1;
}

.knowledge-base-list {
    padding: 10px;
    overflow-y: auto;
    height: calc(100vh - 20px);
}

.knowledge-base-item {
    margin-bottom: 10px;
    cursor: pointer;
}
</style>

<template>
    <el-container style="height: 100%; width: 100%;">
        <!-- Left Sidebar for Chat List -->
        <el-aside class="chat-aside">
            <el-button type="primary" @click="createConversation" class="create-button">新建对话</el-button>
            <div class="chat-list">
                <ChatLogItem class="chat-log-item" :class="{ active: currentConversationId === item.conversation_id }"
                    v-for="item in conversionsList" :key="item.conversation_id" :title="String(item.conversationName)"
                    :conversation_id="item.conversation_id" @click="handleItemClick(item.conversation_id)"
                    @updateTitle="updateConversationTitle(item.conversation_id, $event)"
                    @refreshList="getConversionsList" />
            </div>
        </el-aside>

        <!-- Main Chat Interface -->
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

            <!-- Input Area -->
            <div class="input-area">
                <el-input v-model="message" class="input-box" autosize type="textarea"
                    placeholder="Type your message..." />
                <el-button type="primary" @click="sendMessage">Send</el-button>
                <el-loading v-if="loading" text="Sending..."></el-loading> <!-- Loading indicator -->
            </div>
        </el-main>

        <!-- Right Sidebar for Knowledge Base -->
        <el-aside class="chat-aside-right">
            <div class="knowledge-base-list">
                <KnowledgeBaseItem v-for="item in knowledgebaseList" :key="item.id" class="knowledge-base-item"
                    :class="{ active: choosedKnowledgeBaseId === item.id }"
                    :knowledgeBaseName="String(item.knowledgeBaseName)" :knowledgeBaseId="String(item.id)"
                    @click="switchKnowledgeBase(item.id)" />
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
import { ElMessageBox, ElMessage } from 'element-plus';
import { ElLoading } from 'element-plus';

const conversionsList = ref<any>([]);
let conversionMessage = ref<any>([]);
const knowledgebaseList = ref<any>([]);
const choosedKnowledgeBaseId = ref<any>('');
const message = ref<any>('');
const currentConversationId = ref<any>('');
let chatContent = ref<any>(null);
const  loading = ref<boolean>(false);

async function sendMessage() {
    if (message.value === '') return;

    loading.value = true; // 显示加载状态
    let chatItemUser:any ={
        id: Date.now(),
        query: message.value,
        answer: '',

    };
    
    conversionMessage.value.push(chatItemUser);
    let message_length = conversionMessage.value.length;
    try {
        const response:any = await fetch('http://localhost:9988/v1/api/mark/chat/chat-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "conversation_id": currentConversationId.value.toString(),
                "message": message.value,
                "user_id": "mark",
                "streaming": true
            })
        });

        if (!response.ok) throw new Error('网络错误，无法发送消息');


        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let resultText = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            resultText += decoder.decode(value, { stream: true });
            conversionMessage.value[message_length - 1].answer = resultText;
            scrollToBottom();
        }

        message.value = '';
    } catch (error:any) {
        console.error(error);
    } finally {
        loading.value = false; // 隐藏加载状态
    }
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
    conversionsList.value = data.data.reverse();

    if (conversionsList.value.length > 0) {
        const latestConversationId = conversionsList.value[0].conversation_id;
        handleItemClick(latestConversationId);
    }
}

async function handleItemClick(conversation_id: string) {
    currentConversationId.value = conversation_id;

    // 加载当前对话的历史消息
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/chat/chat-history/' + conversation_id);
    conversionMessage.value = data.data;

    // 设置为当前对话关联的知识库 ID
    let dataLength = data.data.length;
    choosedKnowledgeBaseId.value = data.data[dataLength - 1]?.current_knowledge_baseid || '';

    scrollToBottom();
}

async function getKnowledgeBaseList() {
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/knowledgebase');
    knowledgebaseList.value = data.data;
}

async function switchKnowledgeBase(knowledgeBaseId: string) {
    choosedKnowledgeBaseId.value = knowledgeBaseId;
    if (!currentConversationId.value) return;

    const response: any = await postRequest<any>('http://localhost:9988/v1/api/mark/chat/knowledge_base', {
        "user_id": "mark",
        "conversation_id": currentConversationId.value.toString(),
        "knowledge_base_id": knowledgeBaseId
    });

    if (response.code === 200) {
        ElMessage.info('切换知识库成功！');
        // await handleItemClick(currentConversationId.value);
    }
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

function updateConversationTitle(conversationId: string, newTitle: string) {
    const conversation = conversionsList.value.find(item => item.conversation_id === conversationId);
    if (conversation) {
        conversation.conversationName = newTitle;
    }
}

onMounted(() => {
    getConversionsList();
    scrollToBottom();
    getKnowledgeBaseList();
});
</script>

<style scoped>
.chat-aside,
.chat-aside-right {
    height: 100%;
    padding: 10px;
    background-color: #f7f7f7;
    border-right: 1px solid #e0e0e0;
    overflow-y: auto;
    flex-shrink: 0;
}

.chat-list,
.knowledge-base-list {
    height: 100%;
}

.chat-log-item {
    margin: 8px;
    cursor: pointer;
}

.chat-log-item.active {
    background-color: #e6f7ff;
    color: #1890ff;
    font-weight: bold;
}

.knowledge-base-item {
    margin-bottom: 10px;
    cursor: pointer;
}

.knowledge-base-item.active {
    background-color: #e6f7ff;
    color: #1890ff;
    font-weight: bold;
}

.create-button {
    margin-top: 10px;
    width: 100%;
}

.chat-main {
    display: flex;
    flex-direction: column;
    height: 100%;
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

.message-item-user,
.message-item-assistant {
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

.input-area {
    display: flex;
    padding: 10px;
    background-color: #fff;
    border-top: 1px solid #e0e0e0;
    align-items: center;
    gap: 10px;
}

/* Add some styles for loading */
.el-loading {
    margin-left: 10px; /* Adjust as needed */
}
</style>

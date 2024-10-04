<template>
    <el-container>
        <el-aside class="chat-aside">

            <!-- 左侧对话列表 -->
            <div class="chat-list">
                <!-- <el-card class="chatlog-title" style=""> -->

                <!-- </el-card> -->
                <ChatLogItem class="chat-log-item" v-for="item in conversionsList" :key="item.conversation_id"
                    :title="String(item.conversationName)" @click="handleItemClick(item.conversation_id)">

                </ChatLogItem>

            </div>
            <el-button type="primary" @click="createConversation">新建对话</el-button>
        </el-aside>
        <el-main class="chat-main">
            <!-- 聊天界面 -->
            <div class="chat-content">
                <div class="message-container" v-for="item in conversionMessage">
                    <div class="message-item-user">
                        <MessageItem_User :message="String(item.query)">
                        </MessageItem_User>
                    </div>
                    <div class="message-item-assistant">
                        <MessageItem_Assistant :message="String(item.answer)">
                        </MessageItem_Assistant>
                    </div>
                </div>
            </div>
            <div class="input-area">
                <el-input v-model="message" class="input-box" autosize type="textarea"
                    placeholder="Type your message..." />
                <el-button type="primary" @click="sendMessage">Send</el-button>
            </div>
        </el-main>
        <el-aside class="chat-aside-right">
            <!-- 右侧选择知识库菜单 -->
            <div class="knowledge-base-list">
                <!-- <div > -->
                    <KnowledgeBaseItem v-for="item in knowledgebaseList" :key="item.id" class="knowledge-base-item"  :checked="choosedKnowledgeBaseId === item.id" 
                        :knowledgeBaseName="String(item.knowledgeBaseName)" :knowledgeBaseId="String(item.id)">
                        </KnowledgeBaseItem>
                <!-- </div> -->
            </div>
        </el-aside>
    </el-container>
</template>

<script lang="ts" setup>
import { ref, onMounted, nextTick } from 'vue';
import MessageItem_User from "@/components/MessageItem_User.vue"
import MessageItem_Assistant from "@/components/MessageItem_Assistant.vue";
import ChatLogItem from '@/components/ChatLogItem.vue';
import KnowledgeBaseItem from '@/components/KnowledgeBaseItem.vue';
import { getRequest, postRequest, putRequest, deleteRequest } from '@/utils/http';

// const textarea1 = ref('');
const radio1 = ref('1')
const conversionsList = ref([]);
const conversionMessage = ref([]);
const knowledgebaseList = ref([]);
const choosedKnowledgeBaseId = ref('');

const message  = ref('');

//  当前的对话ID
const currentConversationId = ref('');

async function sendMessage () {
    if(message.value === '') return;
    const data = await postRequest<any>('http://localhost:9988/v1/api/mark/chat/chat-message', {
        "conversation_id": currentConversationId.value,
        "message": message.value,
        "user_id": "mark"
    });
    console.log(data);
    conversionMessage.value.push(data.data)
    message.value = '';
    // handleItemClick(choosedKnowledgeBaseId.value);
    // scrollToBottom();
    // message.value = '';
    // textarea1.value = ''
    // console.log
};

const scrollToBottom = () => {
    nextTick(() => {
        // messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    });
};
async function getConversionsList() {
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/chat/chat-message/mark');
    console.log(data.data[0]);
    conversionsList.value = data.data;
}
async function handleItemClick(conversation_id: string) {
    console.log(conversation_id);
    choosedKnowledgeBaseId.value = conversation_id;
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/chat/chat-history/' + conversation_id);
    // console.log(data.data[0]);
    conversionMessage.value = data.data;
    currentConversationId.value = conversation_id;
    console.log(conversionMessage.value);
}

async function getKnowledgeBaseList() {
    const data = await getRequest<any>('http://localhost:9988/v1/api/mark/knowledgebase');
    // console.log(data);
    knowledgebaseList.value = data.data;
}

// 创建对话
async function createConversation() {
    var knowledge_base_id:string = knowledgebaseList.value[0].id;
    var user_id:string = "mark";

    const data = await postRequest<any>('http://localhost:9988/v1/api/mark/chat/create-conversation', {
        "knowledge_base_id": knowledge_base_id,
        "user_id": user_id
    });
    console.log(data);
    getConversionsList();
    handleItemClick(data.data.conversation_id);
    currentConversationId.value = data.data[0].conversation_id;
}



onMounted(() => {
    getConversionsList();
    scrollToBottom();
    getKnowledgeBaseList();
});
</script>

<style scoped>
.chat-aside {
    height: 100%;
    text-align: center;
}

.chat-list {
    height: 100vh;
    overflow-y: scroll;

}

.chat-log-item {
    margin: 10px;
}

.chat-main {
    height: 100vh;
    /* background-color: #e5e5e5; */
    display: flex;
    flex-direction: column;
}

.chat-content {
    /* background-color: #e5e5e5; */
    overflow-y: auto;
    display: flex;

    /* background-color: #e5e5e5; */
    flex-direction: column;
}

.message-container {
    display: flex;
    /* background-color: #e5e5e5; */

    flex-direction: column;

    /* height: calc(100vh - 100px); */
    /* Adjust height to fit input area */
}

.message-item-user {
    margin: 10px;
    align-self: flex-end;
    /* Align user messages to the right */
}

.message-item-assistant {
    margin: 10px;
    align-self: flex-start;
    /* Align assistant messages to the left */
}

.input-area {
    padding: 10px;
    display: flex;
    justify-content: space-between;
}

.chat-aside-right {
    height: 100%;
}

.knowledge-base-list {
    height: 100vh;
    overflow-y: scroll;
}

.knowledge-base-item {
    margin: 10px;
}
</style>

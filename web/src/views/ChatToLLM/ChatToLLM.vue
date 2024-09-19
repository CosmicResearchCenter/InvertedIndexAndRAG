<template>
    <el-container>
        <el-aside class="chat-aside">
            <!-- 左侧对话列表 -->
            <div class="chat-list">
                <ChatLogItem class="chat-log-item" v-for="o in 20" :title="String('对话' + o)"></ChatLogItem>
            </div>
        </el-aside>
        <el-main class="chat-main">
            <!-- 聊天界面 -->
            <div class="chat-content">
                <div class="message-container">
                    <div class="message-item-assistant" v-for="o in 5" :key="'assistant-' + o">
                        <MessageItem_Assistant
                            :message="String('要使用户的消息在右边显示，助手的消息在左边显示，您可以根据以下步骤调整代码：\n1. **更新HTML结构**：将用户和助手的消息项放在同一个容器内，并使用CSS来控制它们的位置。\n2. **调整CSS**：使用`flex`布局来控制消息的对齐方式。' + o)">
                        </MessageItem_Assistant>
                    </div>
                    <div class="message-item-user" v-for="o in 5" :key="'user-' + o">
                        <MessageItem_User
                            :message="String('助手消息213098019380219380912830912 地方去外地去地区为夺取皇位iudh亲卫队请问地区武汉地区的球队和网球的\n取缔哦亲我的i请问大家哦i轻举妄动' + o)">
                        </MessageItem_User>
                    </div>
                </div>
            </div>
            <div class="input-area">
                <el-input v-model="textarea1" class="input-box" autosize type="textarea"
                    placeholder="Type your message..." />
                <el-button type="primary" @click="sendMessage">Send</el-button>
            </div>
        </el-main>
        <el-aside class="chat-aside-right">
            <!-- 右侧选择知识库菜单 -->
            <div class="knowledge-base-list">

                <KnowledgeBaseItem class="knowledge-base-item" v-for="o in 10" :knowledgeBaseName="String('知识库' + o)"
                    :knowledgeBaseId="String(o)"></KnowledgeBaseItem>

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
const textarea1 = ref('');
const radio1 = ref('1')

const sendMessage = () => {
    if (textarea1.value.trim()) {
        console.log('Message sent:', textarea1.value);
        textarea1.value = '';
        scrollToBottom();
    }
};

const scrollToBottom = () => {
    nextTick(() => {
        // messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    });
};

onMounted(() => {
    scrollToBottom();
});
</script>

<style scoped>
.chat-aside {
    height: 100%;
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

}

.message-container {
    display: flex;
    /* background-color: #e5e5e5; */

    flex-direction: column;
    overflow-y: auto;
    height: calc(100vh - 100px);
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

<template>
    <div class="msg-box">
        <div  class="avatar-box">
            <el-avatar class="avatar" shape="circle" size="100" fit="fit" :src="avatar_url" />
        </div>
        <v-md-preview  :text="message" class="msg"></v-md-preview > 
    </div>
    <!-- 显示召回文档的Box -->
    <div class="retriever-box">
        <el-collapse accordion>
            <el-collapse-item title="召回文档">
                <el-collapse accordion>
                    <el-collapse-item v-for="(doc, index) in retrievedDocs" :key="index" :title="(doc.knowledge_doc_name)">
                        <p>{{ doc.content }}</p>
                    </el-collapse-item>
                </el-collapse>
            </el-collapse-item> 
        </el-collapse>  
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
export default defineComponent({
    name: 'MessageItem_Assistant',
    props: {
        message: {
            type: String as PropType<string>,
            required: true,
        },
        avatar_url: {
            type: String as PropType<string>,
            required: false
        },
        retrievedDocs: {
            type: Array as PropType<Array<{ content: string, knowledge_doc_name: string }>>,
            required: true
        }
    },
});
</script>
<style>
    .msg-box {
        display: flex;
        flex-direction: row;
        /* justify-content: flex-start; */
    }
    .avatar-box{
        width:auto ;
        height: auto;
    }
    .avatar {
        margin: 10px;
        width: 50px;
        height: 50px;
        border-radius: 100%;
    }
    .msg {
        padding: 5px;
        /* margin: 5px; */
        height: auto;
        width: auto;
        /* box-shadow:  2px 3px 6px #ccc; */
        background-color: #ffffff;
    }
    .retriever-box {
        margin-top: 20px;
        padding: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    .retriever-box .el-collapse-item__header {
        font-weight: bold;
        color: #333;
    }
    .retriever-box .el-collapse-item__content {
        padding: 10px;
        background-color: #fff;
        border-top: 1px solid #e0e0e0;
    }
</style>
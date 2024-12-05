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
  gap: 16px;
  margin: 24px 0;
  position: relative;
}

.avatar {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 2px solid #fff;
}

.msg {
  background: linear-gradient(145deg, #ffffff, #f5f5f5);
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 6px 6px 12px rgba(0, 0, 0, 0.08),
              -6px -6px 12px rgba(255, 255, 255, 0.8);
  max-width: 80%;
  position: relative;
}

.msg::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 20px;
  width: 16px;
  height: 16px;
  background: linear-gradient(145deg, #ffffff, #f5f5f5);
  transform: rotate(45deg);
  box-shadow: -3px 3px 6px rgba(0, 0, 0, 0.05);
}

.retriever-box {
  margin: 16px 60px;
  border-radius: 12px;
  background: rgba(248, 249, 250, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.05);
}

.retriever-box :deep(.el-collapse-item__header) {
  padding: 16px;
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  background: transparent;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.retriever-box :deep(.el-collapse-item__content) {
  padding: 20px;
  line-height: 1.6;
  color: #495057;
  background: rgba(255, 255, 255, 0.5);
}
</style>
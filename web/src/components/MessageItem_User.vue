<template>
    <div class="msg-box">
        <!-- <el-card style="" class="msg">
            {{ message }}
        </el-card> -->
        <v-md-preview  :text="message" class="msg"></v-md-preview >
        <div  class="avatar-box">
            <el-avatar class="avatar" shape="circle" size="100" fit="fit" :src="avatar_url" />
        </div>
        </div>

</template>
<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
export default defineComponent({
    name: 'MessageItem_User',
    props: {
        message: {
            type: String as PropType<string>,
            required: true,
        },
        avatar_url: {
            type: String as PropType<string>,
            required: false
        }
    },
});
</script>
<style>
.msg-box {
  display: flex;
  gap: 16px;
  margin: 24px 0;
  justify-content: flex-end;
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
  background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 
    0 4px 24px -1px rgba(37, 99, 235, 0.2),
    0 2px 8px -1px rgba(37, 99, 235, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  max-width: 80%;
  position: relative;
}

.msg::before {
  content: '';
  position: absolute;
  right: -8px;
  top: 20px;
  width: 16px;
  height: 16px;
  background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
  transform: rotate(45deg);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.msg :deep(*) {
  color: #ffffff !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.msg :deep(code) {
  background-color: rgba(255, 255, 255, 0.2) !important;
  border-radius: 6px;
  padding: 2px 6px;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.msg :deep(pre) {
  background-color: rgba(255, 255, 255, 0.15) !important;
  border-radius: 12px;
  padding: 12px;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.msg :deep(p) {
  margin: 0;
  line-height: 1.6;
}
</style>
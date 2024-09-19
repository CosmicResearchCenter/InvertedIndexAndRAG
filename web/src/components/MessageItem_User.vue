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
        flex-direction: row;

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
        /* background-color: #ffffff; */
        box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
    }
</style>
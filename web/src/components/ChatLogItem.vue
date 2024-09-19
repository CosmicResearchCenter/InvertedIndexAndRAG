<template>
    <el-card class="chatlog-title" style="">
        {{ title }}
    </el-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
export default defineComponent({
    name: 'MessageItem',
    props: {
        title: {
            type: String as PropType<string>,
            required: true,
        },
    },
});
</script>
<style>
    .chatlog-title {
        text-align: center;
    }
</style>
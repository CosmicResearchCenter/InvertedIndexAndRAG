<template>
    <el-card shadow="hover" class="kb-box">
        {{ knowledgeBaseName }}
    </el-card>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
export default defineComponent({
    name: 'KnowledgeBaseItem',
    props: {
        knowledgeBaseName: {
            type: String as PropType<string>,
            required: true,
        },
        knowledgeBaseId: {
            type: String as PropType<string>,
            required: true,
        },
    },

});
</script>
<style>
    
</style>
<template>
    <el-row :gutter="20">
        <!-- Create new knowledge base card -->
        <el-col :span="8" class="col-card">
            <el-card class="new-base" shadow="hover" @click="goToCreate">
                <div class="new-base-content">
                    <el-icon :size="60">
                        <Plus />
                    </el-icon>
                    <div>创建知识库</div>
                    <div class="sub-text">导入您的文本数据以增强 LLM 的上下文。</div>
                </div>
            </el-card>
        </el-col>

        <!-- Dynamic cards for files -->
        <el-col v-for="(file, index) in files" :key="index" :span="8" class="col-card">
            <el-card class="box-card" shadow="hover" @click="goToKnowledgeBase(file.id)">
                <div class="card-content">
                    <el-icon :size="60">
                        <Document />
                    </el-icon>
                    <div>{{ file.name }}</div>
                    <div>{{ file.details }}</div>
                </div>

                <!-- Add @click.stop to the container and dropdown items to prevent event propagation -->
                <div class="menu" @click.stop>
                    <el-dropdown trigger="click">
                        <span class="el-dropdown-link" @click.stop>
                            <el-icon>
                                <More />
                            </el-icon>
                        </span>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item @click.stop="handleMenuCommand(file)('settings')">设置</el-dropdown-item>
                                <el-dropdown-item @click.stop="handleMenuCommand(file)('delete')">删除</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { Plus, Document } from '@element-plus/icons-vue';

interface FileData {
    id: number;
    name: string;
    details: string;
}

export default defineComponent({
    components: { Plus, Document },
    setup() {
        const router = useRouter();
        
        const files = reactive<FileData[]>([
            { id: 1, name: '常用校园信息集合.txt', details: '1 文档 | 1 千字符 | 0 关联应用' },
            { id: 2, name: '常用校园信息集合.txt', details: '1 文档 | 1 千字符 | 0 关联应用' },
            { id: 3, name: '常用校园信息集合.txt', details: '1 文档 | 1 千字符 | 0 关联应用' },
            { id: 4, name: '常用校园信息集合.docx', details: '1 文档 | 8 千字符 | 1 关联应用' },
            { id: 5, name: '常用校园信息集合.txt', details: '1 文档 | 19 千字符 | 0 关联应用' }
        ]);

        const goToCreate = () => {
            router.push("/manager/id/create");
        };

        const goToKnowledgeBase = (id: number) => {
            router.push(`/manager/${id}`);
        };

        const handleMenuCommand = (file: FileData) => (command: string) => {
            if (command === 'settings') {
                console.log('Settings for:', file);
                // Add settings functionality here
            } else if (command === 'delete') {
                console.log('Deleting:', file);
                // Add delete functionality here
            }
        };

        return { files, goToCreate, goToKnowledgeBase, handleMenuCommand };
    }
});
</script>

<style scoped>
.box-card,
.new-base {
    width: 100%;
    height: 200px;
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
}

.new-base-content {
    text-align: center;
}

.sub-text {
    font-size: 12px;
    color: #375aa2;
    margin-top: 10px;
}

.col-card {
    margin-bottom: 20px;
}

.card-content {
    text-align: center;
    font-size: 15px;
}

.menu {
    position: absolute;
    bottom: 10px;
    right: 10px;
}

.menu-button {
    padding: 0;
}
</style>
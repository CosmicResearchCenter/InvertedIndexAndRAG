<template>
    <el-row :gutter="20">
        <!-- Create new knowledge base card -->
        <el-col :span="8" class="col-card">
            <el-card class="new-base" shadow="hover" @click="openDialog">
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
                                <el-dropdown-item
                                    @click.stop="handleMenuCommand(file)('settings')">设置</el-dropdown-item>
                                <el-dropdown-item @click.stop="handleMenuCommand(file)('delete')">删除</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </div>
            </el-card>
        </el-col>
        <el-dialog title="设置知识库名称" v-model="dialogVisible">
            <el-input v-model="knowledgeBaseName" placeholder="请输入知识库名称"></el-input>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="createKnowledgeBase">确定</el-button>
            </span>
        </el-dialog>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Plus, Document, More } from '@element-plus/icons-vue';
import { getRequest, postRequest, deleteRequest } from '@/utils/http';

interface FileData {
    id: string;
    name: string;
    details: string;
}

export default defineComponent({
    components: { Plus, Document, More },
    setup() {
        const router = useRouter();

        const files = ref<FileData[]>([]);
        const dialogVisible = ref(false); // 控制弹出框的显示与隐藏
        const knowledgeBaseName = ref(""); // 存储知识库名称

        // 打开弹出框
        const openDialog = () => {
            console.log('打开弹出框');
            dialogVisible.value = true;
        };

        // 初始化时获取知识库数据
        const fetchKnowledgeBases = async () => {
            try {
                const response: any = await getRequest('http://localhost:9988/v1/api/mark/knowledgebase/');
                if (response.code === 200) {
                    files.value = [];  // 清空files
                    response.data.forEach((kb: any) => {
                        files.value.push({
                            id: kb.id,
                            name: kb.knowledgeBaseName,
                            details: 'xxx 文档 | xxx 千字符 | xxx 关联对话' // 示例细节
                        });
                    });
                } else {
                    console.error('获取知识库数据失败:', response.message);
                }
            } catch (error) {
                console.error('请求失败:', error);
            }
        };

        // 初始化时加载知识库数据
        onMounted(fetchKnowledgeBases);

        // 创建知识库
        const createKnowledgeBase = async () => {
            try {
                const response: any = await postRequest('http://localhost:9988/v1/api/mark/knowledgebase/', {
                    base_name: knowledgeBaseName.value || "default"
                });

                if (response.code === 200 && response.data.length > 0) {
                    const id = response.data[0].knowledgeBase_id;
                    router.push(`/manager/${id}/create`);
                    dialogVisible.value = false;
                    knowledgeBaseName.value = "";
                } else {
                    console.error('创建知识库失败:', response.message);
                }
            } catch (error) {
                console.error('请求创建知识库失败:', error);
            }
        };

        const goToKnowledgeBase = (id: string) => {
            router.push(`/manager/${id}`);
        };

        const handleMenuCommand = (file: FileData) => async (command: string) => {
            if (command === 'settings') {
                router.push(`/manager/${file.id}/settings`);
            } else if (command === 'delete') {
                try {
                    const response: any = await deleteRequest(`http://localhost:9988/v1/api/mark/knowledgebase/${file.id}`);
                    if (response.code === 200) {
                        const index = files.value.findIndex(f => f.id === file.id);
                        if (index !== -1) files.value.splice(index, 1);
                        console.log('删除成功:', response.message);
                        await fetchKnowledgeBases();
                    } else {
                        console.error('删除失败:', response.message);
                    }
                } catch (error) {
                    console.error('删除请求失败:', error);
                }
            }
        };

        return {
            files,
            dialogVisible,
            knowledgeBaseName,
            openDialog,
            createKnowledgeBase,
            goToKnowledgeBase,
            handleMenuCommand
        };
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
<template>
    <el-row class="page-content">
        <!-- Sidebar -->
        <el-col :span="4" class="sidebar">
            <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" background-color="#f3f3f4"
                text-color="#303133" active-text-color="#409EFF">
                <el-menu-item index="1" @click="toggleSwitch('1')">
                    <el-icon>
                        <Document />
                    </el-icon>
                    <span slot="title">文档</span>
                </el-menu-item>

                <el-menu-item index="2" @click="toggleSwitch('2')">
                    <el-icon>
                        <Setting />
                    </el-icon>
                    <span slot="title">设置</span>
                </el-menu-item>
            </el-menu>
        </el-col>

        <!-- Main content -->
        <el-col :span="20" class="main-content">
            <div class="documentBox" v-if="switchButton === '1'">
                <!-- Header -->
                <div class="header">
                    <el-input v-model="searchText" placeholder="搜索" class="search-input" clearable />
                    <el-button type="primary" icon="el-icon-plus" @click="addFile">
                        添加文件
                    </el-button>
                </div>

                <!-- Table -->
                <el-table :data="files" style="width: 100%" class="file-table">
                    <el-table-column prop="index" label="#" width="50"></el-table-column>
                    <el-table-column prop="name" label="文件名" width="300" v-slot="scope">
                        <el-icon>
                            <Document />
                        </el-icon>
                        <span class="file-name">{{ scope.row.name }}</span>
                    </el-table-column>
                    <el-table-column prop="size" label="字符数"></el-table-column>
                    <el-table-column prop="recalls" label="召回次数"></el-table-column>
                    <el-table-column prop="uploadDate" label="上传时间"></el-table-column>
                    <el-table-column prop="status" label="状态" width="100">
                        <template v-slot="scope">
                            <el-tag :type="scope.row.status === '可用' ? 'success' : 'warning'">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="100">
                        <template v-slot="scope">
                            <el-dropdown trigger="click">
                                <span class="el-dropdown-link">
                                    <el-icon>
                                        <More />
                                    </el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item>重命名</el-dropdown-item>
                                        <!-- <el-dropdown-item>分段设置</el-dropdown-item> -->
                                        <el-dropdown-item>归档</el-dropdown-item>
                                        <el-dropdown-item>删除</el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="settingBox" v-else>
                <el-form :model="settings" label-width="120px">
                    <el-form-item label="知识库名字">
                        <el-input v-model="settings.knowledgeBaseName" placeholder="请输入知识库名字" />
                    </el-form-item>
                    <el-form-item label="RAG模式">
                        <el-radio-group v-model="settings.rag_model">
                            <el-radio label="0">混合检索（向量+模糊查询）</el-radio>
                            <el-radio label="1">向量检索</el-radio>
                            <el-radio label="2">模糊检索</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="启用二阶段重排">
                        <el-switch v-model="settings.is_rerank" />
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="saveSettings">保存设置</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';
import { getRequest, postRequest, putRequest } from '@/utils/http';

interface File {
    index: number;
    name: string;
    size: string;
    recalls: number;
    uploadDate: string;
    status: string;
    docId: string;
}

export default defineComponent({
    setup() {
        const router = useRouter();
        const route = useRoute();
        const switchButton = ref('1');
        const activeMenu = ref('1');
        const searchText = ref('');
        const files = ref<File[]>([]);

        const settings = ref({
            knowledgeBaseId:"",
            knowledgeBaseName: '',
            rag_model: 0,
            is_rerank: false
        });

        // 获取文档列表并获取每个文档的索引状态
        const fetchFiles = async () => {
            const baseId = route.params.base_id as string;
            try {
                const baseURL = import.meta.env.VITE_APP_BASE_URL;
                const response: any = await getRequest(baseURL+`/v1/api/mark/knowledgebase/${baseId}`);
                if (response.code === 200) {
                    files.value = await Promise.all(response.data.map(async (doc: any, index: number) => {
                        // 获取索引状态
                        const baseURL = import.meta.env.VITE_APP_BASE_URL;
                        const statusResponse: any = await getRequest(
                           baseURL+ `/v1/api/mark/knowledgebase/${baseId}/doc/${doc.doc_id}/index_status`
                        );
                        const status = statusResponse.code === 200 && statusResponse.data[0].index_status === 1 ? '可用' : '未索引';
                        return {
                            index: index + 1,
                            name: doc.doc_name,
                            size: (doc.doc_size / 1024).toFixed(1) + 'k',
                            recalls: 0,
                            uploadDate: new Date(doc.create_time).toLocaleString(),
                            status,
                            docId: doc.doc_id
                        };
                    }));
                    ElMessage.success(response.message);
                } else {
                    ElMessage.error("Failed to retrieve files.");
                }
            } catch (error) {
                console.error(error);
                ElMessage.error("Error fetching documents.");
            }
        };

        const get_kb_config = async () => {
            const baseId = route.params.base_id as string;
            try {
                const baseURL = import.meta.env.VITE_APP_BASE_URL;
                const response: any = await getRequest(baseURL+`/v1/api/mark/knowledgebase/${baseId}/config`);
                if (response.code === 200) {
                    settings.value = response.data[0];
                } else {
                    ElMessage.error("Failed to retrieve settings.");
                }
            } catch (error) {
                console.error(error);
                ElMessage.error("Error fetching settings.");
            }
        };

        const toggleSwitch = (menuIndex: string) => {
            if (switchButton.value !== menuIndex) {
                switchButton.value = menuIndex;
                activeMenu.value = menuIndex;
                ElMessage.info(`切换到${menuIndex === '1' ? '文档' : '设置'}`);
            }
        };

        const addFile = () => {
            const baseId = route.params.base_id as string;
            router.push(`/manager/${baseId}/create`);
        };

        const saveSettings = async () => {
            const baseId = route.params.base_id as string;
            settings.value.knowledgeBaseId = baseId;
            try {
                const baseURL = import.meta.env.VITE_APP_BASE_URL;
                const response: any = await putRequest(baseURL+`/v1/api/mark/knowledgebase/${baseId}/config`, settings.value);
                if (response.code === 200) {
                    ElMessage.success("设置已保存");
                } else {
                    ElMessage.error("保存设置失败");
                }
            } catch (error) {
                console.error(error);
                ElMessage.error("保存设置时出错");
            }
        };

        onMounted(() => {
            fetchFiles();
            get_kb_config();
        });

        return {
            switchButton,
            activeMenu,
            searchText,
            files,
            toggleSwitch,
            addFile,
            settings,
            saveSettings,
            get_kb_config
        };
    }
});
</script>


<style scoped>
.page-content {
    display: flex;
    height: 100vh;
}

.sidebar {
    background-color: #f3f3f4;
    padding: 20px 0;
}

.main-content {
    padding: 20px;
    background-color: white;
}

.header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.search-input {
    width: 300px;
}

.file-table {
    background-color: white;
}

.file-name {
    margin-left: 10px;
}

.more-actions {
    cursor: pointer;
}

/* 在小屏幕下调整布局 */
@media screen and (max-width: 768px) {
  .page-content {
    flex-direction: column;
  }

  .sidebar,
  .main-content {
    width: 100%;
  }
}
</style>
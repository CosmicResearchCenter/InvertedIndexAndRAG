<template>
    <el-row class="page-content">
        <!-- Sidebar -->
        <el-col :span="4" class="sidebar">
            <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" background-color="#f3f3f4" text-color="#303133"
                active-text-color="#409EFF">
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
                            <el-tag v-if="scope.row.status === 'available'" type="success">可用</el-tag>
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
                                        <el-dropdown-item>分段设置</el-dropdown-item>
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
                这是设置
            </div>
        </el-col>
    </el-row>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';
import { getRequest } from '@/utils/http';

interface File {
    index: number;
    name: string;
    size: string;
    recalls: number;
    uploadDate: string;
    status: string;
}

export default defineComponent({
    setup() {
        const router = useRouter();
        const route = useRoute();
        const switchButton = ref('1');
        const activeMenu = ref('1');
        const searchText = ref('');
        const files = ref<File[]>([]);

        // Fetch documents from the backend API
        const fetchFiles = async () => {
            const baseId = route.params.id as string;
            try {
                const response:any = await getRequest(`http://localhost:9988/v1/api/mark/knowledgebase/${baseId}`);
                if (response.code === 200) {
                    files.value = response.data.map((doc: any, index: number) => ({
                        index: index + 1,
                        name: doc.doc_name,
                        size: (doc.doc_size / 1024).toFixed(1) + 'k', // Convert size to kB
                        recalls: 0, // Set default or calculate based on your logic
                        uploadDate: new Date(doc.create_time).toLocaleString(),
                        status: 'available',
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

        const toggleSwitch = (menuIndex: string) => {
            if (switchButton.value !== menuIndex) {
                switchButton.value = menuIndex;
                activeMenu.value = menuIndex;
                ElMessage.info(`切换到${menuIndex === '1' ? '文档' : '设置'}`);
            }
        };

        const addFile = () => {
            router.push('/manager/12/create');
        };

        onMounted(() => {
            fetchFiles();
        });

        return {
            switchButton,
            activeMenu,
            searchText,
            files,
            toggleSwitch,
            addFile
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
</style>
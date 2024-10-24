<template>
    <el-row :gutter="20">
        <!-- Create new knowledge base card -->
        <el-col :span="8" class="col-card">
            <el-card class="new-base" shadow="hover">
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
            <el-card class="box-card" shadow="hover">
                <div class="card-content">
                    <el-icon :size="60">
                        <Document />
                    </el-icon>
                    <div>{{ file.name }}</div>
                    <div>{{ file.details }}</div>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
export default {
    data() {
        return {
            // Sample data for your files
            files: [
                { name: '常用校园信息集合.txt', details: '1 文档 | 1 千字符 | 0 关联应用' },
                { name: '常用校园信息集合.txt', details: '1 文档 | 1 千字符 | 0 关联应用' },
                { name: '常用校园信息集合.txt', details: '1 文档 | 1 千字符 | 0 关联应用' },
                { name: '常用校园信息集合.docx', details: '1 文档 | 8 千字符 | 1 关联应用' },
                { name: '常用校园信息集合.txt', details: '1 文档 | 19 千字符 | 0 关联应用' }
            ]
        };
    }
};
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
</style>
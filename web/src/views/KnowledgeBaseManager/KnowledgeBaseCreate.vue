<template>
    <div class="container">
      <!-- Sidebar -->
      <el-aside width="240px" class="sidebar">
        <el-steps direction="vertical" :active="currentStep">
          <el-step title="选择上次文件"></el-step>
          <el-step title="选择数据源"></el-step>
          <el-step title="文本分段与清洗"></el-step>
          <el-step title="处理并完成"></el-step>
        </el-steps>
      </el-aside>
  
      <!-- Main Content -->
      <el-main class="main-content">
        <el-row>
          <!-- Step 1: Last File -->
          <el-col v-if="currentStep === 1" :span="16" class="file-selection">
            <h3>选择上次文件</h3>
            <el-card shadow="hover" v-for="(file, index) in lastFiles" :key="index" @click="selectFile(file)">
              <p>文件名称: {{ file.name }}</p>
              <p>处理时间: {{ file.processedAt }}</p>
            </el-card>
            <el-button type="primary" @click="proceedToStep(2)">跳过并选择新的数据源</el-button>
          </el-col>
  
          <!-- Step 2 and onwards -->
          <el-col v-else :span="16" class="segmentation-options">
            <template v-if="currentStep === 2">
              <h3>选择数据源</h3>
              <!-- 其他数据源选择内容 -->
              <el-button type="primary" @click="proceedToStep(3)">下一步</el-button>
            </template>
  
            <template v-else-if="currentStep === 3">
              <h3>文本分段与清洗</h3>
              <div class="section">
                <h4>分段设置</h4>
                <el-radio-group v-model="segmentationMethod">
                  <el-radio :label="1">
                    <el-card shadow="hover">
                      <h5>自动分段与清洗</h5>
                      <p>自动设置分段规则与预处理。</p>
                    </el-card>
                  </el-radio>
                  <el-radio :label="2">
                    <el-card shadow="hover">
                      <h5>自定义</h5>
                      <p>自定义分段规则和预处理参数。</p>
                    </el-card>
                  </el-radio>
                </el-radio-group>
              </div>
  
              <div class="section">
                <h4>索引方式</h4>
                <el-radio-group v-model="indexingMethod">
                  <el-radio :label="1">
                    <el-card shadow="hover">
                      <h5>高质量</h5>
                      <p>调用高质量嵌入入口，提高查询准确度。</p>
                    </el-card>
                  </el-radio>
                  <el-radio :label="2">
                    <el-card shadow="hover">
                      <h5>采用 Q&A 分段模式</h5>
                      <el-select v-model="language" placeholder="分段使用的语言">
                        <el-option label="Chinese" value="chinese"></el-option>
                        <el-option label="English" value="english"></el-option>
                      </el-select>
                    </el-card>
                  </el-radio>
                </el-radio-group>
              </div>
  
              <div class="section">
                <h4>检索设置</h4>
                <el-card shadow="hover">
                  <h5>混合检索</h5>
                  <p>利用参考内容和算法获取最优结果。</p>
                  <el-checkbox v-model="useRank" label="使用 Rank 模型"></el-checkbox>
                  <p>模型: bge-reranker-large | Top K: 3 | Score 阈值: 0.8</p>
                </el-card>
              </div>
  
              <el-button type="primary" @click="handleSave">保存并处理</el-button>
              <el-button type="default" @click="proceedToStep(2)">上一步</el-button>
            </template>
          </el-col>
  
          <!-- Segmentation Preview -->
          <el-col :span="8" class="preview-panel" v-if="currentStep === 3">
            <h4>分段预览</h4>
            <el-card shadow="hover" v-for="(segment, index) in segments" :key="index" class="segment-card">
              <p># {{ index + 1 }} {{ segment.title }}</p>
              <p>{{ segment.content }}</p>
              <el-divider></el-divider>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { ElMessage } from 'element-plus';
  
  export default defineComponent({
    name: 'Segmentation',
    setup() {
      const currentStep = ref(1);
      const lastFiles = ref([
        { name: 'file1.txt', processedAt: '2024-10-10 12:34' },
        { name: 'file2.txt', processedAt: '2024-10-12 15:22' }
      ]);
      const segmentationMethod = ref(1);
      const indexingMethod = ref(1);
      const language = ref('chinese');
      const useRank = ref(false);
  
      const segments = ref([
        { title: '汇编语言', content: '汇编语言是一种低级的编程语言...' },
        { title: '系统调用', content: '系统调用是指用户进程通过系统调用与内核交互...' },
        { title: 'Linux 系统调用', content: '您可以在汇编程序中使用 Linux 系统调用...' },
        { title: '贮木指令', content: '贮木指令（INC）是一种加操作...' },
        { title: 'INC 指令', content: 'INC 指令用于将操作数加一...' }
      ]);
  
      const selectFile = (file: any) => {
        ElMessage.success(`已选择文件: ${file.name}`);
        proceedToStep(2);
      };
  
      const proceedToStep = (step: number) => {
        currentStep.value = step;
      };
  
      const handleSave = () => {
        ElMessage.success('处理已保存');
        // Implement save logic here
      };
  
      return {
        currentStep,
        lastFiles,
        segmentationMethod,
        indexingMethod,
        language,
        useRank,
        segments,
        selectFile,
        proceedToStep,
        handleSave
      };
    }
  });
  </script>
  
  <style scoped>
  .container {
    display: flex;
    height: 100vh;
  }
  
  .sidebar {
    background-color: #fff;
    padding: 20px;
  }
  
  .main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px;
    background-color: #f3f3f3;
  }
  
  .segmentation-options {
    padding-right: 20px;
  }
  
  .preview-panel {
    background-color: #fff;
    border-left: 1px solid #e0e0e0;
    padding-left: 20px;
    max-height: 600px;
    overflow-y: auto;
  }
  
  .segment-card {
    margin-bottom: 20px;
  }
  
  .file-selection .el-card {
    margin-bottom: 20px;
    cursor: pointer;
  }
  
  .section {
    margin-bottom: 30px;
  }
  </style>
  
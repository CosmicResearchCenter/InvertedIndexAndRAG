<template>
  <el-container>
    <el-aside width="200px"></el-aside>
    <el-main>
      <el-steps :active="activeStep" align-center finish-status="success">
        <el-step title="选择数据源"></el-step>
        <el-step title="文本分段与清洗"></el-step>
        <el-step title="处理并完成"></el-step>
      </el-steps>

      <!-- 第一步：选择数据源 -->
      <div v-if="activeStep === 1" class="step1">
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :limit="1"
          :auto-upload="false"
          accept=".txt,.md,.pdf,.html,.xlsx,.xls,.docx,.csv,.bin,.py"
          @change="handleFileChange"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">
            拖拽文件至此，或者
            <el-button type="text" @click="uploadFile">选择文件</el-button>
          </div>
          <div class="el-upload__tip" slot="tip">
            已支持TXT, MARKDOWN, PDF, HTML, XLSX, XLS, DOCX, CSV, BIN, PY, 每个文件不超过15MB.
          </div>
        </el-upload>
        <el-card v-if="fileName" class="box-card">
          <div slot="header" class="clearfix">
            <span>{{ fileName }}</span>
          </div>
          <div class="text">文件大小: {{ fileSize }}</div>
        </el-card>
        <el-button style="margin-top: 20px;" type="primary" size="small" @click="nextStep">下一步</el-button>
      </div>

      <!-- 第二步：文本分段与清洗 -->
      <div v-if="activeStep === 2" class="step2">
        <el-row :gutter="20" class="step-content">
          <el-col :span="12">
            <el-card>
              <h3>分段设置</h3>
              <el-radio-group v-model="segmentSetting">
                <el-radio label="auto">自动分段与清洗</el-radio>
                <el-radio label="custom">自定义</el-radio>
              </el-radio-group>
              <el-divider></el-divider>
              <h3>字符数限制</h3>
              <el-input-number v-model="characterLimit" :min="100" :step="100" label="分段字符数" style="width: 100px;"></el-input-number>
              <el-button @click="applyCustomSegment" type="primary" size="small">应用</el-button>
              <el-divider></el-divider>
              <h3>分段模式</h3>
              <el-button type="primary" plain @click="toggleSegmentMode">切换分段模式</el-button>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <h3>分段预览</h3>
              <el-row v-for="(segment, index) in segments" :key="index" class="segment-preview">
                <el-col :span="24">
                  <el-card>
                    <div>段落 # {{ index + 1 }}</div>
                    <div>{{ segment.text }}</div>
                    <div>字数: {{ segment.length }}</div>
                  </el-card>
                </el-col>
              </el-row>
            </el-card>
          </el-col>
        </el-row>
        <el-button style="margin-top: 20px;" type="primary" @click="nextStep">下一步</el-button>
      </div>

      <!-- 第三步：处理并完成 -->
      <div v-if="activeStep === 3" class="step3">
        <el-card>
          <h3>处理完成！</h3>
          <p>你已经完成了所有步骤。</p>
        </el-card>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  setup() {
    const activeStep = ref(1);
    const fileName = ref('');
    const fileSize = ref('');
    const segmentSetting = ref('auto');
    const characterLimit = ref(500);
    const segments = ref([
      { text: '示例文本 1', length: 419 },
      { text: '示例文本 2', length: 436 },
    ]);

    const handleFileChange = (file) => {
      fileName.value = file.name;
      fileSize.value = (file.size / 1024 / 1024).toFixed(2) + ' MB';
    };

    const applyCustomSegment = () => {
      // 调用拆分算法，这里可以实现实际的分段逻辑
      console.log(`将文件按 ${characterLimit.value} 字符分段`);
    };

    const toggleSegmentMode = () => {
      console.log("切换到不同的分段模式");
    };

    const nextStep = () => {
      if (activeStep.value === 1 && !fileName.value) {
        alert("请先选择文件！");
        return;
      }
      if (activeStep.value < 3) {
        activeStep.value += 1;
      }
    };

    return {
      activeStep,
      fileName,
      fileSize,
      segmentSetting,
      characterLimit,
      segments,
      handleFileChange,
      applyCustomSegment,
      toggleSegmentMode,
      nextStep
    };
  }
});
</script>


<style scoped>
.step-content {
  margin-top: 20px;
}
.segment-preview {
  margin-bottom: 10px;
}
</style>

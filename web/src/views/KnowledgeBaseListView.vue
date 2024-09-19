<template>
  <el-space wrap>
      <el-card v-for="i in 3" :key="i" class="box-card" style="width: 250px">
          <template #header>
              <div class="card-header">
                  <span>Card name</span>
                  <el-button class="button" text>Operation button</el-button>
              </div>
          </template>
          <div v-for="o in 4" :key="o" class="text item">
              {{ 'List item ' + o }}
          </div>
      </el-card>
      <el-card class="new-base"  style="width: 200px;height: 200px;">
          新建知识库
      </el-card>
  </el-space>
</template>
<style scoped>
.new-base{
    /* background-color: #f5f7fa; */
    /* border: 1px dashed #e4e7ed; */
    border-radius: 6px;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
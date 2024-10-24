<template>
    <el-row :gutter="20">
        <el-col :span="8" class="col-card" >
            <el-card class="new-base" shadow="hover">
                <el-icon :size="60"><Plus /></el-icon>
            </el-card>
        </el-col>
        <el-col v-for="i in 10" :key="i" :span="8" class="col-card">
            <el-card class="box-card" shadow="hover">
                <div class="card-header">
                    <span>Card name</span>
                    <el-button class="button" text>Operation button</el-button>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>

<style scoped>
.box-card {
    width: 100%;
    height: 200px;
}

.new-base {
    width: 100%;
    height: 200px;
    border-radius: 6px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.col-card {
    margin-bottom: 20px; /* 行与行之间的间隔 */
}
</style>
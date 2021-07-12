<template>
<div>
<el-row :gutter="20">
  <el-col :span="10"><h1>Smart OCR System</h1></el-col>
  <el-col :span="14"><el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item index="1">SmartOCR</el-menu-item>
    <!-- <el-submenu index="2"> 
      <template slot="title">资源中心</template>
      <el-menu-item index="2-1">选项1</el-menu-item>
      <el-menu-item index="2-2">选项2</el-menu-item>
      <el-menu-item index="2-3">选项3</el-menu-item>
      <el-submenu index="2-4">
        <template slot="title">选项4</template>
        <el-menu-item index="2-4-1">选项1</el-menu-item>
        <el-menu-item index="2-4-2">选项2</el-menu-item>
        <el-menu-item index="2-4-3">选项3</el-menu-item>
      </el-submenu>
    </el-submenu>
    <el-menu-item index="3">历史记录</el-menu-item>
    <el-menu-item index="4"
      ><a href="https://" target="_blank">联系我们</a></el-menu-item
    > -->
  </el-menu></el-col>
</el-row>
  
  <div class="line"></div>
  
  <div class="line"></div>
</div>
</template>

<script>
  export default {
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1'
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("//unpkg.com/element-ui@2.15.0/lib/theme-chalk/index.css");
</style>

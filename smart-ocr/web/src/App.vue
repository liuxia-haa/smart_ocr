<template>
  <div id="app">
    <el-container
      v-loading.fullscreen.lock="this.$store.state.loading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
      <el-header><top></top></el-header>
      <el-main>
        <el-row :gutter="20" type="flex">
          <el-col :span="12">
            <OcrManager @node-click="clickArea" @clickCanvas="clickCanvas" />
          </el-col>

          <el-col :span="12">
            <DataModel
              :data="this.$store.state.DataModel.data"
              :chosedDataModel="this.$store.state.chosedDataModel"
              @focus="onFocus"
            />
          </el-col>
        </el-row>
      </el-main>
      <el-footer><bottom></bottom></el-footer>
    </el-container>
  </div>
</template>

<script>
import OcrManager from "./components/OcrManager.vue";
import DataModel from "./components/DataModel.vue";
import top from "./components/top.vue";
import bottom from "./components/bottom.vue";

export default {
  name: "App",
  components: {
    OcrManager,
    DataModel,
    top,
    bottom,
  },
  data() {
    return {
      focus: "",
      data: this.$store.state.DataModel.data,
      mapping: this.$store.state.mapping,
    };
  },
  mounted() {
    this.$store.dispatch("getDataModelList");
  },
  methods: {
    onFocus(e) {
      console.log(e.target.id);
      this.focus = e.target.id;
    },
    clickArea(node) {
      console.log(node);
      this.setMapping(node);
    },
    setMapping(node) {
      var words = "";
      var target = "";
      if (this.focus) {
        if (node.lineContent) {
          words = node.lineContent;
          target = "line";
        }
        if (node.regionContent) {
          words = node.regionContent;
          target = "region";
        }
        this.$store.commit("setDataModel", {
          key: this.focus,
          value: words,
        });
        this.$store.commit("addmapping", {
          key: this.focus,
          box: node.boundingBox,
          target: target,
        });
      }
    },
    clickCanvas(node) {
      console.log(node);
      if (node) {
        this.setMapping(node);
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}

.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: left;
  line-height: 10px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>

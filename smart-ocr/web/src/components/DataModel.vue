
<template>
  <div class="grid-content bg-purple-light">
    <h1>数据模版</h1>
    <div class="line"></div>
    <el-form ref="form" label-position="right" label-width="180px">
      <p v-if="JSON.stringify(data) == '{}'">暂无模版数据，请选择模版!</p>
      <p v-if="JSON.stringify(data) == '{}' && chosedDataModel == 0">
        请添加模版数据项!
      </p>
      <el-form-item
        v-for="(value, name, index) in data"
        :key="index"
        :label="name"
      >
        <el-input
          :id="name"
          type="text"
          class="input"
          v-model="data[name]"
          v-on="listeners"
        ></el-input>
      </el-form-item>
      <h2>模版管理</h2>
      <div class="line"></div>
      <el-form-item label="数据项的ID:">
        <el-input
          type="text"
          class="input"
          placeholder="请输入数据项的ID"
          v-model="ItemName"
        ></el-input>
      </el-form-item>
      <el-form-item label="数据项的默认值:">
        <el-input
          type="text"
          class="input"
          placeholder="请输入数据项的默认值"
          v-model="ItemValue"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="addItem">添加数据项</el-button>
        <el-button type="primary" @click="deleteItem">删除数据项</el-button>
        <el-button type="primary" @click="saveDataModel">保存模版</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  props: ["data", "chosedDataModel"],
  data() {
    return {
      ItemName: "",
      ItemValue: "",
      loading: false,
    };
  },
  computed: {
    listeners() {
      return {
        // Pass all component listeners directly to input
        ...this.$listeners,
        // Override input listener to work with v-model
        input: (event) => {
          console.log(event);
          this.$emit("input", event);
        },
      };
    },
  },
  methods: {
    addItem() {
      this.$store.commit("setDataModel", {
        key: this.ItemName,
        value: this.ItemValue,
      });
    },
    deleteItem() {
      this.$store.commit("delDataModel", {
        key: this.ItemName,
      });
    },
    saveDataModel() {
      this.$confirm("此操作将当前配置保存为模版, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$store.dispatch("saveDataModel").then(() => {
            this.$message({
              type: "success",
              message: "保存成功!",
            });
            this.$alert(
              "POST /api/model/" +
                this.$store.state.chosedDataModel +
                " and Image input name='file', Smart OCR API Demo see /api_test.html",
              "Smart OCR API",
              {
                dangerouslyUseHTMLString: true,
              }
            );
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消保存",
          });
        });
    },
  },
};
</script>

<style lang="scss" scoped>
</style>

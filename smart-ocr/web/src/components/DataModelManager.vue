<template>
  <div>
    <el-tag
      :key="tag.id"
      :type="tag.id == chosedDataModel ? '' : 'info'"
      v-for="tag in dataModelList"
      closable
      :disable-transitions="false"
      @close="handleClose(tag)"
      @click="clickTag(tag)"
    >
      {{ tag.label }}
    </el-tag>
    <el-input
      class="input-new-tag"
      v-if="inputVisible"
      v-model="inputValue"
      ref="saveTagInput"
      size="small"
      @keydown.enter.native="handleInputConfirm"
      @blur="handleInputConfirm"
    >
    </el-input>
    <el-button v-else class="button-new-tag" size="small" @click="showInput"
      >+ New Tag</el-button
    >
  </div>
</template>

<script>
export default {
  name: "datamodelmanager",
  props: ["dataModelList", "chosedDataModel"],
  data() {
    return {
      inputVisible: false,
      inputValue: "",
    };
  },
  methods: {
    handleClose(tag) {
      this.$confirm("此操作将永久删除该模版, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          if (tag.id == 0) {
            this.dataModelList.splice(this.dataModelList.indexOf(tag), 1);
          } else {
            this.$store.dispatch("rmDataModel", tag.id);
          }
          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },

    showInput() {
      this.inputVisible = true;
      this.$nextTick(() => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    clickTag(tag) {
      console.log(this.dataModelList);
      console.log(tag);
      this.$store.dispatch("getDataModel", tag.id);
    },
    handleInputConfirm() {
      console.log("handleInputConfirm");
      let inputValue = this.inputValue;

      if (inputValue) {
        for (let i = 0; i < this.dataModelList.length; i++) {
          if (this.dataModelList[i].id == 0) {
            this.handleClose(this.dataModelList[i]);
          }
        }
        this.dataModelList.push({ id: 0, label: inputValue });
        this.$store.dispatch("getDataModel", 0);
      }
      this.inputVisible = false;
      this.inputValue = "";
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

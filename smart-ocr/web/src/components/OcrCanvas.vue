<template>
  <div class="grid-content bg-purple-light">
    <el-radio-group v-model="direction">
      <el-radio label="ltr">从左往右开</el-radio>
      <el-radio label="rtl">从右往左开</el-radio>
      <el-radio label="ttb">从上往下开</el-radio>
      <el-radio label="btt">从下往上开</el-radio>
    </el-radio-group>

    <el-button
      @click="myCanvas = true"
      type="primary"
      style="margin-left: 16px"
    >
      显示图片
    </el-button>
    <el-drawer
      :title="drawerTitle"
      :modal="false"
      :visible.sync="myCanvas"
      :direction="direction"
      @open="openDrawer"
      @opened="openedDrawer"
      size="60%"
    >
      <canvas ref="myCanvas" v-on:click="clickCanvas"
        >您的浏览器不支持 HTML5 canvas 标签。</canvas
      >
    </el-drawer>
  </div>
</template>

<script>
import util from "../util/util";
export default {
  name: "ocrcanvas",
  props: ["picture", "ocrdata"],
  data() {
    return {
      myCanvas: false,
      drawerTitle: "图片方式显示OCR识别出来的各目标区域",
      direction: "ltr",
      img: new Image(), // 背景图片缓存
      context: {}, // canvas对象
    };
  },
  methods: {
    openDrawer() {
      console.log("openDrawer");
      this.img.src = this.picture;
    },
    openedDrawer() {
      console.log("openedDrawer");
      if (this.ocrdata == "" || this.picture == "") {
        this.drawerTitle = "当前没有要显示的图片和数据！";
      } else {
        this.initDraw();
      }
    },
    initDraw() {
      // 初始化画布
      console.log("initDraw");
      const canvas = this.$refs.myCanvas;
      this.context = canvas.getContext("2d");
      canvas.setAttribute("width", this.img.width);
      canvas.setAttribute("height", this.img.height);
      this.context.drawImage(this.img, 0, 0, this.img.width, this.img.height);
      //准备绘制
      this.context.strokeStyle = "red";
      this.context.beginPath();

      for (var i = 0; i < this.ocrdata.regions.length; i++) {
        for (var j = 0; j < this.ocrdata.regions[i].lines.length; j++) {
          var boundingBox = util.BoxStr2ArrayInt(
            this.ocrdata.regions[i].lines[j].boundingBox
          );
          var wigth = boundingBox[2];
          var height = boundingBox[3];
          this.context.rect(boundingBox[0], boundingBox[1], wigth, height);
        }
      }
      this.context.stroke();
    },
    clickCanvas(e) {
      console.log(e.offsetX, e.offsetY);
      var node = util.findBox(this.ocrdata, { x: e.offsetX, y: e.offsetY });
      this.$emit("clickCanvas", node);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

<template>
  <div class="grid-content bg-purple-light">
    <el-tabs v-model="activeTab" type="card">
      <el-tab-pane label="上传图片" name="first">
        <el-form ref="form" label-width="80px">
          <el-form-item label="选择模版">
            <DataModelManager
              :dataModelList="this.$store.state.dataModelList"
              :chosedDataModel="this.$store.state.chosedDataModel"
            ></DataModelManager>
          </el-form-item>
          <el-form-item label="选择图片">
            <el-upload
              class="upload-demo"
              drag
              :action="this.$store.getters.uploadUrl"
              multiple
              list-type="picture"
              :limit="1"
              :on-exceed="handleExceed"
              :before-upload="beforeUpload"
              :on-success="handleSuccess"
              :on-error="handleError"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
              <div class="el-upload__tip" slot="tip">
                只能上传jpg/png文件，且不超过500kb
              </div>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="识别结果" name="second">
        <OcrCanvas
          :picture="this.imageUrl"
          :ocrdata="this.ocrdata"
          @clickCanvas="clickCanvas"
        ></OcrCanvas>

        <el-tree
          :data="ocrdata.regions"
          :props="defaultProps"
          highlight-current
          default-expand-all
          accordion
          v-on="listeners"
        >
        </el-tree>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import Vue from "vue";
import DataModelManager from "./DataModelManager.vue";
import OcrCanvas from "./OcrCanvas.vue";
import util from "../util/util";
export default {
  name: "ocrshow",
  components: {
    DataModelManager,
    OcrCanvas,
  },
  data() {
    return {
      ocrdata: "",
      imageUrl: "",
      activeTab: "first",
      defaultProps: {
        children: "lines",
        label: "lineContent",
      },
    };
  },
  methods: {
    clickCanvas(e) {
      this.$emit("clickCanvas", e);
    },
    handleExceed() {
      this.$message.warning(`当前限制选择 1 个文件，请先移除文件。`);
    },
    beforeUpload(file) {
      console.log(file);
    //   const isJPG = file.type === "image/jpeg" || file.type === "image/png";
    //   const isLt2M = file.size / 1024 / 1024 < 2;

    //   if (!isJPG) {
    //     this.$message.error("上传头像图片只能是 JPG/PNG 格式!");
    //   }
    //   if (!isLt2M) {
    //     this.$message.error("上传头像图片大小不能超过 2MB!");
    //   }
    //   return isJPG && isLt2M;
    },
    handleError() {
      if (Vue.config.productionTip == false) {
        this.handleSuccess({"fid": "6037b71dbdafd7c59a62d189", "filename": "systemFlow.png", "model": {"DataModel": {"data": {"default": "value"}}, "id": 0, "mapping": {"relation": []}, "name": "default"}, "ocrdata": {"Result": {"exif": "UP", "orientation": "UP", "regions": [{"boundingBox": "239,30,270,30,270,48,239,48", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "239,30,270,30,270,48,239,48", "lang": "zh", "text": "开始", "text_height": 18, "words": [{"boundingBox": "239,30,252,30,252,48,239,48", "word": "开"}, {"boundingBox": "257,30,270,30,270,48,257,48", "word": "始"}]}]}, {"boundingBox": "31,140,106,140,106,158,31,158", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "31,140,106,140,106,158,31,158", "lang": "zh", "text": "人工匹配操作", "text_height": 17, "words": [{"boundingBox": "31,141,43,141,43,158,31,158", "word": "人"}, {"boundingBox": "47,141,56,141,56,158,47,158", "word": "工"}, {"boundingBox": "60,141,69,140,69,157,60,158", "word": "匹"}, {"boundingBox": "73,140,81,140,81,157,73,157", "word": "配"}, {"boundingBox": "85,140,94,140,94,157,85,157", "word": "操"}, {"boundingBox": "98,140,106,140,106,157,98,157", "word": "作"}]}]}, {"boundingBox": "198,125,312,125,312,171,198,171", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "198,125,311,125,311,144,198,144", "lang": "zh", "text": "坐标位置与数据对象", "text_height": 17, "words": [{"boundingBox": "198,126,210,126,210,143,198,143", "word": "坐"}, {"boundingBox": "214,126,223,126,223,143,214,143", "word": "标"}, {"boundingBox": "227,126,236,126,236,143,227,143", "word": "位"}, {"boundingBox": "240,126,248,125,248,142,240,143", "word": "置"}, {"boundingBox": "252,125,257,125,257,142,252,142", "word": "与"}, {"boundingBox": "261,125,269,125,269,142,261,142", "word": "数"}, {"boundingBox": "274,125,282,125,282,142,274,142", "word": "据"}, {"boundingBox": "286,126,295,126,295,143,286,143", "word": "对"}, {"boundingBox": "299,126,311,127,311,144,299,143", "word": "象"}]}, {"boundingBox": "198,140,312,140,312,158,198,158", "lang": "zh", "text": "的人工匹配系统支持", "text_height": 17, "words": [{"boundingBox": "198,141,210,140,210,157,198,158", "word": "的"}, {"boundingBox": "215,140,223,140,223,157,215,157", "word": "人"}, {"boundingBox": "227,140,236,140,236,157,227,157", "word": "工"}, {"boundingBox": "240,140,249,140,249,157,240,157", "word": "匹"}, {"boundingBox": "253,140,257,140,257,157,253,157", "word": "配"}, {"boundingBox": "261,140,270,140,270,157,261,157", "word": "系"}, {"boundingBox": "274,141,283,141,283,158,274,158", "word": "统"}, {"boundingBox": "287,141,295,141,295,158,287,158", "word": "支"}, {"boundingBox": "300,140,312,140,312,157,300,157", "word": "持"}]}, {"boundingBox": "239,154,271,154,271,171,239,171", "lang": "zh", "text": "方法", "text_height": 17, "words": [{"boundingBox": "239,154,251,154,251,171,239,171", "word": "方"}, {"boundingBox": "255,154,271,154,271,171,255,171", "word": "法"}]}]}, {"boundingBox": "22,238,98,238,98,259,22,259", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "22,238,98,238,98,259,22,259", "lang": "zh", "text": "OCR坐标数据", "text_height": 18, "words": [{"boundingBox": "22,241,49,240,49,258,22,259", "word": "OCR"}, {"boundingBox": "53,240,58,240,58,258,53,258", "word": "坐"}, {"boundingBox": "62,239,71,239,71,257,62,257", "word": "标"}, {"boundingBox": "76,239,80,239,80,257,76,257", "word": "数"}, {"boundingBox": "85,239,98,238,98,256,85,257", "word": "据"}]}]}, {"boundingBox": "216,238,294,238,294,257,216,257", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "216,238,294,238,294,257,216,257", "lang": "zh", "text": "映射关系数据", "text_height": 18, "words": [{"boundingBox": "216,238,229,238,229,256,216,256", "word": "映"}, {"boundingBox": "233,238,242,238,242,256,233,256", "word": "射"}, {"boundingBox": "246,238,251,239,251,257,246,256", "word": "关"}, {"boundingBox": "255,239,264,239,264,257,255,257", "word": "系"}, {"boundingBox": "268,239,277,239,277,257,268,257", "word": "数"}, {"boundingBox": "281,239,294,239,294,257,281,257", "word": "据"}]}]}, {"boundingBox": "386,239,467,239,467,256,386,256", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "386,239,467,239,467,256,386,256", "lang": "zh", "text": "自定义数据格式", "text_height": 17, "words": [{"boundingBox": "386,239,394,239,394,256,386,256", "word": "自"}, {"boundingBox": "398,239,406,239,406,256,398,256", "word": "定"}, {"boundingBox": "410,239,418,239,418,256,410,256", "word": "义"}, {"boundingBox": "422,239,431,239,431,256,422,256", "word": "数"}, {"boundingBox": "435,239,439,239,439,256,435,256", "word": "据"}, {"boundingBox": "443,239,455,239,455,256,443,256", "word": "格"}, {"boundingBox": "459,239,467,239,467,256,459,256", "word": "式"}]}]}, {"boundingBox": "198,325,311,325,311,372,198,372", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "198,325,311,325,311,344,198,344", "lang": "zh", "text": "对映射关系数据的解", "text_height": 17, "words": [{"boundingBox": "198,327,210,326,210,343,198,344", "word": "对"}, {"boundingBox": "214,326,223,325,223,342,214,343", "word": "映"}, {"boundingBox": "227,325,236,325,236,342,227,342", "word": "射"}, {"boundingBox": "240,325,248,325,248,342,240,342", "word": "关"}, {"boundingBox": "252,325,257,325,257,342,252,342", "word": "系"}, {"boundingBox": "261,325,269,325,269,342,261,342", "word": "数"}, {"boundingBox": "274,325,282,326,282,343,274,342", "word": "据"}, {"boundingBox": "286,326,295,326,295,343,286,343", "word": "的"}, {"boundingBox": "299,326,311,327,311,344,299,343", "word": "解"}]}, {"boundingBox": "198,340,311,340,311,357,198,357", "lang": "zh", "text": "释执行及数据的自动", "text_height": 17, "words": [{"boundingBox": "198,340,210,340,210,357,198,357", "word": "释"}, {"boundingBox": "214,340,223,340,223,357,214,357", "word": "执"}, {"boundingBox": "227,340,236,340,236,357,227,357", "word": "行"}, {"boundingBox": "240,340,244,340,244,357,240,357", "word": "及"}, {"boundingBox": "248,340,261,340,261,357,248,357", "word": "数"}, {"boundingBox": "265,340,269,340,269,357,265,357", "word": "据"}, {"boundingBox": "274,340,282,340,282,357,274,357", "word": "的"}, {"boundingBox": "286,340,295,340,295,357,286,357", "word": "自"}, {"boundingBox": "299,340,311,340,311,357,299,357", "word": "动"}]}, {"boundingBox": "236,354,275,354,275,372,236,372", "lang": "zh", "text": "化转换", "text_height": 18, "words": [{"boundingBox": "236,354,244,354,244,372,236,372", "word": "化"}, {"boundingBox": "249,354,258,354,258,372,249,372", "word": "转"}, {"boundingBox": "262,354,275,354,275,372,262,372", "word": "换"}]}]}, {"boundingBox": "223,440,302,440,302,458,223,458", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "223,440,302,440,302,458,223,458", "lang": "zh", "text": "转换结果数据", "text_height": 18, "words": [{"boundingBox": "223,440,236,440,236,458,223,458", "word": "转"}, {"boundingBox": "240,440,249,440,249,458,240,458", "word": "换"}, {"boundingBox": "254,440,263,440,263,458,254,458", "word": "结"}, {"boundingBox": "267,440,271,440,271,458,267,458", "word": "果"}, {"boundingBox": "276,440,285,440,285,458,276,458", "word": "数"}, {"boundingBox": "289,440,302,440,302,458,289,458", "word": "据"}]}]}, {"boundingBox": "248,530,279,530,279,548,248,548", "dir": "h", "lang": "zh", "lines": [{"boundingBox": "248,530,279,530,279,548,248,548", "lang": "zh", "text": "结束", "text_height": 18, "words": [{"boundingBox": "248,530,261,530,261,548,248,548", "word": "结"}, {"boundingBox": "266,530,279,530,279,548,266,548", "word": "束"}]}]}], "scene": "screen_shot"}, "errorCode": "0", "requestId": "b1e98658-d18e-4781-b0bc-8ad87e4cf380"}});
      }
    },
    handleSuccess(res) {
      console.log(res);
      var ocrdata = res.ocrdata;
      this.imageUrl = "/file/" + res.fid;
      if (ocrdata.errorCode == "0") {
        this.setOcrData(ocrdata.Result);
        this.$store.commit("changeDataModel", res.model);
      } else {
        this.$message.error("OCR ERROR:" + ocrdata.msg);
      }
      console.log(this.ocrdata);
      this.activeTab = "second";
    },
    setOcrData(ocrdata) {
      // 在线OCR API
      // http://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
      // 即识别结果主要在Result中，输出结构为：regions->lines->words.一个文档可能有多个region，代表段落，一个段落有多行，一行有多个字。
      // 每个段落、每行、每个字都有boundingBox，代表能够框住段落、行、字的最大box的位置信息。
      // boundingBox：共八个值：分别是左上角坐标(x,y)，右上角坐标(x,y)，右下角坐标(x,y)，左下角(x,y)。
      // text：每行中有text存储识别的文本内容
      // 离线OCR API
      // boundingBox: 文本块相对于原始图片的坐标信息，是4个整数以逗号 分隔的方式组成的字符串，4个整数从左到右分别代表文本块的左 上⻆ 横坐标、左上⻆纵坐标、宽度、高度;
      // lineContent: 文本行中的文本信息;
      // 根据以上两种JSON格式统一转换为：
    //   {
    //      regions:[{
    //          boundingBox:"左上⻆横坐标、左上⻆纵坐标、宽度、高度",
    //          lines:[{
    //             boundingBox:"左上⻆横坐标、左上⻆纵坐标、宽度、高度",
    //             lineContent:"文本行中的文本信息"
    //          },
    //          ...
    //          ]
    //      },
    //      ...
    //      ] 
    //   }
      for (var i = 0; i < ocrdata.regions.length; i++) {
        for (var j = 0; j < ocrdata.regions[i].lines.length; j++) {
          var box = util.BoxStr2ArrayInt(
            ocrdata.regions[i].lines[j].boundingBox
          );
          if (box.length == 8) {
            ocrdata.regions[i].lines[j].boundingBox =
              box[0] +
              "," +
              box[1] +
              "," +
              (box[2] - box[0]) +
              "," +
              (box[7] - box[1]);
          }
          if (ocrdata.regions[i].lines[j].text) {
            ocrdata.regions[i].lines[j]["lineContent"] =
              ocrdata.regions[i].lines[j].text;
          }
        }
        box = util.BoxStr2ArrayInt(ocrdata.regions[i].boundingBox);
        if (box.length == 8) {
          ocrdata.regions[i].boundingBox =
            box[0] +
            "," +
            box[1] +
            "," +
            (box[2] - box[0]) +
            "," +
            (box[7] - box[1]);
        }
        if (ocrdata.regions[i].text) {
          ocrdata.regions[i]["regionContent"] = ocrdata.regions[i].text;
        }
      }
      this.ocrdata = ocrdata;
    },
  },
  computed: {
    listeners() {
      return {
        // Pass all component listeners directly to p
        ...this.$listeners,
      };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>

# smart-ocr

#### 介绍
项目介绍：用户上次一张图片，系统自动进行表单填写。
主要功能：图片上传、获取图片 OCR 结果、标记图片文字识别区域、 训练定制模型、表单自动填写。
实现一个自动填写表单的web软件系统，前端上传图片，后端会将图片识别为json格式的数据，并反馈在前端页面，在图片上标注出各个识别目标并可以点击提取OCR文本。
#### 软件架构

##### server：后端相关代码
+ config.py：定义可接受图片格式、配置端口
+ main.py：响应前端请求，将图片以及识别结果（JSON）传入数据库
+ ocr.py：调用有道OCR API，相关配置信息

##### web：前端相关代码
+ dist：生成打包后文件
+ node_modules：安装的依赖包
+ node_modules：安装的依赖包
+ bottom.vue：copyright
+ DataModel.vue：定义运行界面右侧，数据模板相关组件，实现saveDataModel()、addItem()、deleteItem()等方法
+ DataModelManager.vue：定义DataModel相关管理操作，例如删除模板
+ OcrCanvas.vue：定义运行界面左侧，“识别结果”界面相关vue组件，实现initDraw()、clickCanvas()等方法
+ DataManager.vue：是DataModelManager.vue、OcrCanvas.vue的父组件，实现运行界面左侧界面，定义handleSuccess()、setOcrData()等方法。
+ index.js：导出vuex所有配置
+ utils：封装getOverlapbox()、findBox()、transform()等函数
+ main.js：vue入口函数

#### 安装教程

1.  启动server端
···
sudo ntpdate ntp.ubuntu.com # 虚拟机挂起时常会造成时间不同步，造成OCR时间戳错误
sudo mount -t vboxsf code code # 开发环境下与虚拟机共享目录的挂载命令
sudo systemctl start mongod
sudo python main.py
...
    
2.  启动web端
    然后在终端命令行 cd smart_ocr 文件夹下，进入cd web目录
    安装 Node.js 
    npm install
    npm run serve

#### 使用说明

1.  安装成功后，打开前端页面链接
2.  点击上传图片
3.  即可显示识别信息

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
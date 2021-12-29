# 多功能相册app——BlackPearl
起源
------
应计算机软件基础课程要求，及三位青年人对于人工智能前沿知识探索的欲望，本产品应运而生：**面向设计师的相册整理app——BlackPearl**。   
   
代码部分由**J.C.Maxwell**完成，**一船江月**完成UI设计部分，**游哉**负责整体方向和进度。
  
    
功能介绍
--------
### BlackPearl是一款面向设计师群体，用于管理图片的app，具有如下功能。
#### 主体功能
1. **相似查找：** 对相册中图片进行相似查找，搜索出的相似照片可以选择删除/不删除
   
2. **人物分类：** 对相册中的图片，按照主体人物不同进行分类，获得以同一人物为主体的多个相册    

3. **动物分类：** 对相册中的图片，按照物品不同进行分类，获得以同一物体为主体的多个相册

#### 其他功能  
1.  **自定义相册：** 新建、重命名、删除相册，在相册中添加图片；退出app后图片依然保留  

2.  **回收站：** 删除相册中的照片，并在回收站中恢复删除的照片

3.  **记忆存储：** 对于相册、分类结果、回收站等内容，具有记忆功能
    

操作指南
--------
### 小白式app   
**·** 支持Windows系统，使用时不依赖python/torch/tensorflow等环境，正常下载安装即可使用 

### 下载安装步骤

**·** 在本项目中点击绿色图标“Code”，再点击“Download ZIP"，最后点击“保存文件”。 
    
**·** 下载完成后，点击“BlackPearl”图标，选择安装路径（推荐D盘、E盘、F盘，不推荐C盘），**并用智慧的大脑记住**（下一步用到），进行安装。

**·** 安装完成后，找到上一步的安装路径，下拉寻找到文件名为“BlackPearl”的文件，双击即可运行。

### 使用手册

**·**

**·**

**·**

**·**


原理详解
--------
### 一、界面设计
受Eagle的灵感启发，BlackPearl采用Dracula（中文译为吸血鬼）配色方案    
    
界面布局采用PS进行设计


### 二、后端
#### （一）人脸验证
#### Face Recognition简介：
**·** 目前世界上最简洁的人脸识别库
  
**·** 可使用Python和命令行操作
  
**·** 基于C++开源库dlib中的深度学习模型
  
**·** LFW测试准确率达99.38% 
  
#### 算法流程：
 **1.** 加载图片，转化为RGB三通道格式
  
 **2.** 定位照片中人脸，包括[top, right, bottom, left]，分别代表框住人脸的矩形中左上角和右下角的坐标（x1,y1,x2,y2）。
   
 **3.** 提取人脸中特征，包括nose_bridge、right_eyebrow、right_eye、chine、left_eyebrow、bottom_lip、nose_tip、top_lip、left_eye九部分。每个部分包含若干个特征点(x,y)，总共有68个特征点
   
 **4.** 对68个特征点进行编码，每张人脸获得一个128维向量
 
 **5.** 可匹配两个面部特征编码，利用两个向量的内积（余弦距离）来衡量相似度，大于阈值确认是同一人脸，反之亦然。其中阈值默认值为0.6，可调节。

#### （二）相似查找

**综述：** 采用pHash增强版的低频感知哈希算法，避免伽马校正或颜色直方图被调整带来的影响。获得图片指纹后利用Hamming Distance计算两张图片的相似度。

#### 详细原理如下：
 **1.** 将图片缩小为32×32  
  
 **2.** 将32×32的RGB彩图转换为灰度图   
   
 **3.** 计算图像的DCT变换，获得32×32矩阵  
  
 **4.** 缩小DCT矩阵，取左上角8×8矩阵（包含了最多的信息）  
 
 **5.** 计算8×8 DCT矩阵的均值  
 
 **6.** 将矩阵进行二值处理：如果大于均值，则记为1；反之则记为0   
   
 **7.** 二值图按序组合成64位整型哈希值（指纹） 
 
 **8.** 得到指纹以后，对比不同的图片中64位有多少位不同 
  
 **9.** 如果不相同的数据位不超过5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片

#### （三）物品分类
BlackPearl的物品分类功能 以ResNet34残差神经网络为基础，并在网络顶端添加softmax层，获得11维向量，对应图片为11个动物的可能性。

### 三、前端

BlackPearl的前端采用Qt框架
  
Qt是一款跨平台C++图形用户界面应用程序开发框架，可用于GUI程序的开发，也可用于非GUI程序的开发，如控制台、操作系统等。

此外，Qt下含有大型集成开发环境Qt Creator，为GUI设计提供了便利；Qt Designer中可以拖动组件，进行空间布局，具有良好的可视化，并且能够利用UI文件和Python文件的相互转换，协助前端开发。

致谢
------
产品名为**BlackPearl，黑珍珠**，寓意“最艰辛岁月的结晶，母贝伤痛的泪水，历经磨难所以稀有、高贵”。   
    
在此，感谢现实生活中所有人的帮助，感谢网络中创作者们的知识分享。




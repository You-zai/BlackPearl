<div align=center><img width="600" height="180" src="https://github.com/You-zai/-/blob/main/%E7%99%BD%E9%BB%91%E8%89%B2%E5%A4%A7%E6%A0%87%E9%A2%98%E5%A4%A7%E6%A0%87%E9%A2%98%E9%82%80%E8%AF%B7%E4%B8%AD%E6%96%87LinkedIn%20Banner(1).png"/></div>

Tabel of Contents
----------------
*  **起源**
* **功能介绍**
  * 目标用户
  * 主体功能
  * 其他功能
* **操作指南**
* **原理详解**
  * UI设计
  * 后端
  * 前端
* **致谢**

起源
------

### <div align='center' ><font size='70'>面向设计师的相册整理app——BlackPearl</font></div>   
       
<div align='center' ><font size='70'>代码部分由J.C.Maxwell完成，一船江月完成UI设计部分，游哉把控整体方向和进度。</font></div>
　　
  
    
功能介绍
--------
### BlackPearl是一款面向设计师群体，用于管理图片的app，具有如下功能。
<div align=center><img width="400" height="300" src="https://github.com/You-zai/-/blob/main/%E5%9B%BE%E7%89%878.png"/></div>

#### 主体功能

* **相似查找：** 对相册中图片进行相似查找，搜索出的相似照片可以选择删除/不删除
   
* **人物分类：** 对相册中的图片，按照主体人物不同进行分类，获得以同一人物为主体的多个相册    

* **动物分类：** 对相册中的图片，按照物品不同进行分类，获得以同一物体为主体的多个相册
<div align=center><img width="400" height="280" src="https://github.com/You-zai/-/blob/main/%E5%9B%BE%E7%89%877.png"/></div>

#### 其他功能  
*  **自定义相册：** 新建、重命名、删除相册，在相册中添加图片；退出app后图片依然保留  

*  **回收站：** 删除相册中的照片，并在回收站中恢复删除的照片

*  **记忆存储：** 对于相册、分类结果、回收站等内容，具有记忆功能
    

操作指南
--------
### 小白式app   
* 支持Windows系统，使用时不依赖python/torch/tensorflow等环境，正常下载安装即可使用 

### 下载安装步骤

* 下载封装后的文件
    
* 下载完成后，点击“BlackPearl”图标，选择安装路径（推荐D盘、E盘、F盘，不推荐C盘），**并用智慧的大脑记住**（下一步用到），进行安装。

* 安装完成后，找到上一步的安装路径，下拉寻找到文件名为“BlackPearl”的文件，双击即可运行。

### 使用手册

* 详见功能介绍


原理详解
--------
### 一、界面设计
* 受Eagle的灵感启发，BlackPearl采用Dracula（中文译为吸血鬼）配色方案    
<div align=center><img width="400" height="300" src="https://github.com/You-zai/-/blob/main/%E5%9B%BE%E7%89%871.png"/></div>
 
* 界面布局采用PS进行设计


### 二、后端
#### （一）人脸验证
#### Face Recognition简介：
* 目前世界上最简洁的人脸识别库
  
* 可使用Python和命令行操作
  
* 基于C++开源库dlib中的深度学习模型
  
* LFW测试准确率达99.38% 
<div align=center><img width="400" height="280" src="https://github.com/You-zai/-/blob/main/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20211230145402.png  "/></div>

#### 算法流程：
* 加载图片，转化为RGB三通道格式
  
* 定位照片中人脸，包括[top, right, bottom, left]，分别代表框住人脸的矩形中左上角和右下角的坐标（x1,y1,x2,y2）。
   
* 提取人脸中特征，包括nose_bridge、right_eyebrow、right_eye、chine、left_eyebrow、bottom_lip、nose_tip、top_lip、left_eye九部分。每个部分包含若干个特征点(x,y)，总共有68个特征点
   
* 对68个特征点进行编码，每张人脸获得一个128维向量
 
* 可匹配两个面部特征编码，利用两个向量的内积（余弦距离）来衡量相似度，大于阈值确认是同一人脸，反之亦然。其中阈值默认值为0.6，可调节。

#### （二）相似查找

* 采用pHash增强版的低频感知哈希算法，避免伽马校正或颜色直方图被调整带来的影响。获得图片指纹后利用Hamming Distance计算两张图片的相似度。
<div align=center><img width="400" height="280" src="https://github.com/You-zai/-/blob/main/%E5%9B%BE%E7%89%876.png"/></div>

#### 详细原理如下：
* 将图片缩小为32×32  
  
* 将32×32的RGB彩图转换为灰度图   
   
* 计算图像的DCT变换，获得32×32矩阵  
  
* 缩小DCT矩阵，取左上角8×8矩阵（包含了最多的信息）  
 
 * 计算8×8 DCT矩阵的均值  
 
* 将矩阵进行二值处理：如果大于均值，则记为1；反之则记为0   
   
* 二值图按序组合成64位整型哈希值（指纹） 
 
* 得到指纹以后，对比不同的图片中64位有多少位不同 
  
* 如果不相同的数据位不超过5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片

#### （三）物品分类
* BlackPearl的物品分类功能 以ResNet34残差神经网络为基础，并在网络顶端添加softmax层，获得11维向量，对应图片为11个动物的可能性。

### 三、前端
<div align=center><img width="80" height="60" src="https://github.com/You-zai/-/blob/main/%E5%9B%BE%E7%89%872.png"/></div>

* BlackPearl的前端采用Qt框架
  
* Qt是一款跨平台C++图形用户界面应用程序开发框架，可用于GUI程序的开发，也可用于非GUI程序的开发，如控制台、操作系统等。

* 此外，Qt下含有大型集成开发环境Qt Creator，为GUI设计提供了便利；Qt Designer中可以拖动组件，进行空间布局，具有良好的可视化，并且能够利用UI文件和Python文件的相互转换，协助前端开发。
<div align=center><img width="400" height="270" src="https://github.com/You-zai/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202021-12-30%20144434.png"/></div>

致谢
------
我们将产品命名为**BlackPearl，黑珍珠**，寓意“最艰辛岁月的结晶，母贝伤痛的泪水，历经磨难所以稀有、高贵”。   
    
在此，感谢现实生活中所有人的帮助，感谢网络中创作者们的知识分享。




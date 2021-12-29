# 多功能相册app——BlackPearl
起源
------
应计算机软件基础课程要求，以及自身对于人工智能前沿知识探索的欲望，故诞生了本产品：**面向设计师的相册整理app——BlackPearl**。   
    
**BlackPearl**，黑珍珠，象征着最艰辛的岁月，历经磨难，所以稀有、高贵。
  
    
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
**·** 支持Windows系统，用户下载安装包并解压，选择安装路径进行安装。 
   
**·** 安装完成后在上一步的地址中找到“BlackPearl”，点击打开，即可运行。    
    
**·** 用户使用时不依赖python、torch、tensorflow等环境。

原理详解
--------
### 一、界面设计
受Eagle的灵感启发，BlackPearl采用Dracula（中文译为吸血鬼）配色方案    
    
界面布局采用PS进行设计


### 二、后端
#### （一）人脸识别
##### Face Recognition简介：
**·** 目前世界上最简洁的人脸识别库
  
**·** 可使用Python和命令行操作
  
**·** 基于C++开源库dlib中的深度学习模型
  
**·** LFW测试准确率达99.38% 
  
##### 算法流程：
1.加载图片，转化为RGB三通道格式
2.定位照片中人脸
3.提取人脸中特征
4.
#### （二）相似查找

采用pHash增强版的低频感知哈希算法，避免伽马校正或颜色直方图被调整带来的影响。
  
获得图片指纹后利用Hamming Distance计算两张图片的相似度。

算法步骤如下：
缩小图片尺寸  
将其化为灰度图   
计算图像的DCT变换  
缩小DCT  
计算DCT的均值  
对比判断得到二值图  
二值图按序组合成哈希值（指纹）  
计算汉明距离：得到指纹以后，就可以对比不同的图片，看看64位中有多少位是不一样的
如果不相同的数据位不超过5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片

#### （三）物品分类

### 三、前端


致谢
------
产品名为**BlackPearl，黑珍珠**，寓意“最艰辛岁月的结晶，母贝伤痛的泪水，历经磨难所以稀有、高贵”。   
    
在此感谢所有人的帮助。




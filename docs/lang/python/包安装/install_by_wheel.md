# linux安装包失败

## 业务背景

打包系统需要在容器中基于python2.7 安装 fasttext==0.9.2,报安装错误

## 技术设计

采用wheel二进制包的方式进行安装

## 示例

下载.tar.gz 文件

pip download fasttext==0.9.2
tar zxf xxx.tar.gz
cd fasttext.xxx
python setup.py bdist_wheel

然后把生成的wheel文件，上传到打包系统，即可。

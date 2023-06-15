# SimpleHTTPSServer
基于先知文章 https://xz.aliyun.com/t/12605 做的修改。


支持选择是否开启HTTPS、自定义端口、指定Web路径。

## Usage
SimpleHTTPSServer.py -s -p \<port\> -d \<webrootdir\>  
  -s, --useHTTPS         use HTTPS  
  -p, --port     set listening port  
  -d, --dir      set web directory  


开启HTTPS会在当前目录下创建证书文件，使用浏览器访问会提示证书不可信，测试使用时可选择忽略证书错误后使用。  

curl忽略证书错误： curl -k http://yourdomain.com/  
wget忽略证书错误： wget --no-check-certificate http://yourdomain.com/  


**请勿用于生产环境！**

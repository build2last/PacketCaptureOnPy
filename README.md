# PacketCaptureOnPy
packet capture with Python on Windows, then you can use the django show the packet distribution.
---
### 用到的工具
* [wireshark](https://www.wireshark.org/download.html): get pcap file
* [winpcap](https://github.com/build2last/PacketCaptureOnPy/blob/master/%E9%A1%B9%E7%9B%AE%E5%AE%89%E8%A3%85%E5%8C%85/WinPcap_4_1_2.exe): low level interface to elternet module
* [dpkt](https://github.com/build2last/PacketCaptureOnPy/blob/master/%E9%A1%B9%E7%9B%AE%E5%AE%89%E8%A3%85%E5%8C%85/pcap-1.1.win32-py2.7.msi): A python library to decode pcap file
  * Pip install dpkt
* django: here to help create tables in database and make some analyse upon the database with a demo to display the packet distribution among urls, 24-hours and types.
 * pip install django
  
#### Create database in mysql
> CREATE DATABASE pcap DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


ProjectJournal
---
#### [Data structure](https://github.com/build2last/PacketCaptureOnPy/blob/master/web/pcapdisplay/models.py) of the decoded pcap info
1. time	datetime
2. ip	string
3. srcip string
4. dstip string
5. trans_layer_type string
6. ttl int 			;表明数据包在因特网中至多可经过的路由器                
7. len int
8. src_mac string
9. dst_mac string
10. pcap_id
...

****
2016-10-06

#### 内容分析维度
1. 时间：流量（包的个数）在一天二十四小时上的分布，在一周时间上的分布
2. 空间：ip 地址流向
3. 内容：文本和图片，网站域名划分

"东西放到数据库里面，作者要喝奶去了。"
****
2016-10-07

#### 前端：数据展示
* [JavaScript]Tool: https://d3js.org/
* http://bl.ocks.org/dwtkns/4973620
* 【两个小时扔进去了】那个，js不允许跨域访问数据，所以json数据跟网页要放在同一个域名下。
* 正在试图读懂地点json格式
* 理性一点，这种高级需求放到还是要放到最后......

#### 后台需要提供一个提供数据的API
* 读取数据库后加工返回json格式的数据方便前端处理。

****
2016-10-07
#### 在学习前端画表
* 时间分布直方图 OK

* 需求是无限的，人的精力有限的，拿有限换无限，不值得。今日到此为止。

****
2016-10-12
* 大饼图OK，http内容类型统计

****
2016-10-13
* 访问域名分析OK
再做其他的意义不大，不过前端展示还是有很多可以提升的。
比如基于地图模型的流量展示。

协议栈每层包的格式好像忘记了，抽时间总结下。

暂告一段落。
还有更重要的事情等着我呢。

### 项目总结
* 复习做网站
* 复习计网协议栈报文格式
* 抓了包，解析了pcap，其他的收获不多。

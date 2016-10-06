# PacketCaptureOnPy
packet capture with Python on Windows, analyse

ProjectJournal
---
#### data struct of the decoded pcap info
1. time	datetime
2. ip	string
3. srcip string
4. dstip string
5. trans_layer_type string
6. ttl int 			;表明数据包在因特网中至多可经过的路由器                
7. len int
8. src_mac string
9. dst_mac string
10.pcap_id

****
2016-10-06

#### 内容分析维度
1. 时间：流量（包的个数）在一天二十四小时上的分布，在一周时间上的分布
2. 空间：ip 地址流向
3. 内容：文本和图片，网站域名划分


#### database in mysql
> CREATE DATABASE pcap DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

"东西放到数据库里面了，再见！喝奶去了。"
****
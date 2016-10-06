# -*- coding:utf-8 -*-
"""
SQL TO CREATE TABLE

CREATE TABLE `pcapdisplay_package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `host_ip` varchar(50) NOT NULL,
  `src_ip` varchar(50) DEFAULT NULL,
  `dstip` varchar(50) DEFAULT NULL,
  `trans_layer_type` varchar(10) NOT NULL,
  `ttl` int(11) DEFAULT NULL,
  `len` int(11) DEFAULT NULL,
  `src_mac` varchar(50) DEFAULT NULL,
  `dst_mac` varchar(50) DEFAULT NULL,
  `pcap_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
import DecodePackageTools as dpt
import MySQLdb

pwords = "liukun"
dbname = "pcap"

def pcapToMySQL(pcap_list):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd=pwords,db=dbname,port=3306)
        for ipcap in pcap_list:
            cur=conn.cursor()
            cur.execute("""insert into {table} 
                                (time,host_ip,src_ip ,dst_ip,trans_layer_type,ttl, 
                                len,src_mac,dst_mac,pcap_id,data_type,url) values 
                                ( 
                                    '{time}', '{host_ip}', '{src_ip}', '{dst_ip}', '{trans_layer_type}',\
                                    {ttl},{len}, '{src_mac}', '{dst_mac}', {pcap_id}, '{data_type}','{url}'\
                                )  
                                """.format(table="pcapdisplay_package",time=ipcap["time"],host_ip=ipcap["host_ip"],
                                src_ip=ipcap["host_ip"],dst_ip=ipcap["dst_ip"],
                                trans_layer_type=ipcap.get("trans_layer_type",""),ttl=ipcap["ttl"],
                                src_mac=ipcap["src_mac"],len=ipcap["len"],
                                dst_mac=ipcap["dst_mac"],pcap_id=ipcap.get("pcap_id",0),
                                data_type=ipcap.get("data_type","unknown"),url=ipcap.get("url",""))
                                )
            cur.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def exe():
    pcap_list = dpt.get_packets_list("D:\pcap.pcap")
    pcapToMySQL(pcap_list)
if __name__ == "__main__":
    exe()
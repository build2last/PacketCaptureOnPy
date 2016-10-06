# -*- coding:utf-8 -*-
"""
    输入：pcap 包的 path，或提供本地底层 pcap 接口
    输出：包含网络报信息的元组
    将网络包解码，提取出信息。
    date:2016-10-06
"""
import dpkt
import pcap
import datetime
import socket
import logging
import os

# global settings>>>>>>>>
logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=os.path.join(os.path.dirname(__file__) , 'pcap.log'),
            filemode='w')
localhost = socket.gethostbyname(socket.gethostname())
# global end<<<<<<<

def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntoa(inet) # change here socket.AF_INET, 
    except ValueError:
        return socket.inet_ntoa(inet) # socket.AF_INET6,
    
    
def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in address)
    

def get_packets_list(pcap_path, pcap_id=0):
    """Print out information about each packet in a pcap

       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    if not pcap_path:
        pc = pcap.pcap()
    else:
        try:
            pc = pcap.pcap(pcap_path)
        except Exception as e:
            print("Fail to open pcap file for:\n" + str(e))
            return []
    pcap_list = []
    try:
        # For each packet in the pcap process the contents
        for timestamp, buf in pc:
            dic_pcap = {}
            # Print out the timestamp in UTC
            dic_pcap["time"] = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            # print 'Timestamp: ', dic_pcap["time"]

            # Unpack the Ethernet frame (mac src/dst, ethertype --以太网类型码(Ethernet type codes)
            eth = dpkt.ethernet.Ethernet(buf)
            dic_pcap["src_mac"], dic_pcap["dst_mac"] =  mac_addr(eth.src), mac_addr(eth.dst)
            # print 'Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type
            if eth.type == 2048:
                dic_pcap["Ethernet_type"] = "ipv4"
                # http data type
                try:
                    if  eth.data.data.__class__.__name__=='TCP' and eth.data.data.dport == 80:
                        tcp_data = eth.data.data
                        if tcp_data.data:
                            h = dpkt.http.Request(tcp_data.data)
                            accept_text = h.headers["accept"]
                            dic_pcap["url"] = (h.headers.get("host",''))
                            if "text" in accept_text:
                                dic_pcap["data_type"] = "text"
                            elif "image" in accept_text:
                                dic_pcap["data_type"] = "image"
                        else:
                            dic_pcap["data_type"] = "unknown"
                except Exception as e:
                    dic_pcap["data_type"] = "unknown"
                    print(str(e))
                    # logging.error(str(e))

            # Make sure the Ethernet data contains an IP packet
            if not isinstance(eth.data, dpkt.ip.IP):
                print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
                continue

            # Now unpack the data within the Ethernet frame (the IP packet)
            # Pulling out src, dst, length, fragment info, TTL, and Protocol
            ip = eth.data
            if ip.p == 6:
                dic_pcap["trans_layer_type"] = "tcp"
                # print "tcp"
            elif ip.p == 17:
                dic_pcap["trans_layer_type"] = "udp"
            else:
                dic_pcap["trans_layer_type"] = str(ip.p)
                # print "udp"
            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
            # Print out the info
            # print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
            #      (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset)
            dic_pcap["sr_cip"] = inet_to_str(ip.src)
            dic_pcap["dst_ip"] = inet_to_str(ip.dst)
            dic_pcap["len"] = ip.len
            dic_pcap["ttl"] = ip.ttl
            dic_pcap["host_ip"] = localhost
            dic_pcap["pcap_id"] = pcap_id
            pcap_list.append(dic_pcap)
    except Exception as E:
        logging.error(str(E))
        return pcap_list           
   
if __name__ == "__main__":
    pa_list = get_packets_list("D:\pcap.pcap")
    for dic_pcap in pa_list:
        for i in dic_pcap:
            # print i,':',dic_pcap[i]
            if dic_pcap.get("url","")!="":
                print dic_pcap["url"]
    print(len(pa_list))

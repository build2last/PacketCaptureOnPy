# coding:utf-8
import dpkt
import re

def match(pre, line):
        p = re.compile(pre)
        m = p.match(line)
        return m


def main_pcap(p_time, p_data): 
        p = dpkt.ethernet.Ethernet(p_data)
        ret = None
        if p.data.__class__.__name__ == "IP":
            ip_data = p.data
            src_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.src)))
            dst_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_data.dst)))
            if p.data.data.__class__.__name__=='TCP':
                    tcp_data = p.data.data
                    if tcp_data.dport==80:
                            if tcp_data.data:
                                h = dpkt.http.Request(tcp_data.data)
                                host = h.headers.get('host', 'unKnown')
                                accept = h.headers.get('accept', 'unKnown')
                                if "text" in accept:
                                    return u"文本"
                                elif "image" in accept:
                                    return u"图片"
                                pre = "^/.*$"
                                """
                                # url filter?
                                if match(pre, h.uri):                                                                           # url 重写
                                        http_headers = h.headers
                                        host = h.headers['host']                    
                                        url = "http://" + host + h.uri
                                else:
                                        url = h.uri
                                """
                                ret = host
                                return  accept#h.headers.get('accept', 'unKnown')#tcp_data.data.split(" ",1)[0]
                    else:
                        return ''
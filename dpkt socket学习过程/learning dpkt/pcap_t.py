import pcap
import dpkt

			
if __name__ == "__maint__":
	pc=pcap.pcap()
	pc.setfilter("tcp port 8002")
	for ptime,pdata in pc:
		print ptime,pdata

	p=dpkt.ethernet.Ethernet(pdata)
	if p.data.__class__.__name__=='IP':
		ip='%d.%d.%d.%d'%tuple(map(ord,list(p.data.dst)))
		if p.data.data.__class__.__name__=='TCP':
			if data.dport==8002:
				print p.data.data.data # by gashero
	nrecv,ndrop,nifdrop=pc.stats()
# coding:utf-8
import json
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import package

# Create your views here.

# display the analyse content


def display(request):
    return render(request, 'pcapdisplay/host_rank.html')

delta = datetime.timedelta(days=101)    # 展示日期区间
# 流量在时间的分布 API
def time_distribution_json(request):
    re_type = request.GET.get('type')
    if re_type == "all":
        packs = package.objects.exclude(dst_ip__exact='192.168.1.105')
    elif re_type == "http":
        packs = package.objects.filter(time__gte=datetime.date.today()-delta).exclude(url__exact='')
    else:
        packs = package.objects.filter(time__gte=datetime.date.today()-delta)
        # packs = package.objects.order_by("-time")[:50]
    hour_dis_dict = {}
    for i in range(1,25):
        hour_dis_dict[str(i)] = 0;
    time_list = []
    time_list.append(len(packs))
    for ipa in packs:
        hour_dis_dict[str(ipa.time.hour)] += 1
        # time_list.append(ipa.time.strftime("%Y-%m-%d %H:%M:%S"))
    time_by_hour = [hour_dis_dict[str(x)] for x in range(1,25)]
    # 0h 1h 2h ~ 23h
    time_by_hour = [time_by_hour[23] ] + time_by_hour[:23]
    return HttpResponse(str(time_by_hour))

    
# 流量在空间上的分布 API
def geography_distribution_json(request):
    pass

   
# HTTP流量在内容上的分布
def content_distribution_json(request):
    packs = package.objects.filter(time__gte=datetime.date.today()-delta).exclude(url__exact='')
    data_type_dic = {}
    for ipa in packs:
        type = ipa.data_type
        if type == "unknown":
            continue
        elif type in data_type_dic:
            data_type_dic[type] += 1
        else:
            data_type_dic[type] = 1
    ret_str = []
    api_data = {}
    for it in data_type_dic:
        ret_str.append(dict(type=it,count=data_type_dic[it]))
    api_data["data"] =ret_str
    return HttpResponse(json.dumps(api_data))
 
# distrbution by host name ,域名流量排序
def host_distribution_page(request):
     packs = package.objects.filter(time__gte=datetime.date.today()-delta).exclude(url__exact='')
     host_name_dic = {}
     for ipa in packs:
        host_name = ipa.url
        ip_time = ipa.time.strftime("%Y-%m-%d %H:%M:%S")
        #if host_name.count('.')>=2:
        #    host_name = '.'.join(ipa.url.split('.')[1:])
        if host_name in host_name_dic:
            host_name_dic[host_name]["count"] += 1
            if  ip_time > host_name_dic[host_name]["lastvisit"]:
                host_name_dic[host_name]["lastvisit"] =  ip_time
        else: host_name_dic[host_name] = (dict(count=1,lastvisit=ip_time, host_url=host_name))
     re_list = []
     for i in host_name_dic:
        re_list.append(host_name_dic[i])
     # bubble sort by visit times
     i = len(re_list) - 1
     while(i>=0):
        j = 0
        changed = False
        while(j<i):
            if re_list[j]["count"] < re_list[j+1]["count"]: 
                temp = dict(re_list[j])
                re_list[j] = re_list[j+1]
                re_list[j+1] = temp
                changed = True
            j+=1
        if not changed:
             break
        else:
            i-=1
     return render(request, 'pcapdisplay/host_rank.html',
          {
             "re_list": re_list,
          }
      )
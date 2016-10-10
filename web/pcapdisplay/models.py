# coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class package(models.Model):
    """
    data models for ipv4 package
    10 + 1(autoType as primary key) fields
    """
    time = models.DateTimeField(null=False)
    host_ip = models.CharField(max_length=50, null=False)
    src_ip = models.CharField(max_length=50, null=True)
    dst_ip = models.CharField(max_length=50, null=True)
    trans_layer_type = models.CharField(max_length=10, null=False)
    ttl = models.IntegerField(null=True)            
    len = models.IntegerField(null=True)
    src_mac = models.CharField(max_length=50, null=True)
    dst_mac = models.CharField(max_length=50, null=True)
    pcap_id = models.IntegerField(null=False, default=0)
    data_type = models.CharField(max_length=20, null=True)
    url = models.CharField(max_length=200, null=True)
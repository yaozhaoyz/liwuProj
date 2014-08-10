## coding=utf8
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from liwu.settings import URL_PREFIX 
from models import *
import urllib2
import datetime
import os
import json
import re
import heapq
import random

def importData2ItemDB(request):
    responseAll = {};
    for line in open("/disk1/liwuDjango/data/testTaobao.dat"): 
        line = line.split("\t");
        itemUrl = line[1] 
        found = LiwuItem.objects.filter(itemURL=itemUrl)
        if(found == None or len(found)==0):
            pid = Pid(pid=0)
            pid.save()
            pId = len(Pid.objects) 
            aliwu= LiwuItem(pId = pId)
            aliwu.pId = pId;
            aliwu.title = line[0] 
            aliwu.itemURL = line[1] 
            aliwu.price = line[2] 
            aliwu.priceRank = float(line[3]) 
            aliwu.taobaoCommentText = line[4] 
            aliwu.soldAmout = int(line[5])
            aliwu.imageUrl = line[6] 
            aliwu.itemDesc = line[7] 
            aliwu.liwuReason = line[8] 
            aliwu.liwuPersonTag = line[9] 
            aliwu.liwuSeasonTag = line[10] 
            aliwu.liwuTags = line[11] 
            aliwu.liwuGender = line[12] 
            if(line[13] != ""):
                aliwu.updatetime = line[13].strftime('%Y-%m-%d') 
            if(line[14] != ""):
                aliwu.firstShownTime = line[14].strftime('%Y-%m-%d') 
            aliwu.scoreAsLiwu = float(line[15]) 
            aliwu.commentList = line[16].split("`") 
            aliwu.save()
        else:
            continue;
    responseAll["RetCode"] = "RetOK "+str(len(LiwuItem.objects))
    return HttpResponse(json.dumps(responseAll), content_type="application/json")

def showCandidate(request):
    responseAll = {}
    pId = request.GET.get('pId',"");
    res = []
    if(pId == ""):
        pIds = LiwuItem.objects.order_by('pId')
        for i in pIds:
            r = {}
            r["title"] = i.title;
            r["imageUrl"] = i.imageUrl;
            r["click"] = "?pId="; # + str(i.pId);
            res.append(r);
        return render_to_response('showLiwuCandidate.html', {'post': res},context_instance=RequestContext(request))
    else:
        item = LiwuItem.objects.filter(pId=pId)
        res = []
        if(len(item)==0):
            responseAll["RetCode"] = "No such Pid" 
            return HttpResponse(json.dumps(responseAll), content_type="application/json")
        for i in item:
            r = {}
            r["title1"] = i.title;
            r["imageUrl"] = i.imageUrl;
            r["click"] = "?pId="; # + str(i.pId);
            res.appand(r);
        return render_to_response('showACandidateDetail.html', {'post': res},context_instance=RequestContext(request))
        
def processLiwuItem(request):
    responseAll = {}
    if(request.method=="GET"):
        api = request.GET.get('api',""); 
        pId = request.GET.get('pId',""); 
        if(api=="GetItemInfoById"):
            try:
                pId = int(pId)
            except:
                responseAll["RetCode"] = "no paramete pId"
                return HttpResponse(json.dumps(responseAll), content_type="application/json")
            found = LiwuItem.objects.filter(pId=pId)
            if(found == None or len(found)==0):
                responseAll["RetCode"] = "NoSuch Pid"
            else:
                aliwu = found[0]
                responseAll["pId"]= aliwu.pId
                responseAll["title"]= aliwu.title
                responseAll["itemURL"]= aliwu.itemURL
                responseAll["price"]= aliwu.price
                responseAll["priceRank"]= aliwu.priceRank
                responseAll["taobaoCommentText"]= aliwu.taobaoCommentText
                responseAll["soldAmout"]= aliwu.soldAmout
                responseAll["imageUrl"]= aliwu.imageUrl
                responseAll["itemDesc"]= aliwu.itemDesc
                responseAll["liwuReason"]= aliwu.liwuReason
                responseAll["liwuPersonTag"]= aliwu.liwuPersonTag
                responseAll["liwuSeasonTag"]= aliwu.liwuSeasonTag
                responseAll["liwuTags"]= aliwu.liwuTags
                responseAll["liwuTags"]= aliwu.liwuTags
                responseAll["liwuGender"]= aliwu.liwuGender
                responseAll["updatetime"]= aliwu.updatetime
                responseAll["firstShownTime"]= aliwu.firstShownTime
                responseAll["scoreAsLiwu"]= aliwu.scoreAsLiwu
                responseAll["commentList"]= aliwu.commentList
            return HttpResponse(json.dumps(responseAll), content_type="application/json")
        elif(api=="GetMainCardpIds"):
            pIds = LiwuItem.objects.order_by('pId')
            responseAll["pIds"]= []
            for i in pIds:
                responseAll["pIds"].append(i.pId);
            return HttpResponse(json.dumps(responseAll), content_type="application/json")
    responseAll["RetOK"]="No API"
    return HttpResponse(json.dumps(responseAll), content_type="application/json")

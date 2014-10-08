# coding=utf8
from django.template import RequestContext
from django.http import HttpResponse
from qiniu import conf,rs,io
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from liwu.settings import URL_PREFIX 
from models import *
import urllib2
import datetime,time
import os
import json
import re
import heapq
import random
from liwu.settings import BASE_DIR,MEDIA_ROOT,MEDIA_URL,ACCESS_KEY,SECRET_KEY,BUCKET_NAME,QINIU_URL,QINIU_XHURL

conf.ACCESS_KEY = ACCESS_KEY
conf.SECRET_KEY = SECRET_KEY
policy = rs.PutPolicy(BUCKET_NAME)

def save2hasEditedDB(request):
    if request.method == 'POST':
        responseAll = []
        pid = Pid(pid=0)
        pid.save()
        _id = len(Pid.objects) 
        thisTime = str(int(time.time())) + ""
        fReadTxt = request.POST.get("elm1","");
        fReadTxtAll = ""; 
        if(fReadTxt!=""):
            contentHtmlOut = ""
            contentHtmlStore= ""
            contentHtmlDir =  str(MEDIA_ROOT)+"content/"+str(_id)
            os.makedirs(contentHtmlDir);
            contentHtmlOut =  str(MEDIA_ROOT)+"content/"+str(_id)+"/"+thisTime+".html";
            contentHtmlStore=  str(QINIU_URL)+str(_id)+"/contentHtml/"+thisTime+".html";
            fWriteTxt = open(contentHtmlOut,"wb+");
            fCode = "<style>@media only screen and (min-device-width : 320px) and (max-device-width : 568px) and (orientation : portrait) { img { width: 300px; } p {  font-size: 1.5em; text-align: justify; padding: 4px;}} </style>" # for auto adjust format by liaojundong
            fReadTxtAll = "<html xmlns=\"http://www.w3.org/1999/xhtml\"> <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf8\"><body> \n" + fCode + "\n" + fReadTxt + "</body></html>"
            fWriteTxt.write(fReadTxtAll.encode("utf8") )
            fWriteTxt.close();
            filename = contentHtmlOut
            key = filename.replace(BASE_DIR+"/","");
            ret, err = io.put_file(policy.token(), key, filename)
        responseData = {}
        responseData["fReadTxt"] = fReadTxt
        responseData["fCodeHtml"] = fReadTxtAll.encode("utf8"); 
        responseData["post_info"] =  request.POST
        responseData["pId"] =  _id; 
        title = request.POST['title']
        aItem = LiwuItem_hasEditedDB(title=title)
        aItem.pId = _id;
        aItem.itemURL =  request.POST.get('itemURL',"")
        aItem.liwuReason = fReadTxtAll; 
        aItem.price =  request.POST.get('price',"");
        aItem.priceRank = request.POST.get('priceRank',"") 
        rateStr = request.POST.get('rate',"")
        try:
            aItem.rate = float(rateStr)
        except:
            aItem.rate = 4; #default, 0, 4  7 
        aItem.soldAmout = request.POST.get('soldAmout',"")
        aItem.imageUrl = request.POST.get('imageUrl',"")
        aItem.liwuPersonTag = request.POST.get('liwuPersonTag',"") 
        aItem.liwuSeasonTag = request.POST.get('liwuSeasonTag',"") 
        aItem.liwuTags = request.POST.get('liwuTags',"") 
        aItem.liwuGender= request.POST.get('liwuGender',"") 
        scoreAsLiwu = request.POST.get('scoreAsLiwu',"")
        try:
            aItem.scoreAsLiwu = float(scoreAsLiwu);
        except:
            aItem.scoreAsLiwu = 0.5;
        aItem.save()
        old_pId = request.POST.get('pId',"");
        try:
            old_pId = int(old_pId);
        except:
            old_pId = -1;
        found = LiwuItem_toBeEdited.objects.filter(pId = old_pId);
        if(len(found)>0):
            bItem = found[0];
            bItem.editOrNot = 1;
            bItem.save();
        return HttpResponse(json.dumps(responseData), content_type="application/json")

def uploadImgXheditor(request):
    responseData = {}
    if( not os.path.isdir(str(MEDIA_ROOT))):
        os.mkdir(str(MEDIA_ROOT));
    if( not os.path.isdir(str(MEDIA_ROOT)+"XheditorImg/")):
        os.mkdir(str(MEDIA_ROOT)+"XheditorImg/");
    if 'HTTP_CONTENT_DISPOSITION' in request.META:
        disposition = request.META['HTTP_CONTENT_DISPOSITION']
        image_name_suffix = disposition[ disposition.rindex('.') : disposition.rindex('"') ]
        image_name = str(int(time.time())) + image_name_suffix
        filename = str(MEDIA_ROOT)+"XheditorImg/"+image_name
        data = request.body
        Ret = Xh_writeData(data,image_name_suffix,filename,True)
    else:
        if 'filedata' in request.FILES:
            image_name = request.FILES["filedata"].name
            image_name_suffix = image_name[image_name.rindex('.') : ]
            filename = str(MEDIA_ROOT)+"XheditorImg/"+image_name
            Ret = Xh_writeData(request.FILES["filedata"],image_name_suffix,filename,False)
        else:
            Ret = ""
    return HttpResponse(json.dumps({"err":"","msg":Ret},ensure_ascii = False))

def Xh_writeData(data,image_name_suffix,filename, html5):
    ALLOW_SUFFIX =['.jpg','.png','.jpeg','.gif']
    if image_name_suffix in ALLOW_SUFFIX:
        image_name = str(int(time.time())) + image_name_suffix
        try:
            with open(filename,'wb') as destination:
                if html5:
                    destination.write(data)#写文件流
                else:
                    for c in data.chunks():
                        destination.write(c)
            key = filename.replace(BASE_DIR+"/","");
            ret, err = io.put_file(policy.token(), key, filename)
            if(err == None):
                return str(QINIU_XHURL)+key;
            else:
                return ""
        except:
            return "";
    else:
        return "";

def import2beEdit(request):
    responseAll = {};
    for line in open("/disk1/liwuDjango/data/testTaobao.dat"): 
        line = line.split("\t");
        itemUrl = line[1] 
        found = LiwuItem_toBeEdited.objects.filter(itemURL=itemUrl)
        if(found == None or len(found)==0):
            pid = Pid(pid=0)
            pid.save()
            pId = len(Pid.objects) 
            aliwu= LiwuItem_toBeEdited(pId = pId)
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

def showToBeEdited(request):
    responseAll = {}
    pId = request.GET.get('pId',"");
    res = []
    if(pId == ""):
        pIds = LiwuItem_toBeEdited.objects.order_by('pId')
        for i in pIds:
            r = {}
            r["title"] = i.title;
            r["imageUrl"] = i.imageUrl;
            r["click"] = "?pId="+str(i.pId);
            res.append(r);
        return render_to_response('showLiwuCandidate.html', {'post': res},context_instance=RequestContext(request))
    else:
        item = LiwuItem_toBeEdited.objects.filter(pId=pId)
        if(len(item)==0):
            responseAll["RetCode"] = "No such Pid" 
            return HttpResponse(json.dumps(responseAll), content_type="application/json")
        return render_to_response('showACandidateDetail.html', {'post': item[0]},context_instance=RequestContext(request))
        
def uploadSelectedLiwu(request):
    if(request.method == "GET"):
        return render_to_response('uploadSelectedLiwu.html',context_instance=RequestContext(request))
    if(request.method == "POST"):
        responseAll["RetCode"] = "RetOK"
    return HttpResponse(json.dumps(responseAll), content_type="application/json")

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

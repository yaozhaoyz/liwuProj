#coding=utf8
from django.db import models
from mongoengine import *
from liwu.settings import DBNAME
from django import forms
from django.forms.widgets import *
from django.http import HttpResponse

connect(DBNAME)
class Pid(Document):
    pId = IntField()

# Create your models here.
class LiwuItem(Document):
    pId = IntField(required=True)
    title = StringField(required=True)
    itemURL = StringField() # taobao item url
    price = StringField()
    priceRank = IntField() # 7高 4中  1低
    rate = FloatField() # 评价分（描述分）
    taobaoCommentText = StringField() #淘宝用户的评论信息 用 "\1"分隔
    soldAmout = IntField() # 淘宝月销量
    imageUrl= StringField()
    itemDesc = StringField() # 商品介绍 
    liwuReason = StringField() #(为啥值得送):    编辑！
    liwuPersonTag = StringField() # (送给什么样的人)  --  List(weight)   小孩, 用`进行分隔符
    liwuSeasonTag = StringField() #（什么节日场景送） 父亲节、生日、乔迁、生孩子、感谢、道歉(weight)
    liwuTags = StringField()  # --> 商品本身的tag，比如：运动、音乐
    liwuGender = StringField() # -> 适合送给男/女
    updatetime = DateTimeField() # -> 更新时间  (爬取上线)
    firstShownTime = DateTimeField() # -> 被展示过多久了，防止审美疲劳
    scoreAsLiwu =FloatField(default=0.5) #--> 适合当做礼物的权重， 0-1
    commentList = ListField()     # liwuguanjia 用户的评论--->  comment.commentID

class LoginUser(Document):
    pId = IntField(required=True)
    userNick = StringField(max_length=120, required=True)
    headshotImage = StringField(max_length=1000, required=True)
    accountFrom = StringField(max_length=120, required=True) # weibo, qq, 手机号
    weiboId = StringField(max_length=120) # weibo
    qqId = StringField(max_length=120) # weibo
    phoneId= StringField(max_length=120) # weibo
    gouwucheLiwu =ListField()  #:  list of   liwuItem.liwuId
    likeLiwu = ListField() #:  喜欢的礼物  list of   liwuItem.liwuId
    shoucangLiwu = ListField() #:  收藏夹  list of   liwuItem.liwuId

class Comment(Document):
    pId = IntField(required=True)
    typeOf =  IntField(required=True) # 1. 对商品的评价；  2. 对专题的评价
    loginUserId = IntField(required=True)# 评论者的id;LoginUser.pId
    content = StringField(max_length=1000, required=True)#评论的内容
    howManyLikes = IntField(required=True, default=0) #评论被赞了多少次
    liwuReplyTo = IntField(required=True, default= -1) #liwu.pid, 没有，则为-1
    specialSubjectReplyTo = IntField(required=True, default= -1) #SpecialSubject.pid, 没有，则为-1
    commentReplyTo = IntField(required=True,default=-1) #commentId, 对哪个评论的评论如果是主评论，则值是-1
    LoginUserRelpyTo = IntField(required=True,default=-1) #LoginUser.pId, 如果没有，默认是-1
    time = DateTimeField(required=True)

class SpecialSubject(Document):  #专题
    pId = IntField(required=True)
    dateStart = DateTimeField(required=True) # 开始时间 
    dateEnd = DateTimeField(required=True) # 结束时间
    mainImageURL = StringField() # 主图片
    htmlContent = StringField() #： 文章内容
    relateLiwuIds = ListField()  # 相关礼物ids
    

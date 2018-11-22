# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
import json,time
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from main.getExcelData import getExcelData
from django.core import serializers
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from forms import UserForm
from main.utils.user_utils import my_login,accountCase
# Create your views here.
@my_login
def index(request):
    yyid = yyStock.objects.filter(product_name='broke').values("id")
    wmid = yyStock.objects.filter(product_name='wm').values("id")
    pcid = yyStock.objects.filter(product_name='pc').values("id")
    yunyingid = yyStock.objects.filter(product_name='yunying').values("id")
    all_yycase, all_yypassCase = accountCase(yyid)
    all_pccase, all_pcpassCase = accountCase(wmid)
    all_wmcase, all_wmpassCase = accountCase(pcid)
    all_yunyingcase,all_yunyingpassCase = accountCase(yunyingid)
    print all_yycase, all_yypassCase,all_wmcase,all_wmpassCase,all_pccase,all_pcpassCase,all_yunyingcase,all_yunyingpassCase
    return render(request,'index.html',{
        'all_yycase': all_yycase,
        'all_yypassCase': all_yypassCase,
        'all_wmcase': all_wmcase,
        'all_wmpassCase': all_wmpassCase,
        'all_pccase': all_pccase,
        'all_pcpassCase': all_pcpassCase,
        'all_yunyingcase': all_yunyingcase,
        'all_yunyingpassCase': all_yunyingpassCase,
    })
def login(request):
    username = request.COOKIES.get('username')
    print username
    if username is not None:
        return redirect('/',{'username':username})
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember = request.POST.get('remember')
            print remember
            re = auth.authenticate(username = username,password=password)
            print re
            if re is not None:
                auth.login(request,re)
                response = redirect('/',{'username':username })
                request.session['username'] = username
                request.session['password'] = password
                response.set_cookie('username',username,3600)
                response.set_cookie('password', password, 3600)
                return redirect('/',{'username':username })
            else:
                return render(request,'login.html',{'login_error':'用户名或者密码错误'})
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    response = HttpResponse('/login/')
    response.delete_cookie('username')
    return render(request,"login.html")
def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password2 = uf.cleaned_data['password2']
            print password,password2
            if password == password2:
                User.objects.create_user(username = username,password=password)
                re = auth.authenticate(username=username, password=password)
                auth.login(request, re)
                response = redirect('/', {'username': username})
                request.session['username'] = username
                response.set_cookie('username', username, 3600)
                return redirect('/', {'username': username})
                #return render(request,'index.html',{'username':username })
            else:
                return render(request, 'register.html', {'register_error': '两次输入密码不一致'})
    else:
        uf = UserForm()
    return render(request,'register.html',{'uf':uf })
@my_login
def yyBroke(request,product):
    print request.path,product
    if request.path == ('/yyBroke/'+product):
        print request.path,product
        if request.method == 'POST':
            data = json.loads(request.body)
            print data
            case_name = data["case_name"]
            case_version = data["case_version"]
            yyStock.objects.get_or_create(name=case_name,version=case_version,product_name = product )
            return render(request, 'youyuBroker.html', {'versions': case_version})
        else:
            versions = yyStock.objects.filter(product_name = product)
            print versions
            return render(request, 'youyuBroker.html',{'versions':versions,'product':product})
    elif request.path == ('/yyBroke_edit/'+product):
        print request.path
        if request.method == 'POST':
            data = json.loads(request.body)
            print data
            version = data["version"]
            name = data["name"]
            id = data["id"]
            case = yyStock.objects.get(id=int(id))
            case.name = name
            case.version = version
            case.save()
            print "success"
            # return HttpResponseRedirect('/yyBroke/')
            return render(request, 'youyuBroker.html')
@my_login
def yyCaseModel(request,product,version):
    version_id = yyStock.objects.filter(version=version,product_name = product).values("id")
    Version = version_id[0]
    print Version["id"]
    models = caseModel.objects.filter(case_version = int(Version["id"]))
    return render(request,'modelList.html',{'models':models,'case_version':version,'product':product})
@my_login
def caseModel_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print data
        case_version = data["version"]
        product = data["product"]
        model_id = data["id"]
        case_model = data["name"]
        version_id = yyStock.objects.filter(version=case_version, product_name=product).values("id")
        Version = version_id[0]
        print Version["id"]
        search_dict = dict()
        search_dict['case_version_id'] = int(Version["id"])
        search_dict['case_model'] = case_model
        model_cases = yyCasedetail.objects.filter(**search_dict).count()
        print model_cases
        if model_cases == 0:
            caseModel.objects.filter(id = model_id).delete()
            return render(request,'modelList.html')
        else:
            return HttpResponse("请先删除该模块下的子用例")
@my_login
def yyBroke_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print data
        version = data["version"]
        isModel = yyStock.objects.filter(version=version).values("id")
        isModel_id = isModel[0]["id"]
        print isModel_id
        isModel = caseModel.objects.filter(case_version = int(isModel_id))
        if isModel:
            return HttpResponse("请先删除该版本下的子用例")
        else:
            yyStock.objects.filter(version=version).delete()
            print "success"
            return render(request,'youyuBroker.html')
@my_login
def yyBroke_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print data
        filepath = data["filepath"]
        filename = data["filename"]
        case_version = data["version"]
        yyCasefile.objects.get_or_create(filename=filename, filepath=filepath,case_version=case_version)
        print "chenggong"
        path = "/"+case_version+'/caselist'
        print path
        return HttpResponseRedirect(path)

def saveCase(realpath,case_version,product_name):
    print realpath,case_version,product_name
    case_data = getExcelData()
    datas = case_data.mulData(realpath)
    #print datas
    case_version_id = yyStock.objects.filter(version=case_version,product_name=product_name).values("id")
    Version = case_version_id[0]
    print Version["id"]
    version_id = Version["id"]
    print version_id
    sheets = case_data.getallSheet(realpath)
    print sheets
    for sheet in sheets:
        caseModel.objects.get_or_create(case_versionName=case_version, case_modelName=sheet, case_version=int(version_id),product_name=product_name)
    for case in datas:
        yyCasedetail.objects.get_or_create(xuqiu=case["xuqiu"], case_router=case["case_router"],
                                           case_title=case["case_title"],
                                           case_pre=case["case_pre"], case_step=case["case_step"],
                                           case_action=case["case_action"], case_actionPre=case["case_actionPre"],
                                           case_prior=case["case_prior"],
                                           case_result=case["case_result"], case_insru=case["case_insru"],case_model=case["case_model"],
                                           case_version_id=int(version_id),case_id=int(case["case_id"]))

def uploadFiles(request):
    filename = request.POST.get("filename")
    case_version = request.POST.get("case_version")
    files = request.FILES.get("files")
    product_name = request.POST.get("product_name")
    fpath = r'main/caseFiles/%s'%(filename)+".xlsx"

    with open(fpath,'wb') as pic:
        for c in files.chunks():
            pic.write(c)
    #realpath = fpath.decode('utf-8')
    saveCase(fpath,case_version,product_name)
    return render(request,'modelList.html')
@my_login
def yyBroke_search(request,caseinfor):
    case_infro = caseinfor.split('&')
    product = case_infro[0]
    case_version = case_infro[1]
    case_model = case_infro[2]
    print product, case_version,case_model
    if request.method == 'POST':
            print request.POST['prior']
            print request.POST['caseResult']
            version_id = yyStock.objects.filter(version=case_version,product_name = product).values("id")
            Version = version_id[0]
            print Version["id"]
            search_dict = dict()
            if request.POST['prior'] !="" and request.POST['caseResult']!="" :
                casePrior = str(request.POST['prior'])
                search_dict['case_prior'] = casePrior
                search_dict['case_result'] = request.POST['caseResult']
                search_dict['case_version_id'] = int(Version["id"])
                search_dict['case_model'] = case_model
            elif request.POST['prior'] =="" and request.POST['caseResult']!="":
                search_dict['case_result'] = request.POST['caseResult']
                search_dict['case_version_id'] = int(Version["id"])
                search_dict['case_model'] = case_model
            elif request.POST['prior'] !="" and request.POST['caseResult']=="":
                casePrior = str(request.POST['prior'])
                search_dict['case_prior'] = casePrior
                search_dict['case_version_id'] = int(Version["id"])
                search_dict['case_model'] = case_model
            else:
                search_dict['case_version_id'] = int(Version["id"])
                search_dict['case_model'] = case_model
            print search_dict
            cases = yyCasedetail.objects.filter(**search_dict).order_by("case_id")
            print cases
            return render(request, 'youyuCaselist.html',
                          {'cases': cases, 'caseModel': case_model, 'version': case_version ,'prior':request.POST['prior'],
                           'caseResult': request.POST['caseResult'],'product':product})
    elif request.method == 'GET':
            version_id = yyStock.objects.filter(version=case_version,product_name = product).values("id")
            Version = version_id[0]
            print Version["id"]
            search_dict = dict()
            search_dict['case_version_id'] = int(Version["id"])
            search_dict['case_model'] = case_model
            model_cases = yyCasedetail.objects.filter(**search_dict).order_by("case_id")
            return render(request, 'youyuCaselist.html',
                          {'cases': model_cases, 'caseModel': case_model, 'version': case_version, 'prior': "",
                           'caseResult': "",'product':product})
@my_login
def yyBrokeCase_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print data
        caseId = data["caseId"]
        yyCasedetail.objects.filter(id=int(caseId)).delete()
        print "success"
        #return HttpResponseRedirect('/yyBroke/')
        return render(request, 'youyuCaselist.html')
@my_login
def yyBrokeCase_insert(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        caseId = data["caseId"]
        case_version = data["caseVersion"]
        case_model = data["caseModel"]
        case_id = int(caseId)
        yyCasedetail.objects.create(xuqiu="", case_router="",case_title="",
                                           case_pre="", case_step="",
                                           case_action="", case_actionPre="",
                                           case_prior="",
                                           case_result="", case_insru="",case_model=case_model,
                                           case_version_id=int(case_version),case_id=case_id)
        return render(request, 'youyuCaselist.html')
@my_login
def yyBrokeCase_save(request):
    if request.method == 'POST':
        local_username = request.user.username
        print local_username
        data = json.loads(request.body)
        localTime = time.localtime()
        case_excuteTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        print case_excuteTime
        allcase = data["all_case"]
        for case in allcase:
            id = case["caseid"]
            obj = yyCasedetail.objects.get(id = int(id))
            obj.xuqiu = case["xuqiu"]
            obj.case_router=case["case_router"]
            obj.case_title=case["case_title"]
            obj.case_pre=case["case_pre"]
            obj.case_step=case["case_step"]
            obj.case_action=case["case_action"]
            obj.case_actionPre=case["case_actionPre"]
            obj.case_prior=case["case_prior"]
            obj.case_result=case["case_result"]
            obj.case_insru=case["case_infor"]
            obj.save()
        for case in allcase:
            id = case["caseid"]
            case_result = case["case_result"]
            print case_result
            caseinfor = caseLog.objects.filter(case_id_id=int(id))
            print caseinfor
            if caseinfor:
                caseInfor = caseLog.objects.filter(case_id_id=int(id),case_execute=local_username)
                if caseInfor:
                    caseInfor2 = caseLog.objects.get(case_id_id=int(id), case_execute=local_username)
                    caseInfor2.case_executeResult = case_result
                    caseInfor2.case_executeTime = case_excuteTime
                    caseInfor2.save()
                else:
                    caseLog.objects.get_or_create(case_id_id=int(id),case_execute=local_username,
                                              case_executeResult = case_result, case_executeTime = case_excuteTime)
            else:
                caseLog.objects.get_or_create(case_id_id=int(id), case_execute=local_username,
                                              case_executeResult=case_result, case_executeTime=case_excuteTime)
        return render(request, 'youyuCaselist.html')
def execteLog(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        caseId = data["caseId"]
        allCaseLog = caseLog.objects.filter(case_id_id=int(caseId)).values()
        print len(allCaseLog)
        return JsonResponse(list(allCaseLog),safe=False)






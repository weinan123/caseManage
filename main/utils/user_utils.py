from django.shortcuts import redirect
from main.models import *
def my_login(func):
    def inner(*args,**kwargs):
        login_user_id = args[0].session.get('username')
        print login_user_id
        if login_user_id is not None:
            return func(*args,**kwargs)
        else:
            return redirect('/login')
    return inner
def accountCase(countid):
    accountCases = 0
    accountPassCases = 0
    for i in countid:
        oneaccCase = yyCasedetail.objects.filter(case_version_id= i["id"]).count()
        oneaccPassCase = yyCasedetail.objects.filter(case_result="pass",case_version_id= i["id"]).count()
        accountCases = accountCases + oneaccCase
        accountPassCases = accountPassCases + oneaccPassCase
    return accountCases,accountPassCases



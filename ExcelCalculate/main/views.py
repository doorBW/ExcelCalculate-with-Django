from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import *
import hashlib

# Create your views here.
def index(request):
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html')
    else:
        return redirect('main_signin')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print(request)
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    # pw encryption
    encoded_pw = pw.encode()
    encrypted_pw = hashlib.sha256(encoded_pw).hexdigest()
    user = User(user_name = name, user_email = email, user_password = encrypted_pw)
    user.save()
    code = randint(1000, 9999)
    response = redirect('main_verifyCode')
    response.set_cookie('code',code)
    response.set_cookie('user_id',user.id)
    # 이메일 발송 함수 호출
    send_result = send(email,code)
    if send_result:
        return response
    else:
        content = {'message':'이메일 발송에 실패하였습니다.'}
        return render('main/error.html',content)
        # return HttpResponse("이메일 발송에 실패하였습니다.")

def signin(request):
    return render(request, 'main/signin.html')

def login(request):
    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']
    try:
        user = User.objects.get(user_email = loginEmail)
    except:
        return redirect('main_loginFail')
    # 사용자가 입력한 PW 암호화
    encoded_loginPW = loginPW.encode()
    encrypted_loginPW = hashlib.sha256(encoded_loginPW).hexdigest()
    if user.user_password == encrypted_loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_index')
    else:
        return redirect('main_loginFail')

def loginFail(request):
    return render(request, 'main/loginFail.html')

def logout(request):
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_signin')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user',user)
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return response
    else:
        redirect('main_verifyCode')

def result(request):
    if 'user_name' in request.session.keys():
        content = {}
        content['grade_calculate_dic'] = request.session['grade_calculate_dic']
        content['email_domain_dic'] = request.session['email_domain_dic']
        del request.session['grade_calculate_dic']
        del request.session['email_domain_dic']
        return render(request, 'main/result.html',content)
    else:
        return redirect('main_signin')
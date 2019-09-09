from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def calculate(request):
    file = request.FILES['fileInput']
    # print("# 사용자가 등록한 파일의 이름: ",file)
    df = pd.read_excel(file,sheet_name='Sheet1',header=0)
    # print(df.head(5))
    # grade별 value리스트 만들기
    grade_dic = {}
    total_row_num = len(df.index)
    for i in range(total_row_num):
        data = df.loc[i]
        if not data['grade'] in grade_dic.keys():
            grade_dic[data['grade']] = [data['value']]
        else:
            grade_dic[data['grade']].append(data['value'])
    # grade별 최소값 최대값 평균값 구하기
    grade_calculate_dic = {}
    for key in grade_dic.keys():
        grade_calculate_dic[key] = {}
        grade_calculate_dic[key]['min'] = min(grade_dic[key])
        grade_calculate_dic[key]['max'] = max(grade_dic[key])
        grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key]))/len(grade_dic[key])
    # 결과 출력
    grade_list = list(grade_calculate_dic.keys())
    grade_list.sort()
    for key in grade_list:
        print("# grade:",key)
        print("min:",grade_calculate_dic[key]['min'],end='')
        print("/ max:",grade_calculate_dic[key]['max'],end='')
        print("/ avg:",grade_calculate_dic[key]['avg'],end='\n\n')
    
    # 이메일 주소 도메인별 인원 구하기
    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i]
        email_domamin = (data['email'].split("@"))[1]
        if not email_domamin in email_domain_dic.keys():
            email_domain_dic[email_domamin] = 1
        else:
            email_domain_dic[email_domamin] += 1
    print("## EMAIL 도메인 별 사용인원")
    for key in email_domain_dic.keys():
        print("#",key,": ",email_domain_dic[key],"명")
    return HttpResponse("calculate, calculate function!")
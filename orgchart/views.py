from .forms import addemployee
from django.shortcuts import render,get_object_or_404,redirect
from .models import detail
from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import login as auth_login,logout
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.urls import reverse 
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.db.models import Q
import urllib.request
import json

dic = dict()
def tree(request):
    global dic
    dic={}
    name=list()
    print("on")
    token = 'elZxQlHDSUallvL3OnnH'
    url = 'https://api.zenefits.com/core/people'
    hed = {'Authorization': 'Bearer ' + token}
    req = urllib.request.Request(url=url, headers=hed)
    content = urllib.request.urlopen(req)
    data = json.load(content)
    num = data['data']['data']
    for item in num:
        idi = item['id']
        print(idi)
        if detail.objects.filter(emp_id=idi).exists():
            ext = detail.objects.get(emp_id=idi)
            pivot = 0
            if ext.status != item['status']:
                ext.status = item['status']
                pivot=1
            if ext.preferred_name != item['preferred_name']:
                ext.preferred_name = item['preferred_name']
                pivot=1
            if ext.last_name != item['last_name']:
                ext.last_name = item['last_name']
                pivot=1
            if ext.work_phone != item['work_phone']:
                ext.work_phone = item['work_phone']
                pivot=1
            if ext.personal_email != item['personal_email']:
                ext.personal_email = item['personal_email']
                pivot=1
            if ext.location_url != item['location']['url']:
                ext.location_url != item['location']['url']
                pivot=1
            if ext.department_url != item['department']['url']:
                ext.department_url != item['department']['url']
                pivot=1
            if ext.manager_url != item['manager']['url']:
                ext.manager_url != item['manager']['url'] 
                pivot=1
            if pivot:
                ext.save()
            continue
        manager_url = item['manager']['url']
        post = detail()
        print("Nah")
        post.emp_id = idi
        print("-1")
        if item['status'] != None:
            post.status = item['status']
        print("0")
        post.last_name = item['last_name']
        post.preferred_name = item['preferred_name']
        if item['work_phone'] != None:
            post.work_phone = item['work_phone']
        print("1")
        if item['personal_email'] != None:
            post.personal_email = item['personal_email']
        print("2")
        location_url = item['location']['url']
        post.location_url = location_url
        if location_url != None:
            loc = urllib.request.Request(url=location_url, headers=hed)
            loc2 = urllib.request.urlopen(loc)
            loc3 = json.load(loc2)
            string = loc3['data']['city'] + " , " + loc3['data']['state'] + " , " + loc3['data']['country']
            post.location = string
        print("3")
        dept_url = item['department']['url']
        post.department_url = dept_url
        if dept_url != None:
            dept = urllib.request.Request(url=dept_url, headers=hed)
            dept2 = urllib.request.urlopen(dept)
            dept3 = json.load(dept2)
            post.department = dept3['data']['name']
        print("4")
        manager_url = item['manager']['url']
        post.manager_url = manager_url
        if manager_url == None:
            post.manager = "None"
            post.manager_id = "0"
        else:
            man = urllib.request.Request(url=manager_url, headers=hed)
            man2 = urllib.request.urlopen(man)
            man3 = json.load(man2)
            number = man3['data']['id']
            if item['status']=='active':
                print("dic is on")
                if number in dic:
                    dic[number].append(idi)
                else:
                    dic[number]=list()
                    dic[number].append(idi)
            post.manager = man3['data']['preferred_name'] + " " + man3['data']['last_name']
            post.manager_id = man3['data']['id']
        print("5")
        post.save()
        print("inserted")
    total = detail.objects.all()
    for value in total:
        number = value.manager_id
        idi = value.emp_id
        if value.manager == "None" and value.status=="active":
            name.append(idi)
            continue
        if number in dic:
            if idi not in dic[number]:
                dic[number].append(idi)
        else:
            dic[number]=list()
            dic[number].append(idi)
    return render(request,'orgchart/tree.html',{'total':total,'dic':dic,'name':name})


def employee_detail(request,idi):
    emp = get_object_or_404(detail, emp_id=idi)
    if emp.manager_id!=0:
        k = detail.objects.get(emp_id=emp.manager_id)
        emp.manager=k.preferred_name + " " + k.last_name
        emp.save()
    print(emp)
    return render(request,'orgchart/employee_detail.html',{'emp':emp})

def add_employee(request):
    global dic
    if request.method == "POST":
        idi = request.POST.get("manager_id")
        form = addemployee(request.POST)
        if form.is_valid():
            temp = detail.objects.get(emp_id=idi)
            name = temp.preferred_name + " " + temp.last_name
            post = form.save(commit=False)
            post.subordinates_url = 'null'
            post.manager = name
            post.save()
            return redirect('tree')
    else:
        form = addemployee()
    return render(request,'orgchart/add_employee.html',{'form':form})

def detail_edit(request,pk):
    check = get_object_or_404(detail, emp_id=pk)
    idi = check.manager_id
    if request.method == "POST" :
        form = addemployee(request.POST,instance=check)
        if form.is_valid():
            post = form.save(commit=False)
            if idi != 0:
                temp = detail.objects.get(emp_id=idi)
                name = temp.preferred_name + " " + temp.last_name
                post.manager = name
            post.subordinates_url = 'null'
            post.save()
            return redirect('employee_detail',idi = pk)
    else:
        form = addemployee(instance=check)
        return render(request,'orgchart/edit_employee.html',{'form':form})

def delete_employee(request):
    global dic
    name = request.POST.get('str')
    try:
        k=get_object_or_404(detail, emp_id=name)
        k.preferred_name = "X"
        k.last_name = " "
        k.save()
        return redirect('tree')
    except:
        message = "No Result Found"
        return render(request,'orgchart/tree.html', {'message':message})



def search_name(request):
    try:
        if request.method=="POST":
            name = request.POST.get('str')
            string = name.split()
            for s in string:
                print(s)
                print("************")
            if string:
                match = detail.objects.filter(Q(preferred_name__icontains=string[0]) | Q(last_name__icontains=string[0]))
                print("1")
                if match:
                    name = list()
                    total = detail.objects.all()
                    if len(string)==2:
                        print("y")
                        for i in match:
                            if i.last_name == string[1] or i.preferred_name == string[1]:
                                k = i.emp_id
                                name.append(k)
                    else:
                        print("z")
                        for i in match:
                            k = i.emp_id
                            name.append(k)   
                    if len(name)==0:
                        message = "No Result Found"
                        return render(request,'orgchart/tree.html', {'message':message})
                    return render(request,'orgchart/tree.html',{'name':name,'total':total,'dic':dic})
                else:
                    message = "No Result Found"
                    return render(request,'orgchart/tree.html', {'message':message})
    except:
        message = "No Result Found"
        return render(request,'orgchart/tree.html', {'message':message})

def search_id(request):
    try:
        if request.method=="POST":
            string = request.POST.get('str')
            if string:
                match = detail.objects.get(emp_id=string)
                if match:
                    name = list()
                    total = detail.objects.all()
                    name.append(match.emp_id)
                    return render(request,'orgchart/tree.html',{'name':name,'total':total,'dic':dic})
                else:
                    message = "No Result Found"
                    return render(request,'orgchart/tree.html', {'message':message})
    except:
        message = "No Result Found"
        return render(request,'orgchart/tree.html', {'message':message})

def search_location(request):
    try:
        if request.method=="POST":
            name = request.POST.get('str')
            string = name.split()
            if string:
                match = detail.objects.filter(location__icontains=string[0])
                if match:
                    name_location = list()
                    total = detail.objects.all()
                    for i in match:
                        k = i.emp_id
                        name_location.append(k)
                    return render(request,'orgchart/tree.html',{'name_location':name_location,'total':total,'dic':dic})
                else:
                    message = "No Result Found"
                    return render(request,'orgchart/tree.html', {'message':message}) 
    except:
        message = "No Result Found"
        return render(request,'orgchart/tree.html', {'message':message})

def contact(request):
    return render(request,'orgchart/contact.html', {})
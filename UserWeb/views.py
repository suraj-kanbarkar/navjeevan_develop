from .forms import StuForm, UserForm, UsersLoginForm, StuTaskForm, TeachForm, FeedbackForm, FeedUsersLoginForm, MCQCourseForm, MCQ_QueForm,MCQ_AttStuList, NewsDataForm
from TeacherStu.models import Student, User, Stu_Task, Teach_Task, Feedback, MCQ_Question, MCQ_Post, MCQ_Result, News
from django.contrib.auth.models import User as authUser
from . models import Users, FeedbackUser
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,JsonResponse
from rest_framework import compat
from django.views import View
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import json

# @login_required(login_url="/login/")
def home(request): 
    query = request.GET.get("q", None)
    template = "index.html"
    context = {"object_list": query}
    return render(request, template,context)
    
def TaskHome(request): 
    query = request.GET.get("q", None)
    template = "Taskindex.html"
    context = {"object_list": query}
    return render(request, template,context)

# Create a New Student
# @login_required(login_url="/login/") 
def create_view(request):
    query = request.GET.get("q", None)
    # print (query)
    form = StuForm(request.POST,request.FILES)
    template = "createUser.html"
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("/home/create/?q="+query)
    else: 
        form = StuForm()   
    return render(request, template, context)


# Get Infomation of Particular Student According to Id 
# @login_required(login_url="/login/")
def detail_view(request, userid=None):
    qs = get_object_or_404(Student, userid=userid)
    context = {"object" : qs}
    template = "getUserData.html"
    return render(request, template, context) 

def detail_view_user(request, id=None):
    # pass
    qs = get_object_or_404(User, id=id)
    context = {"object" : qs}
    template = "getAuthUserData.html"
    return render(request, template, context) 


# Can Upadate the Student Data
# @login_required(login_url="/login/")
def update_view(request, userid=None):
    query = request.GET.get("q", None)
    print (query)
    obj = get_object_or_404(Student, userid=userid)
    template = "updateUser.html"
    form = StuForm(request.POST or None, instance=obj)
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/stuTeachList?q="+query)
    return render(request, template, context)

def update_view_user(request, id=None):
    obj = get_object_or_404(User, id=id)
    template = "updateAuthUser.html"
    form = UserForm(request.POST or None, instance=obj)
    context = {"form": form}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/")
    return render(request, template, context)


# Can Delete the Student Data
# @login_required(login_url="/admin/")
def delete_view(request , userid=None):
    query = request.GET.get("q", None)
    print (query)
    obj = get_object_or_404(Student, userid=userid)
    context = {"object": obj,"code":query}
    template = "delete.html"
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/stuTeachList?q="+query)
    return render(request, template, context)


def delete_view_user(request , id=None):
    obj = get_object_or_404(User, id=id)
    context = {"object": obj}
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/")

    template = "deleteAuth.html"
    return render(request, template, context)


# Get Infomation of Particular Student According to Id 
# @login_required(login_url="/home/userlogin/")
def Userdata(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        name = request.POST.get('name')        
        form = UsersLoginForm(request.POST)
        qs = Users.objects.filter(name=name)
        if Users.objects.filter(name=name).exists():
            if (qs.filter(password=password).exists()):
                if form.is_valid():
                    obj = Users.objects.filter(name__iexact=name).values("name")[0]["name"] 
                    context = {"object_list" : obj}
                    template = "index.html" 
                    # print("obj"*12,obj)  
                    # messages.success(request, 'Login successfully!') 
                    # return HttpResponseRedirect("/home/", context)
                    return render(request, template, context) 
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/userlogin/")
        else:
            messages.info(request, 'Enter the Correct Name!')
            return HttpResponseRedirect("/userlogin/") 
    else: 
        form = UsersLoginForm()   
    return render(request, "userlogin.html", {"form": form})

def userlogout(request):
    return HttpResponseRedirect("/userlogin/")
 
# Show List of All Data
# @login_required(login_url="/home/userlogin/")
def stuTeachList(request):
    # print(paswd)
    # import pdb
    # pdb.set_trace()

    query = request.GET.get("q", None)
    # print(query)
    # user = User.objects.get(username=request.user.username)
    # print("User NAme" , user )
    # enable=Student.objects.filter(Enable="True")
    obj = Student.objects.filter(userid__contains=query).values().order_by('-clas')
    # print(obj)
    context = {
            "object_list" : obj,
            "code":query
        }
    template = "allList.html"    
    return render(request, template, context)

@login_required(login_url="/login/")
def usersList(request):
    query = request.GET.get("q", None)
    obj = User.objects.all().values()
    context = {
            "object_list" : obj,
            "code":query
        }
    template = "allauthList.html"    
    return render(request, template, context)

def authStuTaskList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        form = UsersLoginForm(request.POST)
        if (Users.objects.filter(name=name).exists()):
            qs = name[-3:] 
            user=Users.objects.filter(name=name)
            if (user.filter(password=password).exists()):
                if form.is_valid(): 
                        obj = Stu_Task.objects.filter(school_code=qs).values().order_by('-date')
                        obj_class = Student.objects.order_by().values('clas').distinct()
                        context = {
                                "username" : name,
                                "object_clist" : obj_class,
                                "object_list" : obj,
                                "query":qs
                            }
                        template = "allTaskList2.html" 
                        return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/Taskhome/authallTask?q=")
        else:
            messages.info(request, 'Username not exist!!!')
            return HttpResponseRedirect("/Taskhome/authallTask?q=")
    else: 
        form = UsersLoginForm()   
    return render(request, "userlogin2.html", {"form": form})
                # scode=Student.objects.filter(mobileNum=mobileNum).values_list('userid')[0][0]
                # qs = scode[-3:]
                # paswd = len(str(password))
                # if password is None or len(password)==0:
                #     messages.info(request, 'Enter the Password!')
                #     return HttpResponseRedirect("/home/authallTask?q="+query)
                
                # else:
                #     saveQuerySet = Users.objects.create(name=mobileNum,password=password)
                #     saveQuerySet.save()
                #     if form.is_valid(): 
                #         obj = Stu_Task.objects.filter(school_code=qs).values().order_by('-date')
                #         obj_class = Student.objects.order_by().values('clas').distinct()
                #         context = {
                #                 "object_clist" : obj_class,
                #                 "object_list" : obj,
                #                 "query":qs
                #             }
                #         template = "allTaskList.html" 
                #         return render(request, template, context)
        


# def authStuTaskList(request):
#     if request.method == 'POST':
#         password = request.POST.get('password')
#         name = request.POST.get('name')
#         print(name,password)
#         qs = name[-3:]       
#         form = UsersLoginForm(request.POST)
#         if (Student.objects.filter(userid=name,category='TEACHER').exists()):
#             check = Student.objects.filter(userid=name,category='TEACHER')
#             if (check.filter(userid=name,mobileNum=password).exists()):
#                 # datas = Student.objects.filter(userid=name,mobileNum=password)
#                 if form.is_valid(): 
#                     obj = Stu_Task.objects.filter(school_code=qs).values().order_by('-date')
#                     obj_class = Student.objects.order_by().values('clas').distinct()
#                     context = {
#                             "object_clist" : obj_class,
#                             "object_list" : obj,
#                             "query":qs
#                         }
#                     template = "allTaskList.html" 
#                     return render(request, template, context)
#             else:
#                 messages.info(request, 'Enter the Correct Password!')
#                 return HttpResponseRedirect("/home/authallTask?q="+query)
#         else:
#             messages.info(request, 'Enter the Username Password!')
#             return HttpResponseRedirect("/home/authallTask?q="+query) 
#     else: 
#         form = UsersLoginForm()   
#     return render(request, "userlogin.html", {"form": form})

def stuTaskList(request):
    query = request.GET.get("q", None)
    obj = Stu_Task.objects.filter(school_code=query).values().order_by('-date')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }
    template = "allTaskList.html"    
    return render(request, template, context)

def stuTaskList2(request):
    query = request.GET.get("q", None)
    obj = Stu_Task.objects.filter(school_code=query).values().order_by('-date')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allTaskList2.html"    
    return render(request, template, context)

# def allTaskList(request): 
#     query = request.GET.get("q", None)
#     template = "allTaskList.html"
#     context = {"object_list": query}
#     return render(request, template,context)

def create_Taskview(request):
    query = request.GET.get("q", None)
    form = StuTaskForm(request.POST,request.FILES)
    template = "addNewTask.html"
    context = {
            "form" : form,
            "code":query
        }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Successfully Created...!!!")
        return HttpResponseRedirect("/home/allTask?q="+query)
    else: 
        form = StuTaskForm() 
        # messages.success(request, "Something went Wrong")  
    return render(request, template, context)

def update_Taskview(request, id=None):
    query = request.GET.get("q", None)
    print (query)
    obj = get_object_or_404(Stu_Task, id=id)
    template = "updateTask.html"
    form = StuTaskForm(request.POST or None, instance=obj)
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/allTask?q="+query)
        # return taskResponse(request, query) 
    return render(request, template, context)

def delete_Taskview(request , id=None):
    query = request.GET.get("q", None)
    # query1=str(query)
    print (query)
    obj = get_object_or_404(Stu_Task, id=id)
    context = {"object": obj,"code":query}
    template = "deleteTask.html"
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allTask?q="+query)
        # return taskResponse(request, query) 
    return render(request, template, context)


def clasSearch(request, clas=None):
    query = request.GET.get("q", None)
    # print(query)
    # print(clas)
    obj = Stu_Task.objects.filter(school_code=query,clas=clas).values().order_by('-date')
    print(obj)
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }
    template = "allTaskList.html"    
    return render(request, template, context)

def create_Taskview2(request):
    query = request.GET.get("q", None)
    form = StuTaskForm(request.POST,request.FILES)
    template = "addNewTask2.html"
    context = {
            "form" : form,
            "query":query
        }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("/Taskhome/allTechTask?q="+query)
    else: 
        form = StuTaskForm()   
    return render(request, template, context)

def update_Taskview2(request, id=None):
    query = request.GET.get("q", None)
    # print (query)
    obj = get_object_or_404(Stu_Task, id=id)
    template = "updateTask2.html"
    form = StuTaskForm(request.POST or None, instance=obj)
    context = {"form": form,"query":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated post!")
        return HttpResponseRedirect("/Taskhome/allTechTask?q="+query)
        # return taskResponse(request, query) 
    return render(request, template, context)

def delete_Taskview2(request , id=None):
    query = request.GET.get("q", None)
    # query1=str(query)
    # print (query)
    obj = get_object_or_404(Stu_Task, id=id)
    context = {"object": obj,"query":query}
    template = "deleteTask2.html"
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/Taskhome/allTechTask?q="+query)
        # return taskResponse(request, query) 
    return render(request, template, context)

def clasSearch2(request, clas=None):
    query = request.GET.get("q", None)
    # print(query)
    # print(clas)
    obj = Stu_Task.objects.filter(school_code=query,clas=clas).values().order_by('-date')
    print(obj)
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allTaskList2.html"    
    return render(request, template, context)

def create_Teachview(request):
    query = request.GET.get("q", None)
    form = TeachForm(request.POST,request.FILES)
    template = "addNewTeachTask.html"
    context = {
            "form" : form,
            "code":query
        }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect('/home/allTeachTask?q='+query)
    else: 
        form = TeachForm()   
    return render(request, template, context) 

def teachTaskList(request):
    query = request.GET.get("q", None)
    obj = Teach_Task.objects.filter(school_code=query
            ).values().order_by('id')
    # print(obj)
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }

    template = "allTechTaskList.html"    
    return render(request, template, context)

def update_TechTaskview(request, id=None):
    query = request.GET.get("q", None)
    print (query)
    obj = get_object_or_404(Teach_Task, id=id)
    template = "updateTask.html"
    form = TeachForm(request.POST or None, instance=obj)
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/allTeachTask?q="+query)
    return render(request, template, context)

def delete_TechTaskview(request , id=None):
    query = request.GET.get("q", None)
    # query1=str(query)
    print (query)
    obj = get_object_or_404(Teach_Task, id=id)
    context = {"object": obj,"code":query}
    template = "deleteTechTask.html"
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allTeachTask?q="+query)
    return render(request, template, context)

def clastechSearch(request, clas=None):
    query = request.GET.get("q", None)
    # print(query)
    # print(clas)
    obj = Teach_Task.objects.filter(school_code=query,clas=clas).values().order_by('id')
    print(obj)
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }
    template = "allTechTaskList.html"    
    return render(request, template, context)

def createFeedview(request):
    query = request.GET.get("q", None)
    form = FeedbackForm(request.POST,request.FILES)
    template = "addFeedback.html"
    context = {
            "form" : form,
            "code":query
        }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect('/home/allFeedback?q='+query)
    else: 
        form = FeedbackForm()   
    return render(request, template, context) 


cred = credentials.Certificate("njms-2e633-firebase-adminsdk-xozcb-5d4d48927c.json")
app = firebase_admin.initialize_app(cred)
# add new code to get connected with firebase stored data wgich is feedback collections data.
def get_cloud_feed_data(query):
    # firstly connect to cloud frebase. 
    # query = request.GET.get("q", None)
    store = firestore.client()
    # doc_ref = store.collection(u'product')
    datas = store.collection(u'feedback')
    doc_ref = datas.where(u'school',u'==',query)
    # doc = store.collection(u'feedback').document(u'VK1WiKlsROsKzwq8E2lF').get()
    # print(f'Document data: {doc.to_dict()}')

    data = []
    try:
        docs = doc_ref.get()
        for doc in docs:
            dic1={}
            dic2=doc.to_dict()            
            dic1['id'] = (doc.id)
            dic1.update(dic2)
            data.append(dic1)
            # print(dic1)
            # print(u'Doc Data:{}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    return data


def feedList(request):
    query = request.GET.get("q", None)
    obj = Feedback.objects.filter(school_code=query
            ).values().order_by('id')
    # print(obj)
    # obj_class = Student.objects.order_by().values('clas').distinct()
    feedback_list = get_cloud_feed_data(query)
    context = {
            # "object_clist" : obj_class,
            "object_list" : feedback_list,
            "code":query
            # "feedback":feedback_list
        }

    template = "allfeedList.html"    
    return render(request, template, context)

def update_feedview(request, id=None):

    query = request.GET.get("q", None)
    template = "updateFeed.html"
    store = firestore.client()
    objs = store.collection(u'feedback').document(id)
    obj = objs.get()
    object_list=obj.to_dict()

    form = FeedbackForm(request.POST,request.FILES) 

    context = {
            "form" : form,
            "object_list": object_list,
            "code":query
            }
    if form.is_valid():
        objects = form.save(commit=False)
        objects.save()
        # if request.method == 'POST':
        objs.delete()
        return HttpResponseRedirect('/home/allFeedback?q='+query)
    
    template = "updateFeed.html"
    return render(request, template, context) 
    
    
def authFeedList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        form = FeedUsersLoginForm(request.POST)
        if (FeedbackUser.objects.filter(name=name).exists()):
            qs = name[-3:] 
            user=FeedbackUser.objects.filter(name=name)
            if (user.filter(password=password).exists()):
                if form.is_valid(): 
                        feedback_list = get_cloud_feed_data(qs)

                        context = {
                                "username" : name,
                                "object_list" : feedback_list,
                                "query":qs
                            }

                        template = "allfeedList2.html"    
                        return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/feedback/authFeed?q=")
        else:
            messages.info(request, 'Username not exist!!!')
            return HttpResponseRedirect("/feedback/authFeed?q=")
    else: 
        form = FeedUsersLoginForm()   
    return render(request, "feeduserlogin.html", {"form": form})

def allfeedList(request):
    qs = request.GET.get("q", None)
    feedback_list = get_cloud_feed_data(qs)
    context = {
            "object_list" : feedback_list,
            "query":qs
            }
    template = "allfeedList2.html"    
    return render(request, template, context)

def authupdate_feedview(request, id=None):
    qs = request.GET.get("q", None)
    template = "updateFeed2.html"
    store = firestore.client()
    objs = store.collection(u'feedback').document(id)
    obj = objs.get()
    object_list=obj.to_dict()
    print(object_list)
    form = FeedbackForm(request.POST,request.FILES) 
    context = {
            "form" : form,
            "object_list": object_list,
            "query":qs
            }
    if form.is_valid():
        objects = form.save(commit=False)
        objects.save()
        objs.delete()
        return HttpResponseRedirect('/feedback/allFeedback?q='+qs)
    
    template = "updateFeed2.html"
    return render(request, template, context) 
    

def MCQ_TopicList(request):
    query = request.GET.get("q", None)
    obj = MCQ_Post.objects.filter(school=query).values().order_by('title')
    # obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            # "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }
    template = "allMCQ_QuizTopic.html"    
    return render(request, template, context)

def create_MCQCourseview(request):
    query = request.GET.get("q", None)
    form = MCQCourseForm(request.POST,request.FILES)
    template = "addMCQ_Topic.html"
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("/home/allMCQ_Topic/?q="+query)
    else: 
        form = MCQCourseForm()   
    return render(request, template, context)

def update_MCQCourseview(request, title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    template = "updateMCQTopic.html"
    form = MCQCourseForm(request.POST or None, instance=obj)
    context = {"form": form,"query":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/allMCQ_Topic/?q="+query)
    return render(request, template, context)

def delete_MCQCourseview(request , title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    context = {"object": obj,"query":query}
    template = "deleteMCQ_Topic.html"
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allMCQ_Topic?q="+query)
    return render(request, template, context)

def MCQ_QuizQueList(request, title=None):
    # title = 'Quizz'
    query = request.GET.get("q", None)
    objs = MCQ_Question.objects.filter(MCQPost_id__school__contains=query)
    obj = objs.filter(MCQPost_id__title=title).values()
    # obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "title" : title,
            "object_list" : obj,
            "code":query
        }
    template = "allMCQ_QuizQue.html"    
    return render(request, template, context)

def create_MCQ_Queview(request, title=None):
    query = request.GET.get("q", None)
    form = MCQ_QueForm(request.POST,request.FILES)
    template = "addMCQ_Que.html"
    context = {"form": form,"objs": title,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/home/createMCQue"+title+"?q="+query)
    else: 
        form = MCQ_QueForm()   
    return render(request, template, context)

def update_MCQ_Queview(request, title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    template = "updateMCQ_Que.html"
    form = MCQ_QueForm(request.POST or None, instance=obj)
    context = {"obj": obj,"objs": title,"query":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated post!")
        messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/home/allMCQ_Que"+title+"?q="+query)
    return render(request, template, context)

def delete_MCQ_Queview(request,title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    context = {"object": obj,"objs": title,"query":query}
    template = "deleteMCQ_Que.html"
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allMCQ_Que"+title+"?q="+query)
    return render(request, template, context)
    
def MCQ_StuList(request):
    query = request.GET.get("q", None)
    obj = MCQ_Result.objects.filter(userid__icontains=query).values().order_by('title')
    user = MCQ_Result.objects.filter(userid__icontains='KAS').values_list('userid', flat=True)
    nameObj = Student.objects.filter(userid__in=user).values()
    print(nameObj)
    context = {
            "user_name" : nameObj,
            "object_list" : obj,
            "code":query
        }
    template = "allMCQ_AttStuList.html"    
    return render(request, template, context)
    
def authMCQList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        form = UsersLoginForm(request.POST)
        if (Users.objects.filter(name=name).exists()):
            query = name[-3:] 
            user=Users.objects.filter(name=name)
            if (user.filter(password=password).exists()):
                if form.is_valid(): 
                        obj = MCQ_Post.objects.filter(school=query).values().order_by('title')
                        obj_class = Student.objects.order_by().values('clas').distinct()
                        context = {
                                "object_clist" : obj_class,
                                "object_list" : obj,
                                "query":query
                            }
                        template = "allMCQ_QuizTopic2.html" 
                        return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/Taskhome/authallTask?q=")
        else:
            messages.info(request, 'Username not exist!!!')
            return HttpResponseRedirect("/Taskhome/authallTask?q=")
    else: 
        form = UsersLoginForm()   
    return render(request, "userlogin2.html", {"form": form})

def clasSearchTopic2(request, clas=None):
    query = request.GET.get("q", None)
    obj = MCQ_Post.objects.filter(school=query,clas=clas).values().order_by('title')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allMCQ_QuizTopic2.html"    
    return render(request, template, context)


def MCQ_TopicList2(request):
    query = request.GET.get("q", None)
    obj = MCQ_Post.objects.filter(school=query).values().order_by('title')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allMCQ_QuizTopic2.html"    
    return render(request, template, context)

def create_MCQCourseview2(request):
    query = request.GET.get("q", None)
    form = MCQCourseForm(request.POST)
    template = "addMCQ_Topic2.html"
    context = {
            "form": form,
            "query":query
            }
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/Taskhome/allMTopic?q="+query)
    else: 
        form = MCQCourseForm()   
    return render(request, template, context)

def update_MCQCourseview2(request, title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    template = "updateMCQTopic2.html"
    form = MCQCourseForm(request.POST or None, instance=obj)
    context = {
            "form": form,
            "query":query
            }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated post!")
        return HttpResponseRedirect("/Taskhome/allMTopic?q="+query)
    return render(request, template, context)

def delete_MCQCourseview2(request , title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    context = {
            "object": obj,
            "query":query
            }
    template = "deleteMCQ_Topic2.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/Taskhome/allMTopic?q="+query)
    return render(request, template, context)

def MCQ_QuizQueList2(request, title=None):
    # title = 'Quizz'
    query = request.GET.get("q", None)
    objs = MCQ_Question.objects.filter(MCQPost_id__school__contains=query)
    obj = objs.filter(MCQPost_id__title=title).values()
    # obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "title" : title,
            "object_list" : obj,
            "query":query
        }
    template = "allMCQ_QuizQue2.html"    
    return render(request, template, context)

def create_MCQ_Queview2(request, title=None):
    query = request.GET.get("q", None)
    form = MCQ_QueForm(request.POST,request.FILES)
    template = "addMCQ_Que2.html"
    context = {
            "form": form,
            "objs": title,
            "query":query
            }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/Taskhome/createMCQue"+title+"?q="+query)
    else: 
        form = MCQ_QueForm()   
    return render(request, template, context)

def detail_MCQ_Queview2(request,title=None, id=None):
    query = request.GET.get("q", None)
    qs = get_object_or_404(MCQ_Question, id=id)
    context = {
            "object" : qs,
            "objs": title,
            "query":query
            }
    template = "getQueData.html"
    return render(request, template, context)


def update_MCQ_Queview2(request, title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    template = "updateMCQ_Que2.html"
    form = MCQ_QueForm(request.POST or None,request.FILES,instance=obj)
    context = {
            "form":form,
            "obj": obj,
            "objs": title,
            "query":query
            }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated Post Successfully!")
        return HttpResponseRedirect("/Taskhome/allMQue"+title+"?q="+query)
    return render(request, template, context)

def delete_MCQ_Queview2(request,title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    context = {
            "object": obj,
            "objs": title,
            "query":query
            }
    template = "deleteMCQ_Que2.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/Taskhome/allMQue"+title+"?q="+query)
    return render(request, template, context)

def MCQ_StuList2(request):
    query = request.GET.get("q", None)
    obj = MCQ_Result.objects.filter(userid__icontains=query).values().order_by('title')
    context = {
            "object_list" : obj,
            "query":query
        }
    template = "allMCQ_AttStuList2.html"    
    return render(request, template, context)

def delete_MCQStu2(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Result, id=id)
    context = {
            "object": obj,
            "query":query
            }
    template = "deleteMCQ_Stu2.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/Taskhome/allMStu?q="+query)
    return render(request, template, context)
    
def NewsDataList(request):
    query = request.GET.get("q", None)
    obj = News.objects.all()

    context = {
            "object_list" : obj,
            "code":query
        }
    template = "allNewsDataList.html"    
    return render(request, template, context)

def create_NewsData(request, id=None):
    query = request.GET.get("q", None)
    form = NewsDataForm(request.POST,request.FILES)
    template = "addNewsData.html"
    # context = {"form": form,"code":query,'typeList':_dict}
    _dict = {}
    # context={}
    if "search" in request.POST:
        school_code = request.POST.get("school_code")
        class_code = request.POST.get("class_code")
        data = Student.objects.filter(clas=class_code,userid__icontains=school_code).values_list('name',flat=True)
        
        for x in range(len(data)):
            _dict[data[x]] = data[x]
    context = {"form": form,"code":query,'typeList':_dict} 
    if form.is_valid():
        
        if "save" in request.POST:
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, 'Data Save Successfully!')
            return HttpResponseRedirect("/home/allNewsData?q="+query)
    else: 
        form = NewsDataForm()      
    return render(request, template, context) 

def update_NewsData(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(News, id=id)
    template = "updateNews.html"
    form = NewsDataForm(request.POST or None, instance=obj)
    _dict = {}

    # context = {"form": form,"query":query}
    if "search" in request.POST:
        school_code = request.POST.get("school_code")
        class_code = request.POST.get("class_code")
        data = Student.objects.filter(clas=class_code,userid__icontains=school_code).values_list('name',flat=True)
        
        for x in range(len(data)):
            _dict[data[x]] = data[x]
    context = {"form": form,"query":query,'typeList':_dict} 
    if form.is_valid():
        if "save" in request.POST:
            obj = form.save(commit=False)
            obj.save()
            # messages.success(request, "Updated Post Successfully!")
            return HttpResponseRedirect("/home/allNewsData?q="+query)
    return render(request, template, context)
    
def delete_NewsData(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(News, id=id)
    context = {"object": obj,"query":query}
    template = "deleteNewsData.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allNewsData?q="+query)
    return render(request, template, context)

# def delete_feedview(request , id=None):

#     query = request.GET.get("q", None)
#     print (query)
#     store = firestore.client()
#     obj = store.collection(u'product').document(id)
#     # obj = get_object_or_404(Feedback, id=id)
#     context = {"object": obj,"code":query}
#     template = "deletefeed.html"
#     if request.method == 'POST':
#         obj.delete()
#         messages.success(request, "Post Deleted...!")
#         return HttpResponseRedirect("/home/allFeedback?q="+query)
#     return render(request, template, context)

# def createFeedview(request):
#     query = request.GET.get("q", None)
#     form = FeedbackForm(request.POST,request.FILES)
#     template = "addFeedback.html"
#     context = {
#             "form" : form,
#             "code":query
#         }
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.save()
#         return HttpResponseRedirect('/home/allFeedback?q='+query)
#     else: 
#         form = FeedbackForm()   
#     return render(request, template, context)

# def stuTeachList(request):
#     query = request.GET.get("q", None)
#     print(query)
#     obj = Student.objects.filter(userid__startswith=query,category="STUDENT"
#             ).values("userid","category","name","mobileNum").order_by('-id')
#     context = {
#             "object_list" : obj,
#             "code":query
#         }
#     template = "allList.html"    
#     return render(request, template, context)


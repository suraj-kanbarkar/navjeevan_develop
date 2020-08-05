from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser,ParseError
from .models import Student, Video, User, News, Stu_Task, Teach_Task, Feedback, MCQ_Post, MCQ_Question, MCQ_Answer, MCQ_Result
from django.shortcuts import render #Default
from django.http import *
from django.shortcuts import get_object_or_404 #get object(error) when object not exist
from rest_framework.views import APIView #API data
from rest_framework.response import Response #Successful 200 response
from rest_framework import status #send back status 
from . import services
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import json
from django.db.models import Q
from . serializers import stuSerializer, videoSerializer, userSerializer, newsSerializer, stuTaskSerializer, noteSerializer, feedbackSerializer, MCQ_QueSerializer, MCQ_PostSerializer, MCQ_AnswerSerializer, MCQ_ResultSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class stulist(APIView):

    def get(self, request):
    	enable=Student.objects.filter(Enable="True")
    	stu_list=enable.all()
    	serializer=stuSerializer(stu_list,many=True)
    	return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        mobileNum = data.get('mobileNum')
        # if (Student.objects.filter(mobileNum=mobileNum).exists()):
        if (User.objects.filter(mobileNum=mobileNum).exists()):
            return services.UserLogin(request)
        else:
            password = data.get('password',None)
            paswd = len(str(password))
            print(paswd)
            # print(paswd)
            # import pdb
            # pdb.set_trace()

            if password is None or len(password)==0:
                return services.MesgResponse(mobileNum,mesg="Please Enter Password.",status=204) 
            
            else:
                # return services.MesgResponse(mobileNum,mesg=" Password.",status=204) 
                saveQuerySet = User.objects.create(mobileNum=mobileNum,password=password)
                saveQuerySet.save()
                return services.LoginDataSuccessResponse(mobileNum,status=200) 
        # else:
            # return services.MesgResponse(mobileNum,mesg='Enter Valid Mobile Number...',status=204)

@api_view(['POST',])
def checkMobileNum(request):
	mobileNum = request.data.get('mobileNum',None)
	enable=Student.objects.filter(Enable="True")
	if (enable.filter(mobileNum=mobileNum).exists()):
		if (enable.filter(mobileNum=mobileNum).exists()):
			return services.MesgResponse(mobileNum,mesg='Mobile Number is Valid...',status=status.HTTP_201_CREATED)
		else:
			return services.MesgResponse(mobileNum,mesg='Mobile Number is Invalid...',status=status.HTTP_400_BAD_REQUEST)    
	else:
		return services.MesgResponse(mobileNum,mesg='User is Blocked from School',status=status.HTTP_400_BAD_REQUEST)


class FileView(APIView):
	parser_classes = (MultiPartParser, FormParser)

	def get(self, request):
		stu_list=Video.objects.all()
		serializer=videoSerializer(stu_list,many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
	 	file_serializer = videoSerializer(data=request.data)
	 	if file_serializer.is_valid():
	 		file_serializer.save()
	 		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
	 	else:
	 		return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
class NewsView(APIView):

	def get(self, request):
		news_list=News.objects.all()
		serializer=newsSerializer(news_list,many=True)
		return Response(serializer.data)

	def post(self, request):
		data=self.request.data
		user_code = data.get('user_code')
		ucode = user_code[0:3]
		# tcode = user_code[-3:]
		if (Student.objects.filter(userid=user_code).exists()):
			reqCls = Student.objects.filter(userid=user_code).values_list('clas',flat=True)[0]
			stuCls = News.objects.filter(class_code=reqCls)
			stuSchool = News.objects.filter(school_code=ucode)
			news_list= (stuCls.filter(school_code=ucode).values() | stuCls.filter(school_code="ALL").values() | stuSchool.filter(class_code='ALL').values() | News.objects.filter(school_code='ALL',class_code='ALL').values())
			serializer=newsSerializer(news_list,many=True)
			return Response(serializer.data)
		else:
			return services.MesgResponse(user_code, mesg='User-Code not Exist...!!!', status=status.HTTP_400_BAD_REQUEST)
			

 
class stuTaskList(APIView):

    def get(self, request):
        stuTask_list=Stu_Task.objects.all()
        serializer=stuTaskSerializer(stuTask_list,many=True)
        return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        school_code = data.get('school_code')
        clas = data.get('clas')
        date = data.get('date')
        if (Stu_Task.objects.filter(school_code=school_code).exists()):
        	scode = Stu_Task.objects.filter(school_code=school_code)
        	if (scode.filter(clas=clas).exists()):
        		stu_list=scode.filter(clas=clas).values()
        		if (stu_list.filter(date=date).exists()):
        			dvalue=stu_list.filter(date=date).values()
        			# dvalue.filter(date=date).values()
	        		serializer=stuTaskSerializer(dvalue,many=True)
	        		return Response(serializer.data)
	        	else:
	        		return services.MesgResponse(clas,mesg="Date Not Exist",status=status.HTTP_400_BAD_REQUEST)
        	else:
        		return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
        else:
        	return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 

class notesList(APIView):

    def get(self, request):
        note_list=Teach_Task.objects.all()
        serializer=noteSerializer(note_list,many=True)
        return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        school_code = data.get('school_code')
        clas = data.get('clas')
        if (Teach_Task.objects.filter(school_code=school_code).exists()):
        	scode = Teach_Task.objects.filter(school_code=school_code)
        	if (scode.filter(clas=clas).exists()):
        		stu_list=scode.filter(clas=clas).values()
        		serializer=noteSerializer(stu_list,many=True)
        		return Response(serializer.data)
        	else:
        		return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
        else:
        	return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 

class feedBackList(APIView):

    def get(self, request):
        feed_list=Feedback.objects.all()
        serializer=feedbackSerializer(feed_list,many=True)
        return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        school_code = data.get('school_code')
        userid = data.get('userid')
        if (Feedback.objects.filter(school_code=school_code).exists()):
        	scode = Feedback.objects.filter(school_code=school_code)
        	if (scode.filter(userid=userid).exists()):
        		stu_list=scode.filter(userid=userid).values()
        		serializer=feedbackSerializer(stu_list,many=True)
        		return Response(serializer.data)
        	else:
        		return services.MesgResponse(userid,mesg="User-Id Not Exist",status=status.HTTP_400_BAD_REQUEST)
        else:
        	return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 

class MCQ_PostTopicView(APIView):
	
	def get(self, request):
		MCQ_Data = MCQ_Post.objects.all()
		MCQue_Data = MCQ_Question.objects.all() 
		serializer1 = MCQ_QueSerializer(MCQue_Data,many=True)
		# serializer = MCQ_PostSerializer(MCQ_Data,many=True) 
		Serializer_list = serializer1.data
		return Response(Serializer_list)

	def post(self, request):
		data=self.request.data
		school = data.get('school')
		clas = data.get('clas')
		userid = data.get('userid')
		if (MCQ_Post.objects.filter(school=school).exists()):
			scode = MCQ_Post.objects.filter(school=school)
			if (scode.filter(clas=clas).exists()):
				clas_list=scode.filter(clas=clas).values()
				serializer=MCQ_PostSerializer(clas_list,many=True)
				return Response(serializer.data)
			else:
				return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
		else:
			return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
def MCQ_QueView(request):
	data=request.data
	title = data.get('title')
	school = data.get('school')
	clas = data.get('clas')
	if (MCQ_Question.objects.filter(MCQPost_id__school__contains=school).exists()):
		scode = MCQ_Question.objects.filter(MCQPost_id__school__contains=school)
		if (scode.filter(MCQPost_id__clas__contains=clas).exists()):
			clas_list=scode.filter(MCQPost_id__clas__contains=clas).values()
			if (clas_list.filter(MCQPost_id__title__contains=title).exists()):
				sublist = clas_list.filter(MCQPost_id__title__contains=title).values()
				# serializer=MCQ_QueSerializer(sublist,many=True)
				serializer = list(sublist)
				# mesg=list(sublist)
				# return Response(serializer)
				questions_list = []
				options_list = []
				asnwers_list = []
				flag_list = []
				url_list = []

				if len(serializer)>0:
					for elm in serializer:
						que_title = elm["que_title"]
						choice_1 = elm["choice_1"]
						choice_2 = elm["choice_2"]
						choice_3 = elm["choice_3"]
						choice_4 = elm["choice_4"]
						correct_answer = elm["correct_answer"]
						flag = elm["flag"]
						que_Image = elm["que_Image"]
						# print(flag_list,url_list)

						questions_list.append(elm["que_title"])
						options_list.append([elm["choice_1"],elm['choice_2'],elm['choice_3'],elm['choice_4']])
						asnwers_list.append(elm["correct_answer"])
						flag_list.append(elm["flag"])
						url_list.append(elm["que_Image"])

				data = {}
				data["questions_list"] = questions_list 
				data["options_list"] = options_list 
				data["asnwers_list"] = asnwers_list
				data["flag_list"] = flag_list
				data["url_list"] = url_list
				# print(data)
				return Response(data)
			else:
				return services.MesgResponse(title,mesg="Subject Not Exist",status=status.HTTP_400_BAD_REQUEST)
		else:
			return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
	else:
		return services.MesgResponse(school,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 


def Apidata(res):
	ansData_list = []
	Question_answer = []
	if (len(res)>0):
		userid = "userid"
		title = "title"
		subject = "subject"

		for elm in res:
			question = elm["question"]
			answer = elm["answer"]

			Question_answer.append({
                "question":question,
                "answer":answer
            })

		ansData_list.append({
			"userid":userid,
			"title":title, 
			"subject":subject,
			"Question_answer":Question_answer
			})

	data = {}
	data = ansData_list
	return data


class MCQ_AnswerData(APIView):

	def get(self, request):
		ans_list=MCQ_Answer.objects.all()
		serializer=MCQ_AnswerSerializer(ans_list,many=True)
		return Response(serializer.data)

	def post(self, request):
		data=request.data
		ans_serializer = MCQ_AnswerSerializer(data=request.data)
		if ans_serializer.is_valid():
			ans_serializer.save()
			res = ans_serializer.data
			return Response(res, status=status.HTTP_201_CREATED)
		else:
			return Response(ans_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	 	

@api_view(['POST'])
def MCQ_FansView(request):
	data=request.data
	userid = data.get('userid')
	title = data.get('title')
	subject = data.get('subject')
	question = data.get('question')
	answer = data.get('answer')
	clas = data.get('clas')
	que_Image = data.get('que_Image')


	if (MCQ_Post.objects.filter(subject=subject,title=title).exists()):
		if (MCQ_Answer.objects.filter(userid=userid,subject=subject,title=title).exists()):
			que_ans = MCQ_Answer.objects.filter(userid=userid,subject=subject,title=title).values()
			serializer=MCQ_AnswerSerializer(que_ans,many=True)
			res = serializer.data
			result , wrong_ans = 0,0 
			ansData_list = []
			Question_answer = []
			tQues = (len(res))
			if (len(res)>0):
				for elm in res:
					question = elm["question"]
					answer = elm["answer"]
					que_Image = elm["que_Image"]
					if (MCQ_Question.objects.filter(que_title=question,correct_answer=answer,que_Image=que_Image).exists()):
						result += 1
					else:
						result += 0
				wrong_ans = tQues-result
				cor_ans = tQues - wrong_ans

			if (MCQ_Result.objects.filter(userid=userid,title=title).exists()):
				print(MCQ_Result.objects.filter(userid=userid,title=title).values())
				return services.MesgResponse(userid,mesg="Student already attend the Quiz,Result Exist with this User-Id!!!",status=status.HTTP_400_BAD_REQUEST)
			else :
				saveQuerySet = MCQ_Result.objects.create(userid=userid,clas=clas,title=title,subject=subject,result=result,total=tQues,correct=cor_ans,wrong=wrong_ans)
				saveQuerySet.save()	
				return JsonResponse({
						"success":True,
						"userid":userid,
						"Score":result,
						"Total Question":tQues,
						"Wrong Answer":wrong_ans,
						"status_code":200
						},status=200)
		else:
			return JsonResponse({
					"success":False,
					"User-Id, Subject, Title": (userid, subject,title),
					"Data":"Data Not Exist of that User-Id, Title and Subject",
					},status=status.HTTP_400_BAD_REQUEST) 
	else: 
		return JsonResponse({
					"success":False,
					"Data":"Data Not Exist of that Title and Subject",
					},status=status.HTTP_400_BAD_REQUEST)

class MCQ_ResultData(APIView):

	def get(self, request):
		res_list=MCQ_Result.objects.all()
		serializer=MCQ_ResultSerializer(res_list,many=True)
		return Response(serializer.data)

	def post(self, request):
		data=self.request.data
		school = data.get('school')
		clas = data.get('clas')
		userid = data.get('userid')
		date = data.get('date')
		if (MCQ_Result.objects.filter(userid=userid).exists()):
			utitle=MCQ_Result.objects.filter(userid=userid).values_list('title', flat=True)
			if (MCQ_Post.objects.filter(school=school).exists()):
				scode = MCQ_Post.objects.filter(school=school)
				if (scode.filter(clas=clas,date=date).exists()):
					clas_list=scode.filter(clas=clas,date=date).exclude(title__in=utitle)
					serializer=MCQ_PostSerializer(clas_list,many=True)
					return Response(serializer.data)
				else:
					return services.MesgResponse(clas,mesg="Class or Date Not Exist",status=status.HTTP_400_BAD_REQUEST)
			else:
				return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST)
		else:
			if (MCQ_Post.objects.filter(school=school).exists()):
				scode = MCQ_Post.objects.filter(school=school)
				if (scode.filter(clas=clas,date=date).exists()):
					clas_list=scode.filter(clas=clas,date=date).values()
					serializer=MCQ_PostSerializer(clas_list,many=True)
					return Response(serializer.data)
				else:
					return services.MesgResponse(clas,mesg="Class or Date Not Exist",status=status.HTTP_400_BAD_REQUEST)
			else:
				return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 
 
                                                                                            
    

@api_view(['GET',])
def userData(request):
      stu_list=User.objects.all()
      serializer=userSerializer(stu_list,many=True)
      return Response(serializer.data)
    
@api_view(['POST',])
def addNews(request):
  	 	file_serializer = newsSerializer(data=request.data)
  	 	if file_serializer.is_valid():
  	 		file_serializer.save()
  	 		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
  	 	else:
  	 		return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def getUserData(request):
  	userid = request.data.get('userid',None)
  	if (Video.objects.filter(userid=userid).exists()):
  		stu_list=Video.objects.filter(userid=userid).values()
  		mesg=list(stu_list)
  		return Response(mesg)
  	else:
  		return services.MesgResponse(userid,mesg="Mobile Number Not Exist",status=204)

@api_view(['POST',])
def addShipmentAPIView(request):
      stuItems = {}
      stuItemList = []
  
      userid = request.data.get('userid', None)
      name = request.data.get('name', None)
      fatherName = request.data.get('fatherName', None)
      clas = request.data.get('clas', None)
      mobileNum = request.data.get('mobileNum ',None)
      category = request.data.get('category',None)
      saveQuerySet = Student.objects.create(userid=userid,name =name,fatherName = fatherName,clas = clas,mobileNum =mobileNum,category =category)
      saveQuerySet.save()
      stuItemList.append({
              "userid":saveQuerySet.userid,
              "name": saveQuerySet.name,
              "fatherName": saveQuerySet.fatherName,
              "clas": saveQuerySet.clas,
              "mobileNum": saveQuerySet.mobileNum,
              "category": saveQuerySet.category,
          })
      stuItems["stuItems"] = stuItemList
      return services.SuccessResponse(stuItems, status=200)	
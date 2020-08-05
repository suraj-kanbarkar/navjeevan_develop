from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from . import views

urlpatterns = [

    path('data/', views.stulist.as_view()),
    path('videoFile/', views.FileView.as_view(),name='Get/Post-File'),
    path('getuserData/', views.getUserData, name='POST-Get-UserData-with-userid'),
    path('stuUpload/', views.addShipmentAPIView, name='AddShipmentAPIView'), 
    path('userData/', views.userData, name='userData'),
    path('checkNum/', views.checkMobileNum, name='checkMobileNum'),
    path('newsData/', views.NewsView.as_view(),name='Get/Post-File'), 
    path('newsUpload/', views.addNews, name='addNews'), 
    # path('videoFile/<int:id>/', views.FileView.as_view()),
    path('stuTaskData/', views.stuTaskList.as_view()), 
    path('notesData/', views.notesList.as_view()),
    path('feedBackData/', views.feedBackList.as_view()),
    url(r'^MCQViewData/', views.MCQ_PostTopicView.as_view(), name='MCQTopic_Data_WithGET_Data_classAndSchool'), 
    url(r'^MCQ_QueData/', views.MCQ_QueView, name='MCQ_QuestionData_AnswerData_AccToTitle_SchoolandClass'),
    url(r'^MCQansData/', views.MCQ_AnswerData.as_view(), name='MCQAnswerData'), 
    url(r'^MCQcheckansData/', views.MCQ_FansView, name='MCQ_CheckAnswerData'),
    url(r'^MCQResData/', views.MCQ_ResultData.as_view(), name="MCQ_ResultData_and_GettingListof_Quizz_those_StudentDon't_attendQuiz"),     

]



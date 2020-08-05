from rest_framework import serializers
from . models import Student, Video, User, News, Stu_Task, Teach_Task, Feedback, MCQ_Post, MCQ_Question, MCQ_Answer, MCQ_Result

class stuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class videoSerializer(serializers.ModelSerializer):

  class Meta():
    model = Video
    fields = '__all__'

class userSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = User
        fields = '__all__'
        
class newsSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = News
        fields = '__all__'
        
class stuTaskSerializer(serializers.ModelSerializer):

  class Meta():
    model = Stu_Task
    fields = '__all__'
    
class noteSerializer(serializers.ModelSerializer):

  class Meta():
    model = Teach_Task
    fields = '__all__' 
    
class feedbackSerializer(serializers.ModelSerializer):

  class Meta():
    model = Feedback
    fields = '__all__' 
    
class MCQ_PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MCQ_Post
        fields = '__all__'

class MCQ_QueSerializer(serializers.ModelSerializer):

    MCQPost_id = MCQ_PostSerializer(read_only=True)
    
    class Meta:
        model = MCQ_Question
        fields = ('id','que_title','flag', 'que_Image', 'choice_1', 'choice_2','choice_3' ,'choice_4' ,'correct_answer' ,'created_at', 'updated_at','MCQPost_id')
        # fields = '__all__'

class MCQ_AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MCQ_Answer
        fields = '__all__' 

class MCQ_ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MCQ_Result
        fields = '__all__'       
                
   
        

        
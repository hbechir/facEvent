from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event,Question,Answer
from user.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        
        
class QuestionSerializer(serializers.ModelSerializer):
    Answer = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'
        
    def get_Answer(self, obj):
        answers = Answer.objects.filter(question=obj)
        serializer = AnswerSerializer(answers, many=True)
        return serializer.data

    def get_author(self, obj):
        user = User.objects.get(id=obj.author.id)
        full = self.context.get('full', False)
        if full:
            serializer = UserSerializer(user)
        else:
            return user.username
        return serializer.data
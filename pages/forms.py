from ast import Mod
from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Comment, Accommodations, Question


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['username'].widget.attrs['class'] = 'register_inputs'
        self.fields['email'].widget.attrs['placeholder'] = 'email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'

# class CommentForm(ModelForm):
#     class Meta:
#         model  = Comment
#         fields = '__all__'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['accommodation'].widget.attrs['placeholder'] = 'Select accommodation...'
        self.fields['accommodation'].widget.attrs['name'] = 'accommodation'
        self.fields['subject'].widget.attrs['placeholder'] = 'Write a subject...'
        self.fields['subject'].widget.attrs['name'] = 'subject'
        self.fields['comment'].widget.attrs[
            'placeholder'] = 'Leave some comment... (500 words max)'
        self.fields['comment'].widget.attrs['name'] = 'comment'


class QuestionForm(ModelForm):
    #answer = forms.CharField(widget=forms.HiddenInput(),initial='good')
    class Meta:
        model = Question
        fields = ('question', 'accommodation')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs[
            'placeholder'] = 'Write your question here.... (500 words max)'


class AnswerForm(ModelForm):
    class Meta:
        model = Question
        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs[
            'placeholder'] = 'Write your answer here.... (500 words max)'

from django.test import TestCase
from .models import Accommodations , Comment , Question, Region 
from .forms import CommentForm , QuestionForm , AnswerForm

class URLtests(TestCase):
  def test_testhomepage(self):
    response = self.client.get('/home')
    self.assertEqual(response.status_code , 200)


class APPmodelTest(TestCase):
  def test_region(self):
    name = Region.objects.create(name = "Victoria Park")
    self.assertEqual(str(name) , "Victoria Park")

  def test_accommodation(self):
    name = Accommodations.objects.create(name = "Cantebury House")
    self.assertEqual(str(name) , "Cantebury House")

  def test_Comment(self):
    accommodation = Accommodations(name = "Cantebury House")
    accommodation.save()
    comment = Comment.objects.create(accommodation = accommodation , comment = "oh god dam this is the most beautiful thing ever seen this is bananana")
    self.assertEqual(str(comment) ,"oh god damn this is the most beautiful thing ever seen this is bananana" )

  def test_questions(self):
    accommodation = Accommodations(name = "Cantebury House")
    accommodation.save()
    question = Question.objects.create(accommodation = accommodation , question = "how r a?")
    self.assertEqual(str(question) , "how r a?")


class appFormTest(TestCase):
  
  def test_comment_form(self):
    accommodation = Accommodations(name = "Cantebury House")
    accommodation.save()
    form = CommentForm(data = { 'accommodation' : accommodation , 'subject':'its alright' , 'comment':"hell ya"})
    self.assertTrue(form.is_valid())

  def test_question_form(self):
    accommodation = Accommodations(name = "Cantebury House")
    accommodation.save()
    form = QuestionForm(data = {'accommodation':accommodation, 'question':"what is going with you all?"})
    self.assertTrue(form.is_valid())

  def test_answer_form(self):
    accommodation = Accommodations(name = "Cantebury House")
    accommodation.save()
    question = Question.objects.create(accommodation = accommodation , question = "how r a?")
    form = AnswerForm(data = {'answer':"ist good"})
    self.assertTrue(form.is_valid())

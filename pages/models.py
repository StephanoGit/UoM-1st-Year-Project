
from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Min
from better_profanity import profanity




class Region(models.Model):
  name = models.CharField(max_length=200)
  image = models.ImageField(null = True , blank = True )

  def __str__(self):
      return self.name


class Accommodations(models.Model):
  region = models.ForeignKey(Region,on_delete= models.SET_NULL , null = True)
  name = models.CharField(max_length=200)
  occupancy = models.CharField(max_length=200 , null=True)
  student_type = models.CharField(null=True , max_length= 50)
  price = models.IntegerField(null=True)
  bathroom = models.CharField(null=True , max_length=20)
  campus = models.CharField(max_length = 200,null=True)
  catering = models.CharField(max_length=100,null=True)
  post_code = models.CharField(null=True , max_length= 50)
  image = models.ImageField(null = True , blank = True )

  def __str__(self):
      return self.name


class Comment(models.Model):
    # user = models.ForeignKey(User , on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodations, on_delete=models.CASCADE)
    subject = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    value_of_money = models.FloatField(blank=True, null=True)
    location = models.FloatField(blank=True, null=True)
    internet = models.FloatField(blank=True, null=True)
    social = models.FloatField(blank=True, null=True)
    overall = models.FloatField(blank=True, null=True)

    def __str__(self):
      return self.comment

class Question(models.Model):
  accommodation = models.ForeignKey(Accommodations , on_delete=models.CASCADE)
  question = models.TextField(null = True , blank = True)
  answer = models.TextField(null = True, blank = True, default='')

  def __str__(self):
    return self.question

class Image_table(models.Model):
  accommodation = models.ForeignKey(Accommodations , on_delete=models.CASCADE)
  images = models.ImageField(null = True, blank = True)

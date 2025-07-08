from django.db import models
from django.contrib.auth.models import User


class Authors(models.Model):
    au_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=50, null=True)
    year_born = models.SmallIntegerField(null=True)

    def __str__(self):
        return self.author

class Publishers(models.Model):
    pubid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=10, null=True)
    zip = models.CharField(max_length=15, null=True)
    telephone = models.CharField(max_length=15, null=True)
    fax = models.CharField(max_length=15, null=True)
    comments = models.TextField(null=True)

    def __str__(self):
        return self.name

class Titles(models.Model):
    title = models.CharField(max_length=255, null=True)
    year_published = models.SmallIntegerField(null=True)
    isbn = models.CharField(primary_key=True, max_length=20)
    pubid = models.ForeignKey(Publishers, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, null=True)
    notes = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=50, null=True)
    comments = models.TextField(null=True)
    author = models.ManyToManyField(Authors, related_name="titles")
    cover = models.ImageField(upload_to='images/', null=True)
    

    def __str__(self):
        return self.title
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    close = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'title']

    def __str__(self):
        return f"{self.title.title} - {self.user.last_name}({self.start} - {self.end})"

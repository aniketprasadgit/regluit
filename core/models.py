from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Campaign(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500, null=False)
    description = models.CharField(max_length=10000, null=False)
    target = models.FloatField(null=False)
    deadline = models.DateTimeField(null=False)
    paypal_receiver = models.CharField(max_length=100, null=True)
    amazon_receiver = models.CharField(max_length=100, null=True)
    work = models.ForeignKey("Work", related_name="campaigns")

    def __unicode__(self):
        return u"Campaign for %s" % self.work.title


class Work(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1000)
    openlibrary_id = models.CharField(max_length=50, null=True)

    @classmethod
    def get_by_isbn(klass, isbn):
        for w in Work.objects.filter(Q(editions__isbn_10=isbn) | Q(editions__isbn_13=isbn)):
            return w
        return None

    def cover_image_small(self):
        first_isbn = self.editions.all()[0].isbn_10
        return "http://covers.openlibrary.org/b/isbn/%s-S.jpg" % first_isbn

    def __unicode__(self):
        return self.title


class Author(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500)
    openlibrary_id = models.CharField(max_length=50, null=True)
    works = models.ManyToManyField("Work", related_name="authors")

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500)
    works = models.ManyToManyField("Work", related_name="subjects")

    def __unicode__(self):
        return self.name


class Edition(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1000)
    description = models.TextField(default='', null=True)
    publisher = models.CharField(max_length=255)
    publication_date = models.CharField(max_length=50)
    isbn_10 = models.CharField(max_length=10, null=True)
    isbn_13 = models.CharField(max_length=13, null=True)
    openlibrary_id = models.CharField(max_length=50, null=True)
    work = models.ForeignKey("Work", related_name="editions", null=True)

    def __unicode__(self):
        return self.title

    @classmethod
    def get_by_isbn(klass, isbn):
        for e in Edition.objects.filter(Q(isbn_10=isbn) | Q(isbn_13=isbn)):
            return e
        return None

class EditionCover(models.Model):
    openlibrary_id = models.IntegerField()
    edition = models.ForeignKey("Edition", related_name="covers")


class Wishlist(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, related_name='wishlist')
    works = models.ManyToManyField('Work', related_name='wishlists')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tagline = models.CharField(max_length=140, blank=True)

from regluit.core import signals

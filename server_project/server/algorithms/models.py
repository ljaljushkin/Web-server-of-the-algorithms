# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
# * Rearrange models' order
# * Make sure each model has one field with primary_key=True
# * Remove `managed = True` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True,max_length=45)
    password = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    account_cash = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user'


class TestData(models.Model):
    testdata_id = models.AutoField(primary_key=True)
    input_data = models.CharField(max_length=1000)
    output_data = models.CharField(max_length=1000)
    run_options = models.CharField(max_length=1000)

    class Meta:
        managed = True
        db_table = 'test_data'


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'status'


class Algorithm(models.Model):
    algorithm_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, db_column='user_id')
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    source_code = models.TextField(blank=True)
    status_id = models.ForeignKey(Status, db_column='status_id')
    build_options = models.CharField(unique=False, max_length=1000)
    testdata_id = models.ForeignKey(TestData, db_column='testdata_id')
    price = models.IntegerField()
    language = models.CharField(unique=False, max_length=100)

    class Meta:
        managed = True
        db_table = 'algorithm'


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = True
        db_table = 'tag'


class TagList(models.Model):
    taglist_id = models.AutoField(primary_key=True)
    algorithm_id = models.ForeignKey('Algorithm', db_column='algorithm_id')
    tag_id = models.ForeignKey('Tag', db_column='tag_id')

    class Meta:
        managed = True
        db_table = 'tag_list'

class BoughtAlgorithm(models.Model):
    boughtalgs_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', db_column='user_id')
    algorithm_id = models.ForeignKey('Algorithm', db_column='algorithm_id')

    class Meta:
        managed = True
        db_table = 'bought_algorithms'

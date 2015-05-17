# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
# * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = True` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class EnumField(models.Field):
    def __init__(self, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        assert self.choices, "Need choices for enumerator"

    def db_type(self, connection):
        if not all(isinstance(col, basestring) for col, _ in self.choices):
            raise ValueError("MySQL ENUM values should be strings")

        return "ENUM({})".format(",".join("'{}'".format(col) for col, _ in self.choices))


# class Language(EnumField, models.CharField):
#     def __init__(self, *args, **kwargs):
#         flavors = [('cpp',  'C++'),
#                    ("pascal", "Pascal"),
#                    ("cs", "C#"),
#                    ]
#         kwargs.setdefault('choices', flavors)
#         super(Language, self).__init__(*args, **kwargs)


class User(models.Model):
    # user_id = models.IntegerField(primary_key=True)
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True,max_length=45)
    password = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    account_cash = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user'


class TestData(models.Model):
    # testdata_id = models.IntegerField(primary_key=True)
    testdata_id = models.AutoField(primary_key=True)
    input_data = models.CharField(max_length=1000)
    output_data = models.CharField(max_length=1000)
    run_options = models.CharField(max_length=1000)

    class Meta:
        managed = True
        db_table = 'test_data'


class Algorithm(models.Model):
    # algorithm_id = models.IntegerField(primary_key=True)
    algorithm_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', db_column='user_id')
    algorithm_name = models.CharField(unique=True, max_length=100)
    algorithm_description = models.TextField(blank=True)
    source_code = models.TextField(blank=True)
    status_id = models.ForeignKey('Status', db_column='status_id')
    build_options = models.CharField(unique=False, max_length=1000)
    testdata_id = models.ForeignKey('TestData', db_column='testdata_id')
    price = models.IntegerField()
    language = models.CharField(unique=False, max_length=100)
    # language = Language(max_length=20)

    class Meta:
        managed = True
        db_table = 'algorithm'


class Tag(models.Model):
    tag_id = models.IntegerField(primary_key=True)
    tag_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'tag'


class Status(models.Model):
    # status_id = models.IntegerField(primary_key=True)
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'status'


class TagList(models.Model):
    taglist_id = models.IntegerField(primary_key=True)
    algorithm_id = models.ForeignKey('Algorithm', db_column='algorithm_id')
    tag_id = models.ForeignKey('Tag', db_column='tag_id')

    class Meta:
        managed = True
        db_table = 'tag_list'

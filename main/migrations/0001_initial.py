# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='caseLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('case_execute', models.CharField(max_length=15)),
                ('case_executeResult', models.CharField(max_length=15)),
                ('case_executeTime', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='caseModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('case_versionName', models.CharField(max_length=50)),
                ('case_modelName', models.CharField(max_length=50)),
                ('case_verion', models.IntegerField(verbose_name=main.models.yyStock)),
                ('product_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='yyCasedetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('xuqiu', models.CharField(max_length=10)),
                ('case_router', models.CharField(max_length=20)),
                ('case_title', models.CharField(max_length=20)),
                ('case_pre', models.CharField(max_length=200)),
                ('case_step', models.CharField(max_length=10)),
                ('case_action', models.CharField(max_length=500)),
                ('case_actionPre', models.CharField(max_length=700)),
                ('case_prior', models.CharField(max_length=5)),
                ('case_result', models.CharField(max_length=10)),
                ('case_insru', models.CharField(max_length=30)),
                ('case_model', models.CharField(max_length=10)),
                ('case_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='yyCasefile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=20)),
                ('filepath', models.CharField(max_length=30)),
                ('case_version', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='yyStock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('creat_time', models.DateTimeField()),
                ('update_time', models.DateTimeField()),
                ('product_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='yycasedetail',
            name='case_version',
            field=models.ForeignKey(related_name='caseVersion', to='main.yyStock'),
        ),
        migrations.AddField(
            model_name='caselog',
            name='case_id',
            field=models.ForeignKey(to='main.yyCasedetail'),
        ),
    ]

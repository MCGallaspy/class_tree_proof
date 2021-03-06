# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 19:42
from __future__ import unicode_literals

import class_tree.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LearnerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(blank=True, max_length=100, null=True)),
                ('kind_id', models.IntegerField(blank=True, null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='class_tree.Node')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='learnergroup',
            name='node',
            field=mptt.fields.TreeForeignKey(default=class_tree.models.make_new_node, on_delete=django.db.models.deletion.CASCADE, to='class_tree.Node'),
        ),
        migrations.AddField(
            model_name='learner',
            name='node',
            field=mptt.fields.TreeForeignKey(default=class_tree.models.make_new_node, on_delete=django.db.models.deletion.CASCADE, to='class_tree.Node'),
        ),
        migrations.AddField(
            model_name='learner',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learner_roles', to='class_tree.User'),
        ),
        migrations.AddField(
            model_name='facility',
            name='node',
            field=mptt.fields.TreeForeignKey(default=class_tree.models.make_new_node, on_delete=django.db.models.deletion.CASCADE, to='class_tree.Node'),
        ),
        migrations.AddField(
            model_name='coach',
            name='node',
            field=mptt.fields.TreeForeignKey(default=class_tree.models.make_new_node, on_delete=django.db.models.deletion.CASCADE, to='class_tree.Node'),
        ),
        migrations.AddField(
            model_name='coach',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coach_roles', to='class_tree.User'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='node',
            field=mptt.fields.TreeForeignKey(default=class_tree.models.make_new_node, on_delete=django.db.models.deletion.CASCADE, to='class_tree.Node'),
        ),
        migrations.AddField(
            model_name='admin',
            name='node',
            field=mptt.fields.TreeForeignKey(default=class_tree.models.make_new_node, on_delete=django.db.models.deletion.CASCADE, to='class_tree.Node'),
        ),
        migrations.AddField(
            model_name='admin',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_roles', to='class_tree.User'),
        ),
    ]

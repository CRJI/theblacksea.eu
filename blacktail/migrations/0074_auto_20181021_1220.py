# Generated by Django 2.0.9 on 2018-10-21 12:20

from itertools import chain
import django.contrib.postgres.fields.jsonb
from django.db import migrations
import json

page_authors = {}
rev_authors = {}


def forward_1(apps, schema_editor):
    Story = apps.get_model('blacktail', 'Story')
    BlogPost = apps.get_model('blacktail', 'BlogPost')

    for page in chain(Story.objects.all(), BlogPost.objects.all()):
        page_authors[page.pk] = [a.pk for a in page.authors.all()]
        for rev in page.revisions.all():
            content = json.loads(rev.content_json)
            rev_authors[rev.pk] = content['authors']


def forward_2(apps, schema_editor):
    Story = apps.get_model('blacktail', 'Story')
    BlogPost = apps.get_model('blacktail', 'BlogPost')

    for page in chain(Story.objects.all(), BlogPost.objects.all()):
        author_ids = page_authors.get(page.pk)
        if author_ids:
            page.author_ids = author_ids
            page.save()

        for rev in page.revisions.all():
            author_ids = rev_authors.get(rev.pk)
            if author_ids:
                content = json.loads(rev.content_json)
                content['author_ids'] = author_ids
                rev.content_json = json.dumps(content)
                rev.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blacktail', '0073_storiesfolder_hide_title'),
    ]

    operations = [
        migrations.RunPython(forward_1),
        migrations.RemoveField(
            model_name='story',
            name='authors',
        ),
        migrations.AddField(
            model_name='story',
            name='author_ids',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='authors',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='author_ids',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
        migrations.RunPython(forward_2),
    ]

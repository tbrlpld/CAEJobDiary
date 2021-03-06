# Generated by Django 2.0.9 on 2019-05-19 16:22
from datetime import date

from django.db import migrations


# It is not possible in Django to run custom model methods during migrations.
# This is so that the correct version of the methods are used during the
# migration -- because the methods might have changed between the creation
# of the data migration and it's application.
# Therefore, all custom model methods that are supposed to be executed need to
# be redefined in the migration!
# See also https://docs.djangoproject.com/en/2.2/topics/migrations/#data-migrations

# Duplicates of model methods to be applied during migration

def _keyword_parsed_main_name(job):
    """
    Return string of the parsed `main_name` of the job
    """
    split_at_last_dot = str(job.main_name).rsplit(".", 1)
    last_dot_replaced = " ".join(split_at_last_dot)
    stripped_underscore = last_dot_replaced.replace("_", " ")
    return stripped_underscore


def _keyword_parsed_sub_dir(job):
    """
    Return parsed `sub_dir` string
    """
    split_at_slashes = job.sub_dir.split("/")
    parsed_words = set()
    for folder_name in split_at_slashes:
        parsed_words.add(folder_name)
        if "_" in folder_name:
            for word in folder_name.split("_"):
                parsed_words.add(word)
    return " ".join(parsed_words)


def _keyword_parse_fulltext(fulltext_string):
    """
    Returned parsed version of input string
    """
    parsed_words = set()
    for word in fulltext_string.split():
        parsed_words.add(word.strip("()[]\{\}!?,.\"':;-_"))
    return " ".join(parsed_words)


def _keyword_parsed_job_status(job):
    status_string = job.get_job_status_display()
    status_string = status_string.replace("/", "")
    return " ".join(status_string.split())


def _keyword_parsed_result_assessment(job):
    """
    Return keyword parsed result assessment
    """
    display_string = job.get_result_assessment_display()
    if display_string == "not ok":
        display_string += " nok"
    return display_string


def sub_date_isostring(job):
    sub_date_date = date(
        year=job.sub_date.year,
        month=job.sub_date.month,
        day=job.sub_date.day,
    )
    return sub_date_date.isoformat()


def _build_keyword_string(job):
    """
    Build a string of unique keywords describing the job

    The returned string contains whitespace separated words that help
    identify the job, e.g. to make it searchable.
    """
    unique_keywords = set()
    unique_keywords.add(str(job.job_id))
    unique_keywords.add(job.main_name)
    for word in _keyword_parsed_main_name(job).split():
        unique_keywords.add(word)
    if job.user:
        unique_keywords.add(job.user.username)
    if job.project:
        unique_keywords.add(job.project)
    for word in _keyword_parsed_sub_dir(job).split():
        unique_keywords.add(word)
    for word in _keyword_parse_fulltext(job.info).split():
        unique_keywords.add(word)
    for word in _keyword_parse_fulltext(job.result_summary).split():
        unique_keywords.add(word)
    for word in _keyword_parsed_job_status(job).split():
        unique_keywords.add(word)
    unique_keywords.add(job.get_analysis_status_display())
    for word in _keyword_parsed_result_assessment(job).split():
        unique_keywords.add(word)
    unique_keywords.add(sub_date_isostring(job))
    return " ".join(unique_keywords)


def _update_keyword_association_with_string(job, KeywordModel):
    """
    Update the keyword associations with the word in the keyword_string
    """

    words_from_associated_keywords = set([
        keyword.word for keyword in job.keywords.all()])
    words_from_string = set(job.keyword_string.split())
    # Words that are in the string but are not represented by a keyword yet
    new_word_from_string = words_from_string.difference(
        words_from_associated_keywords)
    # Words that have associated keywords but are not in the string anymore
    removed_keyword_words = words_from_associated_keywords.difference(
        words_from_string)

    added_keywords = []
    for word in new_word_from_string:
        word = word[0:200] if len(word) > 200 else word  # Trim long words
        keyword, created = KeywordModel.objects.get_or_create(word=word)
        if created:
            keyword.full_clean()
            keyword.save()
        job.keywords.add(keyword)
        added_keywords.append(keyword)

    removed_keywords = []
    for word in removed_keyword_words:
        keyword = job.keywords.get(word=word)
        job.keywords.remove(keyword)
        removed_keywords.append(keyword)
    return added_keywords, removed_keywords


# Migration functions

def add_keywords_to_data(apps, schema_editor):
    Job = apps.get_model('diary', 'Job')
    Keyword = apps.get_model('diary', 'Keyword')
    for job in Job.objects.all():
        job.keyword_string = _build_keyword_string(job)
        job.save()
        _update_keyword_association_with_string(job, Keyword)
        job.save()


def remove_keywords_from_data(apps, schema_editor):
    Job = apps.get_model('diary', 'Job')
    for job in Job.objects.all():
        job.keyword_string = ""
        job.save()
    Keyword = apps.get_model('diary', 'Keyword')
    Keyword.objects.all().delete()
    # Checking that it worked
    for job in Job.objects.all():
        assert job.keyword_string == ""
    assert Keyword.objects.count() == 0


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0006_auto_20190515_1816'),
    ]

    operations = [
        migrations.RunPython(
            add_keywords_to_data,
            remove_keywords_from_data
        ),
    ]

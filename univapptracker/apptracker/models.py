from django.db import models

# Create your models here.


# Table  CollegeLookup
class CollegeLookup(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=200)
    college_status = models.CharField(max_length=50,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self


# Table  ProgramLookup
class ProgramLookup(models.Model):
    program_id = models.AutoField(primary_key=True)
    proram_name = models.CharField(max_length=200)
    program_status = models.CharField(max_length=50,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self

# Table  ApplicationTypeLookup
class ApplicationTypeLookup(models.Model):
    application_type_id = models.AutoField(primary_key=True)
    application_type_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self


# Table  ApplicationStatusLookup
class ApplicationStatusLookup(models.Model):
    application_status_id = models.AutoField(primary_key=True)
    application_status_name = models.CharField(max_length=200)

    def __str__(self):
        return self


# Table  CheckListLookup
class CheckListLookup(models.Model):
    checklist_lookup_id = models.AutoField(primary_key=True)
    checklist_lookup_name = models.CharField(max_length=200)
    checklist_lookup_status = models.CharField(max_length=50,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self



# Table  Tracking
class apptracker_tracking(models.Model):
    tracking_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    college_name = models.CharField(max_length=255)
    program_name = models.CharField(max_length=50)
    application_type = models.CharField(max_length=50)
    application_deadline = models.DateField(null=True, blank=True)
    application_status = models.CharField(max_length=50)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    test_score_needed = models.CharField(max_length=10)
    transcripts_needed = models.CharField(max_length=10)
    cv_needed = models.CharField(max_length=10)
    reco_letters_needed = models.IntegerField(null=True, blank=True)
    personal_statement_needed = models.CharField(max_length=10,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    comments = models.CharField(max_length=255,null=True, blank=True)
    delete_flag = models.BooleanField(default=False)


    def __str__(self):
        return self 


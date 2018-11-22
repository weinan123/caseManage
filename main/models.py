from django.db import models
# Create your models here.
class yyStock(models.Model):
    version = models.CharField(max_length=10,)
    name = models.CharField(max_length=50)
    creat_time = models.DateTimeField()
    update_time = models.DateTimeField()
    product_name = models.CharField(max_length=20)
class yyCasefile(models.Model):
    filename = models.CharField(max_length=20)
    filepath = models.CharField(max_length=30)
    case_version = models.CharField(max_length=15)

    def __str__(self):
        return self.filename
class caseModel(models.Model):
    case_versionName = models.CharField(max_length=50)
    case_modelName = models.CharField(max_length=50)
    case_version = models.IntegerField(yyStock)
    product_name = models.CharField(max_length=20)

    def __str__(self):
        return self.case_versionName
class yyCasedetail(models.Model):
    xuqiu = models.CharField(max_length=10)
    case_router = models.CharField(max_length=20)
    case_title = models.CharField(max_length=20)
    case_pre = models.CharField(max_length=200)
    case_step = models.CharField(max_length=10)
    case_action = models.CharField(max_length=500)
    case_actionPre = models.CharField(max_length=700)
    case_prior = models.CharField(max_length=5)
    case_result = models.CharField(max_length=10)
    case_insru = models.CharField(max_length=30)
    case_version = models.ForeignKey(yyStock,related_name="caseVersion")
    case_model = models.CharField(max_length=10)
    case_id = models.IntegerField()
    def __str__(self):
        return self.case_title

class caseLog(models.Model):
    case_id = models.ForeignKey(yyCasedetail)
    case_execute = models.CharField(max_length=15)
    case_executeResult = models.CharField(max_length=15)
    case_executeTime = models.CharField(max_length=30)













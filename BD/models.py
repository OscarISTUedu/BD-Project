from django.db import models
class Patient(models.Model):
    med_card = models.IntegerField()
'''
class Practice(models.Model):
    name = models.CharField(
        max_length=255, null=True, db_collation="utf8mb3_general_ci"
    )
    company = models.ForeignKey(
        Companies, on_delete=models.DO_NOTHING, related_name="company"
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, related_name="faculty"
    )

    def __str__(self) -> str:
        return self.name
'''
# Create your models here.

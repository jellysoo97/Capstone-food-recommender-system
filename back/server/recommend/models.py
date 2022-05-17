from django.db import models

class Ingre(models.Model):
    ingre_id = models.AutoField(primary_key=True)
    ingre_name = models.CharField(max_length=45, blank=True, null=True)
    ingre_group_large = models.CharField(max_length=45, blank=True, null=True)
    ingre_group_small = models.CharField(max_length=45, blank=True, null=True)
    ingre_group_1 = models.CharField(max_length=45, blank=True, null=True)
    ingre_group_2 = models.CharField(max_length=45, blank=True, null=True)
    ingre_group_3 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingre'
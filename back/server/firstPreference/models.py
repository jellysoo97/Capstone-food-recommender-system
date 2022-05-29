from django.db import models


class Recipe(models.Model):
    recipe_id = models.IntegerField(primary_key=True)
    recipe_nm_ko = models.CharField(max_length=30, blank=True, null=True)
    sumry = models.CharField(max_length=100, blank=True, null=True)
    cooking_time = models.CharField(max_length=20, blank=True, null=True)
    qnt = models.CharField(max_length=20, blank=True, null=True)
    level_nm = models.CharField(max_length=20, blank=True, null=True)
    img_url = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe_main'


class Preference(models.Model):
    id = models.AutoField(primary_key=True)
    user_index = models.IntegerField(null=False, blank=False)
    recipe_id = models.IntegerField(null=False, blank=False)
    recipe_score = models.SmallIntegerField(blank=False, null=True)

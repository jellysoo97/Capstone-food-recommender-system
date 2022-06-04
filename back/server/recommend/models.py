# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class RecipeBasic(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    recipe_id = models.IntegerField(db_column='RECIPE_ID', blank=True, null=True)  # Field name made lowercase.
    recipe_nm_ko = models.TextField(db_column='RECIPE_NM_KO', blank=True, null=True)  # Field name made lowercase.
    sumry = models.TextField(db_column='SUMRY', blank=True, null=True)  # Field name made lowercase.
    cooking_time = models.TextField(db_column='COOKING_TIME', blank=True, null=True)  # Field name made lowercase.
    qnt = models.TextField(db_column='QNT', blank=True, null=True)  # Field name made lowercase.
    level_nm = models.TextField(db_column='LEVEL_NM', blank=True, null=True)  # Field name made lowercase.
    img_url = models.TextField(db_column='IMG_URL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recipe_basic'


class RecipeIngre(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    recipe_id = models.IntegerField(db_column='RECIPE_ID', blank=True, null=True)  # Field name made lowercase.
    recipe_nm_ko = models.TextField(db_column='RECIPE_NM_KO', blank=True, null=True)  # Field name made lowercase.
    energy = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    carbo = models.FloatField(blank=True, null=True)
    fiber = models.FloatField(blank=True, null=True)
    calcium = models.FloatField(blank=True, null=True)
    steel = models.FloatField(blank=True, null=True)
    magne = models.FloatField(blank=True, null=True)
    phos = models.FloatField(blank=True, null=True)
    calrium = models.FloatField(blank=True, null=True)
    natrium = models.FloatField(blank=True, null=True)
    copper = models.FloatField(blank=True, null=True)
    selenium = models.FloatField(blank=True, null=True)
    vita_d3 = models.FloatField(blank=True, null=True)
    dfe = models.FloatField(blank=True, null=True)
    vita_b12 = models.FloatField(blank=True, null=True)
    vita_c = models.FloatField(blank=True, null=True)
    threo = models.FloatField(blank=True, null=True)
    valine = models.FloatField(blank=True, null=True)
    histi = models.FloatField(blank=True, null=True)
    tyrosine = models.FloatField(blank=True, null=True)
    cysteine = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe_ingre'

class RecipeOrder(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    recipe_id = models.IntegerField(db_column='RECIPE_ID', blank=True, null=True)  # Field name made lowercase.
    cooking_no = models.IntegerField(db_column='COOKING_NO', blank=True, null=True)  # Field name made lowercase.
    cooking_dc = models.TextField(db_column='COOKING_DC', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recipe_order'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# 최적궁합_glv 모델
class BestCombiGlv(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    best_combination = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'best_combi_glv'

# 식품군별 상세분류 모델
class IngreGroup(models.Model):
    group = models.TextField(db_column='GROUP', blank=True, null=True)  # Field name made lowercase.
    sub_igrdt = models.TextField(db_column='SUB_IGRDT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ingre_group'

# 재료리스트 정리 모델
class IngreList(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    recipe_id = models.IntegerField(db_column='RECIPE_ID', blank=True, null=True)  # Field name made lowercase.
    subgroup = models.TextField(db_column='SUBGROUP', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ingre_list'

# 채식주의자종류 모델
class VegeType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    unnamed_0 = models.IntegerField(db_column='Unnamed: 0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    vege_kinds = models.TextField(db_column='VEGE_KINDS', blank=True, null=True)  # Field name made lowercase.
    vege_indbl = models.TextField(db_column='VEGE_INDBL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'vege_type'

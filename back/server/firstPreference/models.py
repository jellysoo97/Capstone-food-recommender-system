from django.db import models

class Preference(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False, blank=False)
    recipe_id = models.IntegerField(null=False, blank=False)
    ratings = models.FloatField(blank=False, null=True)

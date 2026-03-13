from django.db import models


class Marque(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "marque"
        managed = False


class Modele(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    marque = models.ForeignKey(
        Marque, on_delete=models.DO_NOTHING, db_column="marque_id"
    )

    class Meta:
        db_table = "modele"
        managed = False


class Ville(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "ville"
        managed = False


class Secteur(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.DO_NOTHING, db_column="ville_id")

    class Meta:
        db_table = "secteur"
        managed = False

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models








class ConsejeroEvento(models.Model):
    id_consejero = models.ForeignKey('Consejeros', models.DO_NOTHING, db_column='id_consejero', blank=True, null=True)
    numero_evento = models.ForeignKey('Evento', models.DO_NOTHING, db_column='numero_evento', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consejero_evento'


class Consejeros(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    facultad = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    image_path = models.CharField(max_length=100)
    suplente = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    def __str__(self):              # __unicode__ on Python 2
        return  '%s %s %s %s %s %s %s %s' %(self.id,self.nombre,self.nombre,self.facultad,self.cargo,self.image_path,self.suplente,self.fecha_inicio)

    class Meta:
        managed = False
        db_table = 'consejeros'


class Evento(models.Model):
    numero_evento = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'evento'


class Rfid(models.Model):
    id_rfid = models.CharField(db_column='id_RFID', primary_key=True, max_length=60)  # Field name made lowercase.
    id_consejero = models.ForeignKey(Consejeros, models.DO_NOTHING, db_column='id_consejero', blank=True, null=True)
    def __str__(self):
        return '%s %s' %(self.id_rfid,self.id_consejero)
    class Meta:
        managed = False
        db_table = 'rfid'

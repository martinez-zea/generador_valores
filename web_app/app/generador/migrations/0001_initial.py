# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Version'
        db.create_table('generador_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('en_uso', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('generador', ['Version'])

        # Adding model 'Unidad'
        db.create_table('generador_unidad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('signo', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('valor', self.gf('django.db.models.fields.FloatField')(blank=True)),
        ))
        db.send_create_signal('generador', ['Unidad'])

        # Adding model 'Configuracion'
        db.create_table('generador_configuracion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['generador.Version'])),
            ('fecha_inicio', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('valor_proyecto', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('valor_energia', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('valor_papel', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('valor_hora_trabajo', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('valor_simbolico', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('valor_tintas', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('porcentaje_devaluacion', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('porcentaje_valuacion', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('ventana_inactividad', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('generador', ['Configuracion'])

        # Adding M2M table for field unidad on 'Configuracion'
        db.create_table('generador_configuracion_unidad', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('configuracion', models.ForeignKey(orm['generador.configuracion'], null=False)),
            ('unidad', models.ForeignKey(orm['generador.unidad'], null=False))
        ))
        db.create_unique('generador_configuracion_unidad', ['configuracion_id', 'unidad_id'])

        # Adding model 'TituloValor'
        db.create_table('generador_titulovalor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identificador', self.gf('django.db.models.fields.IntegerField')()),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')()),
            ('certificado', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('fuente', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('generador', ['TituloValor'])

        # Adding model 'Estado'
        db.create_table('generador_estado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('num_titulos_emitidos', self.gf('django.db.models.fields.IntegerField')()),
            ('valor_unitario', self.gf('django.db.models.fields.FloatField')()),
            ('tiempo_actividad', self.gf('django.db.models.fields.IntegerField')()),
            ('capital', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('generador', ['Estado'])

    def backwards(self, orm):
        # Deleting model 'Version'
        db.delete_table('generador_version')

        # Deleting model 'Unidad'
        db.delete_table('generador_unidad')

        # Deleting model 'Configuracion'
        db.delete_table('generador_configuracion')

        # Removing M2M table for field unidad on 'Configuracion'
        db.delete_table('generador_configuracion_unidad')

        # Deleting model 'TituloValor'
        db.delete_table('generador_titulovalor')

        # Deleting model 'Estado'
        db.delete_table('generador_estado')

    models = {
        'generador.configuracion': {
            'Meta': {'object_name': 'Configuracion'},
            'fecha_inicio': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porcentaje_devaluacion': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'porcentaje_valuacion': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'unidad': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['generador.Unidad']", 'symmetrical': 'False', 'blank': 'True'}),
            'valor_energia': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'valor_hora_trabajo': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'valor_papel': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'valor_proyecto': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'valor_simbolico': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'valor_tintas': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ventana_inactividad': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generador.Version']"})
        },
        'generador.estado': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Estado'},
            'capital': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_titulos_emitidos': ('django.db.models.fields.IntegerField', [], {}),
            'tiempo_actividad': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'valor_unitario': ('django.db.models.fields.FloatField', [], {})
        },
        'generador.titulovalor': {
            'Meta': {'ordering': "['-fecha_creacion']", 'object_name': 'TituloValor'},
            'certificado': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {}),
            'fuente': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificador': ('django.db.models.fields.IntegerField', [], {}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'generador.unidad': {
            'Meta': {'object_name': 'Unidad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'signo': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'valor': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        },
        'generador.version': {
            'Meta': {'object_name': 'Version'},
            'en_uso': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['generador']
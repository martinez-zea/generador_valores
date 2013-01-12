# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Configuracion.porcentaje_valuacion'
        db.alter_column('generador_configuracion', 'porcentaje_valuacion', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Configuracion.porcentaje_devaluacion'
        db.alter_column('generador_configuracion', 'porcentaje_devaluacion', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Configuracion.fecha_inicio'
        db.alter_column('generador_configuracion', 'fecha_inicio', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Configuracion.valor_energia'
        db.alter_column('generador_configuracion', 'valor_energia', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Configuracion.valor_hora_trabajo'
        db.alter_column('generador_configuracion', 'valor_hora_trabajo', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Configuracion.valor_papel'
        db.alter_column('generador_configuracion', 'valor_papel', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Configuracion.ventana_inactividad'
        db.alter_column('generador_configuracion', 'ventana_inactividad', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Configuracion.valor_tintas'
        db.alter_column('generador_configuracion', 'valor_tintas', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Configuracion.valor_simbolico'
        db.alter_column('generador_configuracion', 'valor_simbolico', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Configuracion.valor_proyecto'
        db.alter_column('generador_configuracion', 'valor_proyecto', self.gf('django.db.models.fields.FloatField')(null=True))
    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Configuracion.porcentaje_valuacion'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.porcentaje_valuacion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.porcentaje_devaluacion'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.porcentaje_devaluacion' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.fecha_inicio'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.fecha_inicio' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.valor_energia'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.valor_energia' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.valor_hora_trabajo'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.valor_hora_trabajo' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.valor_papel'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.valor_papel' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.ventana_inactividad'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.ventana_inactividad' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.valor_tintas'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.valor_tintas' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.valor_simbolico'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.valor_simbolico' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.valor_proyecto'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.valor_proyecto' and its values cannot be restored.")
    models = {
        'generador.configuracion': {
            'Meta': {'object_name': 'Configuracion'},
            'fecha_inicio': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porcentaje_devaluacion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'porcentaje_valuacion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'unidad': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['generador.Unidad']", 'null': 'True', 'blank': 'True'}),
            'valor_energia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'valor_hora_trabajo': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'valor_papel': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'valor_proyecto': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'valor_simbolico': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'valor_tintas': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ventana_inactividad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
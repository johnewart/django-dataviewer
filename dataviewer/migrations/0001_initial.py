# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ViewField'
        db.create_table('dataviewer_viewfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('dataviewer', ['ViewField'])

        # Adding model 'ViewTable'
        db.create_table('dataviewer_viewtable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('dataviewer', ['ViewTable'])

        # Adding M2M table for field fields on 'ViewTable'
        db.create_table('dataviewer_viewtable_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('viewtable', models.ForeignKey(orm['dataviewer.viewtable'], null=False)),
            ('viewfield', models.ForeignKey(orm['dataviewer.viewfield'], null=False))
        ))
        db.create_unique('dataviewer_viewtable_fields', ['viewtable_id', 'viewfield_id'])

        # Adding M2M table for field embedded_tables on 'ViewTable'
        db.create_table('dataviewer_viewtable_embedded_tables', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_viewtable', models.ForeignKey(orm['dataviewer.viewtable'], null=False)),
            ('to_viewtable', models.ForeignKey(orm['dataviewer.viewtable'], null=False))
        ))
        db.create_unique('dataviewer_viewtable_embedded_tables', ['from_viewtable_id', 'to_viewtable_id'])

        # Adding model 'Page'
        db.create_table('dataviewer_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mtom_mappings', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dataviewer', ['Page'])

        # Adding M2M table for field groups on 'Page'
        db.create_table('dataviewer_page_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm['dataviewer.page'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('dataviewer_page_groups', ['page_id', 'group_id'])

        # Adding M2M table for field tables on 'Page'
        db.create_table('dataviewer_page_tables', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm['dataviewer.page'], null=False)),
            ('viewtable', models.ForeignKey(orm['dataviewer.viewtable'], null=False))
        ))
        db.create_unique('dataviewer_page_tables', ['page_id', 'viewtable_id'])


    def backwards(self, orm):
        
        # Deleting model 'ViewField'
        db.delete_table('dataviewer_viewfield')

        # Deleting model 'ViewTable'
        db.delete_table('dataviewer_viewtable')

        # Removing M2M table for field fields on 'ViewTable'
        db.delete_table('dataviewer_viewtable_fields')

        # Removing M2M table for field embedded_tables on 'ViewTable'
        db.delete_table('dataviewer_viewtable_embedded_tables')

        # Deleting model 'Page'
        db.delete_table('dataviewer_page')

        # Removing M2M table for field groups on 'Page'
        db.delete_table('dataviewer_page_groups')

        # Removing M2M table for field tables on 'Page'
        db.delete_table('dataviewer_page_tables')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dataviewer.page': {
            'Meta': {'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mtom_mappings': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tables': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dataviewer.ViewTable']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dataviewer.viewfield': {
            'Meta': {'object_name': 'ViewField'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dataviewer.viewtable': {
            'Meta': {'object_name': 'ViewTable'},
            'embedded_tables': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'embedded_tables_rel_+'", 'to': "orm['dataviewer.ViewTable']"}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dataviewer.ViewField']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['dataviewer']

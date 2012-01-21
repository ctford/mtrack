# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Product'
        db.create_table('logistics_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sms_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('product_code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('average_monthly_consumption', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('emergency_order_level', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.ProductType'])),
        ))
        db.send_create_signal('logistics', ['Product'])

        # Adding M2M table for field equivalents on 'Product'
        db.create_table('logistics_product_equivalents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm['logistics.product'], null=False)),
            ('to_product', models.ForeignKey(orm['logistics.product'], null=False))
        ))
        db.create_unique('logistics_product_equivalents', ['from_product_id', 'to_product_id'])

        # Adding model 'ProductType'
        db.create_table('logistics_producttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('logistics', ['ProductType'])

        # Adding model 'SupplyPointType'
        db.create_table('logistics_supplypointtype', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, primary_key=True, db_index=True)),
        ))
        db.send_create_signal('logistics', ['SupplyPointType'])

        # Adding model 'SupplyPoint'
        db.create_table('logistics_supplypoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPointType'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('last_reported', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
            ('supplied_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'], null=True, blank=True)),
        ))
        db.send_create_signal('logistics', ['SupplyPoint'])

        # Adding M2M table for field groups on 'SupplyPoint'
        db.create_table('logistics_supplypoint_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('supplypoint', models.ForeignKey(orm['logistics.supplypoint'], null=False)),
            ('supplypointgroup', models.ForeignKey(orm['logistics.supplypointgroup'], null=False))
        ))
        db.create_unique('logistics_supplypoint_groups', ['supplypoint_id', 'supplypointgroup_id'])

        # Adding model 'SupplyPointGroup'
        db.create_table('logistics_supplypointgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('logistics', ['SupplyPointGroup'])

        # Adding model 'LogisticsProfile'
        db.create_table('logistics_logisticsprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'], null=True, blank=True)),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'], null=True, blank=True)),
        ))
        db.send_create_signal('logistics', ['LogisticsProfile'])

        # Adding model 'ProductStock'
        db.create_table('logistics_productstock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.Product'])),
            ('days_stocked_out', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('manual_monthly_consumption', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, blank=True)),
            ('auto_monthly_consumption', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, blank=True)),
            ('use_auto_consumption', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('logistics', ['ProductStock'])

        # Adding unique constraint on 'ProductStock', fields ['supply_point', 'product']
        db.create_unique('logistics_productstock', ['supply_point_id', 'product_id'])

        # Adding model 'StockTransfer'
        db.create_table('logistics_stocktransfer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('giver', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='giver', null=True, to=orm['logistics.SupplyPoint'])),
            ('giver_unknown', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['logistics.SupplyPoint'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.Product'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('initiated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('logistics', ['StockTransfer'])

        # Adding model 'StockRequest'
        db.create_table('logistics_stockrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.Product'])),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('response_status', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('is_emergency', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('requested_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('responded_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('received_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('requested_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requested_by', null=True, to=orm['rapidsms.Contact'])),
            ('responded_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responded_by', null=True, to=orm['rapidsms.Contact'])),
            ('received_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='received_by', null=True, to=orm['rapidsms.Contact'])),
            ('balance', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('amount_requested', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('amount_approved', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('amount_received', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('canceled_for', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.StockRequest'], null=True)),
        ))
        db.send_create_signal('logistics', ['StockRequest'])

        # Adding model 'ProductReportType'
        db.create_table('logistics_productreporttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('logistics', ['ProductReportType'])

        # Adding model 'ProductReport'
        db.create_table('logistics_productreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.Product'])),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'])),
            ('report_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.ProductReportType'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('report_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow, db_index=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms_httprouter.Message'], null=True, blank=True)),
        ))
        db.send_create_signal('logistics', ['ProductReport'])

        # Adding model 'StockTransaction'
        db.create_table('logistics_stocktransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.Product'])),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('beginning_balance', self.gf('django.db.models.fields.IntegerField')()),
            ('ending_balance', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('product_report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.ProductReport'], null=True)),
        ))
        db.send_create_signal('logistics', ['StockTransaction'])

        # Adding model 'RequisitionReport'
        db.create_table('logistics_requisitionreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'])),
            ('submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('report_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms_httprouter.Message'])),
        ))
        db.send_create_signal('logistics', ['RequisitionReport'])

        # Adding model 'NagRecord'
        db.create_table('logistics_nagrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supply_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistics.SupplyPoint'])),
            ('report_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('warning', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('nag_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('logistics', ['NagRecord'])

        # Adding model 'Responsibility'
        db.create_table('logistics_responsibility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('logistics', ['Responsibility'])

        # Adding model 'ContactRole'
        db.create_table('logistics_contactrole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('logistics', ['ContactRole'])

        # Adding M2M table for field responsibilities on 'ContactRole'
        db.create_table('logistics_contactrole_responsibilities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contactrole', models.ForeignKey(orm['logistics.contactrole'], null=False)),
            ('responsibility', models.ForeignKey(orm['logistics.responsibility'], null=False))
        ))
        db.create_unique('logistics_contactrole_responsibilities', ['contactrole_id', 'responsibility_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ProductStock', fields ['supply_point', 'product']
        db.delete_unique('logistics_productstock', ['supply_point_id', 'product_id'])

        # Deleting model 'Product'
        db.delete_table('logistics_product')

        # Removing M2M table for field equivalents on 'Product'
        db.delete_table('logistics_product_equivalents')

        # Deleting model 'ProductType'
        db.delete_table('logistics_producttype')

        # Deleting model 'SupplyPointType'
        db.delete_table('logistics_supplypointtype')

        # Deleting model 'SupplyPoint'
        db.delete_table('logistics_supplypoint')

        # Removing M2M table for field groups on 'SupplyPoint'
        db.delete_table('logistics_supplypoint_groups')

        # Deleting model 'SupplyPointGroup'
        db.delete_table('logistics_supplypointgroup')

        # Deleting model 'LogisticsProfile'
        db.delete_table('logistics_logisticsprofile')

        # Deleting model 'ProductStock'
        db.delete_table('logistics_productstock')

        # Deleting model 'StockTransfer'
        db.delete_table('logistics_stocktransfer')

        # Deleting model 'StockRequest'
        db.delete_table('logistics_stockrequest')

        # Deleting model 'ProductReportType'
        db.delete_table('logistics_productreporttype')

        # Deleting model 'ProductReport'
        db.delete_table('logistics_productreport')

        # Deleting model 'StockTransaction'
        db.delete_table('logistics_stocktransaction')

        # Deleting model 'RequisitionReport'
        db.delete_table('logistics_requisitionreport')

        # Deleting model 'NagRecord'
        db.delete_table('logistics_nagrecord')

        # Deleting model 'Responsibility'
        db.delete_table('logistics_responsibility')

        # Deleting model 'ContactRole'
        db.delete_table('logistics_contactrole')

        # Removing M2M table for field responsibilities on 'ContactRole'
        db.delete_table('logistics_contactrole_responsibilities')


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
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Point']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': "orm['locations.LocationType']"})
        },
        'locations.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'locations.point': {
            'Meta': {'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'})
        },
        'logistics.contactrole': {
            'Meta': {'object_name': 'ContactRole'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'responsibilities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['logistics.Responsibility']", 'null': 'True', 'blank': 'True'})
        },
        'logistics.logisticsprofile': {
            'Meta': {'object_name': 'LogisticsProfile'},
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'logistics.nagrecord': {
            'Meta': {'object_name': 'NagRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nag_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'report_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']"}),
            'warning': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'logistics.product': {
            'Meta': {'object_name': 'Product'},
            'average_monthly_consumption': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'emergency_order_level': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'equivalents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'equivalents_rel_+'", 'null': 'True', 'to': "orm['logistics.Product']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'product_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sms_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ProductType']"}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'logistics.productreport': {
            'Meta': {'object_name': 'ProductReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_httprouter.Message']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'report_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow', 'db_index': 'True'}),
            'report_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ProductReportType']"}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']"})
        },
        'logistics.productreporttype': {
            'Meta': {'object_name': 'ProductReportType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'logistics.productstock': {
            'Meta': {'unique_together': "(('supply_point', 'product'),)", 'object_name': 'ProductStock'},
            'auto_monthly_consumption': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'days_stocked_out': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'manual_monthly_consumption': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']"}),
            'use_auto_consumption': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'logistics.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'logistics.requisitionreport': {
            'Meta': {'object_name': 'RequisitionReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms_httprouter.Message']"}),
            'report_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']"})
        },
        'logistics.responsibility': {
            'Meta': {'object_name': 'Responsibility'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'logistics.stockrequest': {
            'Meta': {'object_name': 'StockRequest'},
            'amount_approved': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'amount_received': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'amount_requested': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'balance': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'canceled_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.StockRequest']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_emergency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.Product']"}),
            'received_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'received_by'", 'null': 'True', 'to': "orm['rapidsms.Contact']"}),
            'received_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'requested_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requested_by'", 'null': 'True', 'to': "orm['rapidsms.Contact']"}),
            'requested_on': ('django.db.models.fields.DateTimeField', [], {}),
            'responded_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responded_by'", 'null': 'True', 'to': "orm['rapidsms.Contact']"}),
            'responded_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'response_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']"})
        },
        'logistics.stocktransaction': {
            'Meta': {'object_name': 'StockTransaction'},
            'beginning_balance': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'ending_balance': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.Product']"}),
            'product_report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ProductReport']", 'null': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']"})
        },
        'logistics.stocktransfer': {
            'Meta': {'object_name': 'StockTransfer'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'closed_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'giver'", 'null': 'True', 'to': "orm['logistics.SupplyPoint']"}),
            'giver_unknown': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.Product']"}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': "orm['logistics.SupplyPoint']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'logistics.supplypoint': {
            'Meta': {'object_name': 'SupplyPoint'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['logistics.SupplyPointGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_reported': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'supplied_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPointType']"})
        },
        'logistics.supplypointgroup': {
            'Meta': {'object_name': 'SupplyPointGroup'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'logistics.supplypointtype': {
            'Meta': {'object_name': 'SupplyPointType'},
            'code': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rapidsms.backend': {
            'Meta': {'object_name': 'Backend'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'rapidsms.connection': {
            'Meta': {'unique_together': "(('backend', 'identity'),)", 'object_name': 'Connection'},
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Backend']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'commodities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'reported_by'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['logistics.Product']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'needs_reminders': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.ContactRole']", 'null': 'True', 'blank': 'True'}),
            'supply_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logistics.SupplyPoint']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villagers'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'rapidsms_httprouter.message': {
            'Meta': {'object_name': 'Message'},
            'application': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'null': 'True', 'to': "orm['rapidsms_httprouter.MessageBatch']"}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['rapidsms.Connection']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_response_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'null': 'True', 'to': "orm['rapidsms_httprouter.Message']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'rapidsms_httprouter.messagebatch': {
            'Meta': {'object_name': 'MessageBatch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['logistics']

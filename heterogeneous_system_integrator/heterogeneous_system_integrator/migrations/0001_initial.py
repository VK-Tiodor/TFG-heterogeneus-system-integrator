# Generated by Django 4.2 on 2024-06-02 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0018_improve_crontab_helptext'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hostname', models.CharField(help_text='www.host_site.com or 192.168.0.1')),
                ('port', models.IntegerField(blank=True, help_text='5432', null=True)),
                ('username', models.CharField(blank=True, null=True)),
                ('password', models.CharField(blank=True, null=True)),
                ('auth_endpoint', models.CharField(blank=True, null=True)),
                ('auth_type', models.CharField(blank=True, choices=[('basic', 'Basic'), ('bearer', 'Bearer'), ('key', 'X-Api-Key')], help_text='Authentication method. Leave blank if no login is required to use the API', null=True)),
                ('username_field_name', models.CharField(blank=True, help_text='Field name of the username that goes in the login request. Leave blank if auth type is not Bearer', null=True)),
                ('password_field_name', models.CharField(blank=True, help_text='Field name of the password that goes in the login request. Leave blank if auth type is not Bearer', null=True)),
                ('access_token_field_name', models.CharField(blank=True, help_text='Field name of the access token that comes in the login response. Leave blank if auth type is not Bearer', null=True)),
                ('api_type', models.CharField(choices=[('soap', 'SOAP'), ('rest', 'REST')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AsyncTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseDataLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field_name', models.CharField(help_text='The field name which value is subject of comparison')),
                ('comparison_operator', models.CharField(choices=[('==', 'Equal'), ('>', 'Greater than'), ('>=', 'Greater than or equal to'), ('in', 'In'), ('<', 'Less than'), ('<=', 'Less than or equal to'), ('!=', 'Not equal'), ('nin', 'Not in')])),
                ('comparison_value', models.CharField(help_text='The value that is going to be compared with')),
                ('conversion_value', models.CharField(help_text='The new value that is going to receive the field when the conditions are met')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DbConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hostname', models.CharField(help_text='www.host_site.com or 192.168.0.1')),
                ('port', models.IntegerField(blank=True, help_text='5432', null=True)),
                ('username', models.CharField(blank=True, null=True)),
                ('password', models.CharField(blank=True, null=True)),
                ('db_type', models.CharField(choices=[('postgres', 'PostgreSQL'), ('mongo', 'MongoDB')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field_name', models.CharField(help_text='The field name which value is subject of comparison')),
                ('comparison_operator', models.CharField(choices=[('==', 'Equal'), ('>', 'Greater than'), ('>=', 'Greater than or equal to'), ('in', 'In'), ('<', 'Less than'), ('<=', 'Less than or equal to'), ('!=', 'Not equal'), ('nin', 'Not in')])),
                ('comparison_value', models.CharField(help_text='The value that is going to be compared with')),
                ('type', models.CharField(choices=[('keep', 'Keep'), ('discard', 'Discard')], help_text='Filter behaviour with data when conditions are met')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FtpConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hostname', models.CharField(help_text='www.host_site.com or 192.168.0.1')),
                ('port', models.IntegerField(blank=True, help_text='5432', null=True)),
                ('username', models.CharField(blank=True, null=True)),
                ('password', models.CharField(blank=True, null=True)),
                ('ftp_type', models.CharField(choices=[('basic', 'Basic'), ('ftps', 'FTPS'), ('ftpes', 'FTPES'), ('sftp', 'SFTP')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('origin_field_name', models.CharField(blank=True, help_text='Source field name from where to extract the value, in case of inner fields use dots (.) to route. Incompatible with "Constant value"', null=True)),
                ('constant_value', models.CharField(blank=True, help_text='Source constant value. Incompatible with "Origin field name"', null=True)),
                ('destination_field_name', models.CharField(help_text='Target field name where the value is going to be stored')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('minute', models.CharField(default='*', help_text='Possible values from 0 to 59. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')),
                ('hour', models.CharField(default='*', help_text='Possible values from 0 to 23. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')),
                ('day_of_week', models.CharField(default='*', help_text='Possible values from 1 to 7. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')),
                ('day_of_month', models.CharField(default='*', help_text='Possible values from 1 to 31. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')),
                ('month_of_year', models.CharField(default='*', help_text='Possible values from 1 to 12. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')),
                ('celery_crontab', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.crontabschedule')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransformStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('keep_leftover_fields', models.BooleanField(default=False, help_text='Behavior with the data fields that have not been mapped.')),
                ('conversions_after_mappings', models.BooleanField(default=False, help_text='Conversions change values over the specified field names. This process can be done on the original fields or the mapped fields.')),
                ('conversions', models.ManyToManyField(blank=True, help_text='Conversions to modify the field values that are going to be uploaded', null=True, related_name='transform_steps', to='heterogeneous_system_integrator.conversion')),
                ('mappings', models.ManyToManyField(help_text='Mappings to choose which data fields are going to be uploaded and from which origin', related_name='transform_steps', to='heterogeneous_system_integrator.mapping')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransferStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data_location', models.ForeignKey(help_text='Data location where the transfering data process is going to take place', on_delete=django.db.models.deletion.PROTECT, related_name='transfer_steps', to='heterogeneous_system_integrator.basedatalocation')),
                ('filters', models.ManyToManyField(blank=True, help_text='Filter to select the data that is going to be transfered', null=True, related_name='transfer_steps', to='heterogeneous_system_integrator.filter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('merge_field_name', models.CharField(blank=True, help_text='Field name by which to merge the data. Must be a unique identifier for the objects. Leave blank if there is only one download step.', null=True)),
                ('download_steps', models.ManyToManyField(help_text='Steps that download data', related_name='subtasks_download', to='heterogeneous_system_integrator.transferstep')),
                ('transform_step', models.ForeignKey(blank=True, help_text='Step that transforms data to the configured format', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subtasks', to='heterogeneous_system_integrator.transformstep')),
                ('upload_step', models.ForeignKey(help_text='Step that uploads data', on_delete=django.db.models.deletion.PROTECT, related_name='subtasks_upload', to='heterogeneous_system_integrator.transferstep')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlannedTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('execute_at', models.DateTimeField(help_text='Date and time when the task is going to be executed')),
                ('async_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_tasks', to='heterogeneous_system_integrator.asynctask')),
                ('celery_task', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PeriodicTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stop_at', models.DateTimeField(blank=True, help_text='From that point on the task is not going to be executed anymore and is goint to be deleted', null=True)),
                ('async_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_tasks', to='heterogeneous_system_integrator.asynctask')),
                ('celery_task', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask')),
                ('period', models.ForeignKey(help_text='Time pattern used for task execution', on_delete=django.db.models.deletion.PROTECT, related_name='periodic_tasks', to='heterogeneous_system_integrator.period')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='asynctask',
            name='subtasks',
            field=models.ManyToManyField(help_text='Subtasks that are going to be executed', related_name='tasks', to='heterogeneous_system_integrator.subtask'),
        ),
        migrations.CreateModel(
            name='FtpDataLocation',
            fields=[
                ('basedatalocation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='heterogeneous_system_integrator.basedatalocation')),
                ('directory_path', models.CharField(help_text='Path to the directory where the transfering file process is going to take place. Separate field names using slashes (/)')),
                ('filename', models.CharField(blank=True, help_text='Filename from where to get or where to save the data', null=True)),
                ('regex_pattern', models.CharField(blank=True, help_text='Regular expression to get data from multiple files', null=True)),
                ('connection', models.ForeignKey(help_text='Connection where the transfering data process is going to take place', on_delete=django.db.models.deletion.PROTECT, related_name='data_locations', to='heterogeneous_system_integrator.ftpconnection')),
            ],
            options={
                'abstract': False,
            },
            bases=('heterogeneous_system_integrator.basedatalocation',),
        ),
        migrations.CreateModel(
            name='DbDataLocation',
            fields=[
                ('basedatalocation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='heterogeneous_system_integrator.basedatalocation')),
                ('db_name', models.CharField(help_text='Database name')),
                ('schema', models.CharField(help_text='Schema name')),
                ('table', models.CharField(help_text='Table name')),
                ('connection', models.ForeignKey(help_text='Connection where the transfering data process is going to take place', on_delete=django.db.models.deletion.PROTECT, related_name='data_locations', to='heterogeneous_system_integrator.dbconnection')),
            ],
            options={
                'abstract': False,
            },
            bases=('heterogeneous_system_integrator.basedatalocation',),
        ),
        migrations.CreateModel(
            name='ApiDataLocation',
            fields=[
                ('basedatalocation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='heterogeneous_system_integrator.basedatalocation')),
                ('endpoint', models.CharField(help_text='API Endpoint where to apply the requests')),
                ('path_to_results_list', models.CharField(blank=True, help_text='Path to the results list inside the API response from where to get data. Separate field names using dots (.)', null=True)),
                ('connection', models.ForeignKey(help_text='Connection where the transfering data process is going to take place', on_delete=django.db.models.deletion.PROTECT, related_name='data_locations', to='heterogeneous_system_integrator.apiconnection')),
            ],
            options={
                'abstract': False,
            },
            bases=('heterogeneous_system_integrator.basedatalocation',),
        ),
    ]

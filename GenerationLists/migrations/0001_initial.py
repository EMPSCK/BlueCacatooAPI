# Generated by Django 4.1 on 2024-10-01 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('compid', models.AutoField(db_column='compId', primary_key=True, serialize=False)),
                ('compguid', models.CharField(db_column='compGuid', max_length=50, unique=True)),
                ('date1', models.DateField()),
                ('date2', models.DateField()),
                ('compname', models.CharField(db_column='compName', max_length=300)),
                ('city', models.CharField(max_length=300)),
                ('chairman_id', models.CharField(db_column='chairman_Id', max_length=20)),
                ('scrutineerid', models.CharField(db_column='scrutineerId', max_length=20)),
                ('lin_const', models.IntegerField()),
                ('isactive', models.IntegerField(db_column='isActive')),
                ('issecret', models.IntegerField(db_column='isSecret')),
            ],
            options={
                'db_table': 'competition',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CompetitionFilesCopy',
            fields=[
                ('fileid', models.AutoField(db_column='fileId', primary_key=True, serialize=False)),
                ('compid', models.IntegerField(db_column='compId')),
                ('groupid', models.IntegerField(db_column='groupId')),
                ('turid', models.IntegerField(db_column='turId')),
                ('danceid', models.IntegerField(db_column='danceId')),
                ('danceendid', models.IntegerField(blank=True, db_column='danceEndId', null=True)),
                ('groupname', models.CharField(blank=True, db_column='groupName', max_length=255, null=True)),
                ('turname', models.CharField(blank=True, db_column='turName', max_length=255, null=True)),
                ('filename', models.CharField(blank=True, db_collation='utf8_bin', db_column='fileName', max_length=255, null=True)),
                ('filetitle', models.CharField(blank=True, db_collation='utf8_bin', db_column='fileTitle', max_length=255, null=True)),
                ('loadurl', models.CharField(blank=True, db_column='loadUrl', max_length=255, null=True)),
                ('deleteurl', models.CharField(blank=True, db_column='deleteUrl', max_length=255, null=True)),
                ('thedate', models.DateTimeField(blank=True, db_column='theDate', null=True)),
            ],
            options={
                'db_table': 'competition_files_copy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CompetitionJudges',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('compid', models.IntegerField(db_column='compId')),
                ('lastname', models.CharField(db_collation='utf8mb4_bin', db_column='lastName', max_length=255)),
                ('firstname', models.CharField(db_collation='utf8mb4_bin', db_column='firstName', max_length=255)),
                ('lastname2', models.CharField(blank=True, db_collation='utf8mb4_bin', db_column='lastName2', max_length=50, null=True)),
                ('firstname2', models.CharField(blank=True, db_collation='utf8mb4_bin', db_column='firstName2', max_length=50, null=True)),
                ('secondname', models.CharField(blank=True, db_collation='utf8mb4_bin', db_column='SecondName', max_length=50, null=True)),
                ('birth', models.DateField(blank=True, db_column='Birth', null=True)),
                ('dsfarr_category', models.CharField(blank=True, db_collation='utf8mb4_bin', db_column='DSFARR_Category', max_length=50, null=True)),
                ('dsfarr_categorydate', models.CharField(blank=True, db_column='DSFARR_CategoryDate', max_length=50, null=True)),
                ('wdsf_categorydate', models.CharField(blank=True, db_column='WDSF_CategoryDate', max_length=50, null=True)),
                ('regionid', models.IntegerField(blank=True, db_column='RegionId', null=True)),
                ('city', models.CharField(blank=True, db_column='City', max_length=50, null=True)),
                ('club', models.CharField(blank=True, db_column='Club', max_length=50, null=True)),
                ('translit', models.CharField(blank=True, db_column='Translit', max_length=50, null=True)),
                ('sport_category', models.CharField(blank=True, db_column='SPORT_Category', max_length=50, null=True)),
                ('sport_categorydate', models.DateField(blank=True, db_column='SPORT_CategoryDate', null=True)),
                ('sport_categorydateconfirm', models.DateField(blank=True, db_column='SPORT_CategoryDateConfirm', null=True)),
                ('federation', models.CharField(blank=True, max_length=50, null=True)),
                ('archive', models.CharField(blank=True, db_column='Archive', max_length=50, null=True)),
                ('booknumber', models.IntegerField(blank=True, db_column='bookNumber', null=True)),
                ('notjudges', models.IntegerField(blank=True, db_column='notJudges', null=True)),
                ('is_use', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'competition_judges',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Judges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booknumber', models.CharField(blank=True, db_column='BookNumber', max_length=20, null=True)),
                ('lastname', models.CharField(blank=True, db_column='LastName', max_length=50, null=True)),
                ('firstname', models.CharField(blank=True, db_column='FirstName', max_length=50, null=True)),
                ('secondname', models.CharField(blank=True, db_column='SecondName', max_length=50, null=True)),
                ('birth', models.DateField(blank=True, db_column='Birth', null=True)),
                ('dsfarr_category', models.CharField(blank=True, db_column='DSFARR_Category', max_length=50, null=True)),
                ('dsfarr_categorydate', models.DateField(blank=True, db_column='DSFARR_CategoryDate', null=True)),
                ('wdsf_categorydate', models.DateField(blank=True, db_column='WDSF_CategoryDate', null=True)),
                ('regionid', models.IntegerField(blank=True, db_column='RegionId', null=True)),
                ('city', models.CharField(blank=True, db_column='City', max_length=50, null=True)),
                ('club', models.CharField(blank=True, db_column='Club', max_length=50, null=True)),
                ('translit', models.CharField(blank=True, db_column='Translit', max_length=50, null=True)),
                ('archive', models.CharField(blank=True, db_column='Archive', max_length=50, null=True)),
                ('sport_category', models.CharField(blank=True, db_column='SPORT_Category', max_length=50, null=True)),
                ('sport_categorydate', models.DateField(blank=True, db_column='SPORT_CategoryDate', null=True)),
                ('sport_categorydateconfirm', models.DateField(blank=True, db_column='SPORT_CategoryDateConfirm', null=True)),
                ('federation', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'judges',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.CharField(max_length=20)),
                ('id_active_comp', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField()),
                ('active', models.IntegerField()),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]

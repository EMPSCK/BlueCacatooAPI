# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Competition(models.Model):
    compid = models.AutoField(db_column='compId', primary_key=True)  # Field name made lowercase.
    compguid = models.CharField(db_column='compGuid', unique=True, max_length=50)  # Field name made lowercase.
    date1 = models.DateField()
    date2 = models.DateField()
    compname = models.CharField(db_column='compName', max_length=300)  # Field name made lowercase.
    city = models.CharField(max_length=300)
    chairman_id = models.CharField(db_column='chairman_Id', max_length=20)  # Field name made lowercase.
    scrutineerid = models.CharField(db_column='scrutineerId', max_length=20)  # Field name made lowercase.
    lin_const = models.IntegerField()
    isactive = models.IntegerField(db_column='isActive')  # Field name made lowercase.
    issecret = models.IntegerField(db_column='isSecret')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'competition'


class CompetitionFilesCopy(models.Model):
    fileid = models.AutoField(db_column='fileId', primary_key=True)  # Field name made lowercase.
    compid = models.IntegerField(db_column='compId')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupId')  # Field name made lowercase.
    turid = models.IntegerField(db_column='turId')  # Field name made lowercase.
    danceid = models.IntegerField(db_column='danceId')  # Field name made lowercase.
    danceendid = models.IntegerField(db_column='danceEndId', blank=True, null=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='groupName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    turname = models.CharField(db_column='turName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='fileName', max_length=255, db_collation='utf8_bin', blank=True, null=True)  # Field name made lowercase.
    filetitle = models.CharField(db_column='fileTitle', max_length=255, db_collation='utf8_bin', blank=True, null=True)  # Field name made lowercase.
    loadurl = models.CharField(db_column='loadUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deleteurl = models.CharField(db_column='deleteUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    thedate = models.DateTimeField(db_column='theDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'competition_files_copy'


class CompetitionJudges(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    compid = models.IntegerField(db_column='compId')  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255, db_collation='utf8mb4_bin')  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=255, db_collation='utf8mb4_bin')  # Field name made lowercase.
    lastname2 = models.CharField(db_column='lastName2', max_length=50, db_collation='utf8mb4_bin', blank=True, null=True)  # Field name made lowercase.
    firstname2 = models.CharField(db_column='firstName2', max_length=50, db_collation='utf8mb4_bin', blank=True, null=True)  # Field name made lowercase.
    secondname = models.CharField(db_column='SecondName', max_length=50, db_collation='utf8mb4_bin', blank=True, null=True)  # Field name made lowercase.
    birth = models.DateField(db_column='Birth', blank=True, null=True)  # Field name made lowercase.
    dsfarr_category = models.CharField(db_column='DSFARR_Category', max_length=50, db_collation='utf8mb4_bin', blank=True, null=True)  # Field name made lowercase.
    dsfarr_categorydate = models.CharField(db_column='DSFARR_CategoryDate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wdsf_categorydate = models.CharField(db_column='WDSF_CategoryDate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    regionid = models.IntegerField(db_column='RegionId', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    club = models.CharField(db_column='Club', max_length=50, blank=True, null=True)  # Field name made lowercase.
    translit = models.CharField(db_column='Translit', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sport_category = models.CharField(db_column='SPORT_Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sport_categorydate = models.DateField(db_column='SPORT_CategoryDate', blank=True, null=True)  # Field name made lowercase.
    sport_categorydateconfirm = models.DateField(db_column='SPORT_CategoryDateConfirm', blank=True, null=True)  # Field name made lowercase.
    federation = models.CharField(max_length=50, blank=True, null=True)
    archive = models.CharField(db_column='Archive', max_length=50, blank=True, null=True)  # Field name made lowercase.
    booknumber = models.IntegerField(db_column='bookNumber', blank=True, null=True)  # Field name made lowercase.
    notjudges = models.IntegerField(db_column='notJudges', blank=True, null=True)  # Field name made lowercase.
    is_use = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition_judges'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Judges(models.Model):
    booknumber = models.CharField(db_column='BookNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    secondname = models.CharField(db_column='SecondName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    birth = models.DateField(db_column='Birth', blank=True, null=True)  # Field name made lowercase.
    dsfarr_category = models.CharField(db_column='DSFARR_Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dsfarr_categorydate = models.DateField(db_column='DSFARR_CategoryDate', blank=True, null=True)  # Field name made lowercase.
    wdsf_categorydate = models.DateField(db_column='WDSF_CategoryDate', blank=True, null=True)  # Field name made lowercase.
    regionid = models.IntegerField(db_column='RegionId', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    club = models.CharField(db_column='Club', max_length=50, blank=True, null=True)  # Field name made lowercase.
    translit = models.CharField(db_column='Translit', max_length=50, blank=True, null=True)  # Field name made lowercase.
    archive = models.CharField(db_column='Archive', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sport_category = models.CharField(db_column='SPORT_Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sport_categorydate = models.DateField(db_column='SPORT_CategoryDate', blank=True, null=True)  # Field name made lowercase.
    sport_categorydateconfirm = models.DateField(db_column='SPORT_CategoryDateConfirm', blank=True, null=True)  # Field name made lowercase.
    federation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'judges'


class Users(models.Model):
    tg_id = models.CharField(max_length=20)
    id_active_comp = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'

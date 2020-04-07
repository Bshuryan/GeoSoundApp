# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class City(models.Model):
    city_id = models.IntegerField(db_column='CITY_ID', primary_key=True)  # Field name made lowercase.
    city_lat = models.FloatField(db_column='CITY_LAT')  # Field name made lowercase.
    city_long = models.FloatField(db_column='CITY_LONG')  # Field name made lowercase.
    city_zips = models.CharField(db_column='CITY_ZIPS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    city_name = models.CharField(db_column='CITY_NAME', max_length=45)  # Field name made lowercase.
    city_state = models.CharField(db_column='CITY_STATE', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CITY'


class Location(models.Model):
    loc_id = models.AutoField(db_column='LOC_ID', primary_key=True)  # Field name made lowercase.
    loc_street = models.CharField(db_column='LOC_STREET', max_length=45, blank=True, null=True)  # Field name made lowercase.
    loc_zip = models.CharField(db_column='LOC_ZIP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    loc_addr_num = models.CharField(db_column='LOC_ADDR_NUM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='CITY_ID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LOCATION'


class Playlist(models.Model):
    playlist_id = models.AutoField(db_column='PLAYLIST_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='USER_ID')  # Field name made lowercase.
    playlist_date_created = models.DateTimeField(db_column='PLAYLIST_DATE_CREATED')  # Field name made lowercase.
    playlist_date_modified = models.DateTimeField(db_column='PLAYLIST_DATE_MODIFIED')  # Field name made lowercase.
    playlist_name = models.CharField(db_column='PLAYLIST_NAME', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PLAYLIST'


class Song(models.Model):
    song_id = models.IntegerField(db_column='SONG_ID', primary_key=True)  # Field name made lowercase.
    song_name = models.CharField(db_column='SONG_NAME', max_length=150)  # Field name made lowercase.
    song_artist = models.CharField(db_column='SONG_ARTIST', max_length=60, blank=True, null=True)  # Field name made lowercase.
    song_duration = models.IntegerField(db_column='SONG_DURATION', blank=True, null=True)  # Field name made lowercase.
    song_genre = models.CharField(db_column='SONG_GENRE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    song_times_played = models.IntegerField(db_column='SONG_TIMES_PLAYED', blank=True, null=True)  # Field name made lowercase.
    song_year = models.IntegerField(db_column='SONG_YEAR', blank=True, null=True, validators=[MinValueValidator(1950), MaxValueValidator(2020)])  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SONG'


class SongInPlaylist(models.Model):
    sip_id = models.AutoField(db_column='SIP_ID', primary_key=True)  # Field name made lowercase.
    playlist = models.ForeignKey(Playlist, models.DO_NOTHING, db_column='PLAYLIST_ID')  # Field name made lowercase.
    song = models.ForeignKey(Song, models.DO_NOTHING, db_column='SONG_ID')  # Field name made lowercase.
    sip_date_added = models.DateTimeField(db_column='SIP_DATE_ADDED', blank=True, null=True)  # Field name made lowercase.
    sip_times_played = models.IntegerField(db_column='SIP_TIMES_PLAYED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SONG_IN_PLAYLIST'


class User(models.Model):
    user_id = models.AutoField(db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    user_password = models.CharField(db_column='USER_PASSWORD', max_length=45)  # Field name made lowercase.
    user_email = models.CharField(db_column='USER_EMAIL', unique=True, max_length=45)  # Field name made lowercase.
    loc = models.ForeignKey(Location, models.DO_NOTHING, db_column='LOC_ID')  # Field name made lowercase.
    user_fname = models.CharField(db_column='USER_FNAME', max_length=45)  # Field name made lowercase.
    user_lname = models.CharField(db_column='USER_LNAME', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'USER'


class UserPlayingSong(models.Model):
    play_id = models.AutoField(db_column='PLAY_ID', primary_key=True)  # Field name made lowercase.
    play_time = models.DateTimeField(db_column='PLAY_TIME', blank=True, null=True)  # Field name made lowercase.
    song = models.ForeignKey(Song, models.DO_NOTHING, db_column='SONG_ID')  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='USER_ID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'USER_PLAYING_SONG'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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

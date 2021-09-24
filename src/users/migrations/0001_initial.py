# Generated by Django 3.2.6 on 2021-09-22 15:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_hospital_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HospitalAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_admin', to='hospital.hospital')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_hospital_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('speciality', models.CharField(blank=True, max_length=255, null=True)),
                ('proficiency', models.CharField(blank=True, max_length=255, null=True)),
                ('experience', models.PositiveIntegerField(default=1)),
                ('photo', models.ImageField(upload_to='doctors/')),
                ('biography', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('education', models.TextField(blank=True, null=True)),
                ('courses', models.TextField(blank=True, null=True)),
                ('procedures', models.TextField(blank=True, null=True)),
                ('doctor_likes_amount', models.PositiveIntegerField(default=0)),
                ('visit_duration', models.PositiveIntegerField(blank=True, null=True)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('feedbacks_amount', models.PositiveIntegerField(default=0)),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='hospital.hospital')),
                ('specialization', models.ManyToManyField(blank=True, to='hospital.Specialization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_doctor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'.", regex='^\\+?1?\\d{9,15}$')])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=255)),
                ('age', models.PositiveIntegerField(default=18)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
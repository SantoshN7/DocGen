# Generated by Django 2.2.6 on 2019-10-08 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=255)),
                ('c_fee', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=255)),
                ('s_email', models.EmailField(max_length=254, unique=True)),
                ('s_mobile', models.BigIntegerField(unique=True)),
                ('s_eligibility', models.BigIntegerField(unique=True)),
                ('s_birth_date', models.DateTimeField()),
                ('s_gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Document_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genrated_time', models.DateTimeField(auto_now_add=True)),
                ('d_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DOC.Document')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DOC.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_status', models.CharField(choices=[('Pending', 'Pending'), ('Full Paid', 'Full Paid')], default='Full Paid', max_length=20)),
                ('course_status', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Ongoing', max_length=20)),
                ('roll_no', models.IntegerField(unique=True)),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DOC.Course')),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DOC.Student')),
            ],
        ),
    ]

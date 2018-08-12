# Generated by Django 2.1 on 2018-08-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20180811_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(choices=[('tvm', 'Thiruvananthapuram'), ('ptm', 'Pathanamthitta'), ('alp', 'Alappuzha'), ('ktm', 'Kottayam'), ('idk', 'Idukki'), ('mpm', 'Malappuram'), ('koz', 'Kozhikode'), ('wnd', 'Wayanad'), ('knr', 'Kannur'), ('ksr', 'Kasaragod'), ('pkd', 'Palakkad'), ('tcr', 'Thrissur'), ('ekm', 'Ernakulam'), ('kol', 'Kollam')], max_length=15)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('commodities', models.TextField(verbose_name='What you can contribute')),
            ],
        ),
    ]
# Generated by Django 3.1.5 on 2021-01-23 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('graphs', '0003_delete_trades'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date traded')),
                ('symbol', models.CharField(max_length=10)),
                ('volume', models.IntegerField(default=1)),
                ('pnl', models.FloatField()),
                ('tags', models.ManyToManyField(to='graphs.Tag')),
            ],
            options={
                'ordering': ['date', 'symbol'],
            },
        ),
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField()),
                ('amount', models.FloatField()),
                ('commission', models.FloatField()),
                ('fees', models.FloatField()),
                ('payment_type', models.CharField(max_length=20)),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphs.trade')),
            ],
        ),
    ]

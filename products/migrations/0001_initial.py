# Generated by Django 4.2 on 2024-08-31 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('category', models.CharField(choices=[('F', 'Fruit'), ('V', 'Vegetable'), ('M', 'Meat'), ('O', 'Other')], max_length=1)),
            ],
        ),
    ]

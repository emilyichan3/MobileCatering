# Generated by Django 4.2.16 on 2025-02-10 09:54

import cloudinary_storage.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caterer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caterer_name', models.CharField(max_length=60)),
                ('caterer_description', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=120)),
                ('activate', models.BooleanField(default=True)),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caterer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('product_description', models.CharField(max_length=200)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('unit_discount_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('available_from', models.DateField(default=django.utils.timezone.now)),
                ('available_to', models.DateField(default=django.utils.timezone.now)),
                ('sample_image', models.ImageField(null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='menu_pics')),
                ('caterer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='orders.caterer')),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('order_qualities', models.IntegerField()),
                ('unit_discount_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pick_up_at', models.DateField(default=django.utils.timezone.now)),
                ('comment', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=60)),
                ('order_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.menu')),
            ],
        ),
    ]

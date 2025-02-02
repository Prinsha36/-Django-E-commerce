# Generated by Django 5.1.1 on 2025-01-20 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0007_esewapayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Esewa', 'Esewa'), ('Khalti', 'Khalti')], default='Cash On Delivery', max_length=20)),
                ('payment_completed', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='EsewaPayment',
        ),
    ]

# Generated manually

from django.db import migrations, models
import accounts.models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.get_avatar_upload_path),
        ),
    ]

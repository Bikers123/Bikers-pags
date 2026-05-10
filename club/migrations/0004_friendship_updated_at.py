from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0003_profile_upload_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="friendship",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]


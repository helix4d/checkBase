from django.contrib.auth import get_user_model
from django.db import migrations


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin#184!"
ADMIN_EMAIL = "admin@example.com"


def create_admin_user(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
        )


def remove_admin_user(apps, schema_editor):
    User = get_user_model()
    User.objects.filter(username=ADMIN_USERNAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("evaluations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin_user, reverse_code=remove_admin_user),
    ]

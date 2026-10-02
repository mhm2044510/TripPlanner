from django.db import migrations


def seed_cities(apps, schema_editor):
    City = apps.get_model("trips", "City")

    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
        "Austin",
        "Jacksonville",
        "Fort Worth",
        "Columbus",
        "Indianapolis",
        "Charlotte",
        "Seattle",
        "Denver",
        "Washington",
        "Boston",
        "Nashville",
        "Baltimore",
        "Oklahoma City",
        "Portland",
        "Las Vegas",
        "Detroit",
        "Memphis",
        "Louisville",
        "Milwaukee",
        "Albuquerque",
    ]

    for city in cities:
        City.objects.get_or_create(name=city)


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0002_city"),
    ]

    operations = [
        migrations.RunPython(seed_cities),
    ]
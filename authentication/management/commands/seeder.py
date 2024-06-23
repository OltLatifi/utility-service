from django.core.management.base import BaseCommand, CommandError
from authentication.models import UsagePermission


class Command(BaseCommand):
    help = "Seeds the database with default information"
    permissions = [
        {
            "name": "Free version",
            "requests": 1,
        },
        {
            "name": "Payed",
            "requests": 3,
        },
        {
            "name": "Enterprise",
            "requests": 10,
        },
    ]

    def handle(self, *args, **options):
        for i in self.permissions:
            UsagePermission.objects.create(
                name=i["name"],
                requests_per_second=i["requests"],
            )
        self.stdout.write(
            self.style.SUCCESS("Usage permissions created succesfully")
        )

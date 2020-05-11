from django.core.management import BaseCommand

from ...models import DimDate, FactReview


class Command(BaseCommand):
    help = "Remove all the fact reviews"

    def handle(self, *args, **options):
        FactReview.objects.all().delete()
        DimDate.objects.all().delete()

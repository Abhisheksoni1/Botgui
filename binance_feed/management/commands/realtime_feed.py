from django.core.management import BaseCommand
from binance_feed import websocket_feed


class Command(BaseCommand):
    help = 'populate database from Twitter data'

    def handle(self, *args, **options):
        websocket_feed.main()
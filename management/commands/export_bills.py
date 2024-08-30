# adc/management/commands/export_bills.py
import pandas as pd
from django.core.management.base import BaseCommand
from adc.models import Bill, BillItem

class Command(BaseCommand):
    help = 'Extract data from Bill and BillItem models for Apriori analysis'

    def handle(self, *args, **kwargs):
        # Extract bills and their items
        bills = Bill.objects.all()
        transactions = []

        for bill in bills:
            items = BillItem.objects.filter(bill=bill)
            # Collect item names (products) for each transaction
            transaction = [item.article.name for item in items]
            transactions.append(transaction)

        # Convert transactions to DataFrame and save as CSV
        df = pd.DataFrame(transactions)
        df.to_csv('transactions.csv', index=False, header=False)
        self.stdout.write(self.style.SUCCESS('Successfully exported data to transactions.csv'))

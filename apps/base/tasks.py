from io import BytesIO
import io
from celery import shared_task
from ticket.admin import TicketResource, CheckInResource
from transactions.admin import TransactionResource
from storages.backends.sftpstorage import SFTPStorage
from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings

@shared_task
def export_all_data():
    if settings.DEBUG:
        print("Exporting data to SFTP server task")
    else:
        ticket_data = TicketResource().export()
        transaction_data = TransactionResource().export()
        check_in_data = CheckInResource().export()
        storage = SFTPStorage()

        # Define the remote file path on the SFTP server
        ticket_data_path = 'ticket_data.csv'
        transaction_data_path = 'transaction_data.csv'
        check_in_data_path = 'check_in_data.csv'

        # Save the CSV data to SFTP storage
        ticket_csv = ContentFile(ticket_data.csv)
        transaction_csv = ContentFile(transaction_data.csv)
        check_in_csv = ContentFile(check_in_data.csv)
        if ((storage.exists(ticket_data_path)) or (storage.exists(transaction_data_path)) or (storage.exists(check_in_data_path))):
            storage.delete(ticket_data_path)
            storage.delete(transaction_data_path)
            storage.delete(check_in_data_path)

        storage.save(ticket_data_path, ticket_csv)
        storage.save(transaction_data_path, transaction_csv)
        storage.save(check_in_data_path, check_in_csv)
    
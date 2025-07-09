import csv
from django.core.management.base import BaseCommand
from icd.models import ICDCode

class Command(BaseCommand):
    help = "Import ICD codes from a CSV file (run before import_diagnoses)"

    def handle(self, *args, **kwargs):
        file_path = "/app/icd_files/icd10_codes.csv"
        
        with open(file_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                code = row['icd_code']
                diagnose_name = row['diagnose_name']
                description = row['description']
                
                # Combine diagnose_name and description for the description field
                full_description = f"{diagnose_name}: {description}"
                
                # Create or update the ICDCode entry
                ICDCode.objects.update_or_create(
                    code=code,
                    defaults={
                        'description': full_description
                    }
                )
        
        self.stdout.write(self.style.SUCCESS("ICD codes imported successfully!"))
        self.stdout.write(
            self.style.WARNING("Next step: Run 'python manage.py import_diagnoses' to import diagnoses with foreign keys.")
        )
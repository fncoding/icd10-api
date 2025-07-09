import csv
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from diagnosen.models import Diagnosis
from icd.models import ICDCode

class Command(BaseCommand):
    help = "Import diagnoses from a CSV file and link them to existing ICD codes"

    def handle(self, *args, **kwargs):
        file_path = "/app/icd_files/icd10_codes.csv"
        
        created_count = 0
        updated_count = 0
        error_count = 0
        
        with open(file_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                code = row['icd_code']
                diagnose_name = row['diagnose_name']
                
                try:
                    # Find the corresponding ICD code
                    icd_code = ICDCode.objects.get(code=code)
                    
                    # Create or update the Diagnosis entry
                    diagnosis, created = Diagnosis.objects.update_or_create(
                        title=diagnose_name,
                        icd_code=icd_code,
                        defaults={}
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"ICD code {code} not found in database. Skipping diagnosis: {diagnose_name}")
                    )
                    error_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error processing {code}: {str(e)}")
                    )
                    error_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Diagnoses import completed!\n"
                f"Created: {created_count}\n"
                f"Updated: {updated_count}\n"
                f"Errors: {error_count}"
            )
        )

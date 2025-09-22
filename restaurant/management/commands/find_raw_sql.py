import os
import re
from django.core.management.base import BaseCommand

RAW_RE = re.compile(r'\.(raw|extra)\s*\(', re.I)

class Command(BaseCommand):
    help = "Scan project for remaining raw/extra SQL calls."

    def handle(self, *args, **options):
        root = os.getcwd()
        matches = 0
        for folder, _, files in os.walk(root):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(folder, file)
                    with open(path, encoding='utf-8') as f:
                        for n, line in enumerate(f, 1):
                            if RAW_RE.search(line):
                                self.stdout.write(
                                    self.style.WARNING(f"{path}:{n}  ->  {line.strip()}")
                                )
                                matches += 1
        if matches:
            self.stdout.write(self.style.ERROR(f"\nFound {matches} raw SQL calls – refactor to ORM."))
        else:
            self.stdout.write(self.style.SUCCESS("No raw SQL found – you are clean!"))
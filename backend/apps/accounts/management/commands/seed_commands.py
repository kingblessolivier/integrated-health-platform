"""
Seed the `commands` catalogue (docs/03). Idempotent. Run after applying the schema:

    python manage.py seed_commands

For the MVP Clinical Slice we seed the commands those endpoints bind to; extend with the
full ~115-code catalogue as later phases land.
"""
from django.core.management.base import BaseCommand

# (code, description) — domain/action are derived from the code.
MVP_COMMANDS = [
    ("PTRG", "Register patient (NIDA auto-fill)"),
    ("PTSR", "Search patient"),
    ("PTVW", "View longitudinal record"),
    ("ENNW", "Open / new encounter"),
    ("ENHX", "Review history / timeline"),
    ("ENDX", "Diagnosis (ICD-10/11)"),
    ("ENCL", "Close encounter"),
    ("RXNW", "Prescribe (digital sign)"),
    ("RXVF", "Verify prescription (pharmacist)"),
    ("RXDP", "Dispense (FEFO + barcode)"),
    ("ANVW", "Role-scoped dashboard view"),
]


class Command(BaseCommand):
    help = "Seed the command catalogue (idempotent)."

    def handle(self, *args, **options):
        from apps.accounts.models import Command as CommandRow

        created = 0
        for code, description in MVP_COMMANDS:
            _, made = CommandRow.objects.get_or_create(
                code=code,
                defaults={"domain": code[:2], "action": code[2:], "description": description},
            )
            created += int(made)
        self.stdout.write(self.style.SUCCESS(f"Seeded commands ({created} new, {len(MVP_COMMANDS)} total)."))

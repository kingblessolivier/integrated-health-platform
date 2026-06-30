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
    ("PHPS", "Point-of-sale sale"),
    ("PHSP", "Insurer / patient split"),
    ("PHMM", "Mobile-money request-to-pay"),
    ("PHEB", "RRA EBM certified receipt"),
    ("CHHH", "Household visit list"),
    ("CHIC", "iCCM assessment (sick child)"),
    ("CHRD", "RDT result + auto dose calc"),
    ("RFNW", "Create referral (6-digit tracking code)"),
    ("RFRC", "Receive referral by code"),
    ("RFTR", "Track referral status"),
    ("EMSO", "Patient SOS (one-tap, GPS)"),
    ("EMIN", "Intake request (912 / SOS / transfer)"),
    ("EMDS", "Dispatch nearest unit (PostGIS)"),
    ("EMHO", "Handover to ED"),
    ("CLEL", "Eligibility check"),
    ("CLSB", "Submit claim / batch"),
    ("CLSC", "AI scrubbing queue"),
    ("CLRV", "Review dispute"),
    ("CLST", "Settlement status"),
    ("SVMP", "Disease cluster map (real-time)"),
    ("SVAL", "Outbreak alert / threshold"),
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

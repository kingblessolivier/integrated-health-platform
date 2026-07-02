"""
Bootstrap a login: create a Django auth user linked to a `staff` row + command bundle, so
`FourAxisTokenSerializer` can issue a JWT carrying the four-axis scope (closes the gap noted
in docs/65). For local/API testing — grants the full seeded command set.

Prereqs: the domain schema is applied (backend/sql/0001_initial.sql) AND auth tables exist
(`python manage.py migrate`). Then:

    python manage.py seed_commands
    python manage.py bootstrap_user --nida 1199900000000001

A random password is generated and printed unless --password is given (no secrets in code).
"""
import secrets

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection

from apps.accounts.models import Command as CommandModel
from apps.accounts.models import Staff, UserCommand


class Command(BaseCommand):
    help = "Create an auth user linked to a staff row + command bundle (local/API testing)."

    def add_arguments(self, parser):
        parser.add_argument("--nida", required=True,
                            help="National ID — used as the username and staff.nida_id")
        parser.add_argument("--tenant", help="Existing tenant UUID (a demo tenant is created if omitted)")
        parser.add_argument("--password", help="Password (a random one is generated + printed if omitted)")
        parser.add_argument("--name", default="Test User")

    def handle(self, *args, **opts):
        user_model = get_user_model()
        nida = opts["nida"]
        password = opts.get("password") or secrets.token_urlsafe(12)

        tenant_id = opts.get("tenant")
        with connection.cursor() as cur:
            if not tenant_id:
                cur.execute("INSERT INTO tenants(name, kind) VALUES ('Demo Tenant','facility') "
                            "RETURNING id")
                tenant_id = cur.fetchone()[0]
            # RLS is FORCEd, so set the tenant GUC before touching tenant-scoped tables.
            cur.execute("SELECT set_config('app.tenant_id', %s, false)", [str(tenant_id)])

        staff, _ = Staff.objects.get_or_create(
            nida_id=nida, defaults={"tenant_id": tenant_id, "full_name": opts["name"]})

        granted = 0
        for code in CommandModel.objects.values_list("code", flat=True):
            _, made = UserCommand.objects.get_or_create(staff_id=staff.id, command_id=code)
            granted += int(made)

        # Least privilege (docs/08): a normal login, not a Django superuser. Access is granted
        # entirely by the command bundle above.
        user, _ = user_model.objects.get_or_create(username=nida)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f"User '{nida}' ready — staff {staff.id}, tenant {tenant_id}, "
            f"{granted} commands granted.\nPassword: {password}"))

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from checklist.models import Branch


class Command(BaseCommand):
    help = "Create/update branch users and set branch PINs"

    def handle(self, *args, **options):
        BRANCH_PASSWORDS = {
            "sairam": "4821",
            "fontan": "7394",
            "technomart": "6158",
            "alay": "2947",
            "minor": "8603",
            "gorkiy": "1749",
            "parkent": "5532",
            "aviators": "9086",
            "risoviy": "4215",
            "sergeli_east": "6674",
            "druzhba": "3128",
            "royson": "8459",
            "beruniy": "5093",
            "medik_city": "7781",
            "next": "2460",
            "grand_mir": "9347",
            "muqimiy": "6812",
            "parus": "1576",
            "atlas": "8924",
            "chimghan": "3648",
            "yangiyul": "7209",
            "golden_live": "9951",
        }

        for username, pin in BRANCH_PASSWORDS.items():
            user, user_created = User.objects.get_or_create(username=username)
            if user_created:
                user.set_password("temp1234")  # texnik vaqtinchalik
                user.save()

            branch, branch_created = Branch.objects.update_or_create(
                user=user,
                defaults={"name": username.title()}
            )

            branch.set_pin(pin)
            branch.save()

            self.stdout.write(
                f"{'CREATED' if user_created else 'OK'} USER | "
                f"{'CREATED' if branch_created else 'UPDATED'} BRANCH | "
                f"{username} | PIN SET"
            )

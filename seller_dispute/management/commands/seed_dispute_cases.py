import random
from django.core.management.base import BaseCommand
from faker import Faker
from seller_dispute.models import DisputeCase, DisputeCaseUpdate, Return

fake = Faker()

# Define the possible status progressions
STATUS_SEQUENCES = {
    'open': ['open'],
    'in_review': ['open', 'in_review'],
    'resolved': ['open', 'in_review', 'resolved'],
    'rejected': ['open', 'in_review', 'rejected'],
}

class Command(BaseCommand):
    help = "Seed 15 random dispute cases with full update sequences and unique returns."

    def handle(self, *args, **kwargs):
        statuses = ['open', 'in_review', 'resolved', 'rejected']
        available_returns = list(Return.objects.filter(dispute_case__isnull=True))
        if len(available_returns) < 15:
            self.stdout.write(self.style.ERROR("Not enough available returns to assign 15 unique dispute cases!"))
            return
        selected_returns = random.sample(available_returns, 15)
        for idx, return_event in enumerate(selected_returns, 1):
            final_status = random.choice(statuses)
            case_number = f"CASE-{fake.unique.bothify(text='????-####').upper()}"
            dispute_case = DisputeCase.objects.create(
                case_number=case_number,
                reason=fake.sentence(nb_words=6),
                description=fake.paragraph(nb_sentences=2),
                status=final_status,
                return_event=return_event,
                resolution_notes=fake.sentence(nb_words=8),
                disputed_amount=round(random.uniform(1, float(return_event.return_amount or 1)), 2)
            )
            # Add the full sequence of updates
            for status in STATUS_SEQUENCES[final_status]:
                DisputeCaseUpdate.objects.create(
                    dispute_case=dispute_case,
                    status=status,
                    comment=f"Status set to {status.title()}"
                )
            self.stdout.write(self.style.SUCCESS(f"Created DisputeCase {case_number} with status {final_status} for Return {return_event.return_id} (updates: {STATUS_SEQUENCES[final_status]})"))
        self.stdout.write(self.style.SUCCESS("Successfully seeded 15 dispute cases with full update sequences!")) 
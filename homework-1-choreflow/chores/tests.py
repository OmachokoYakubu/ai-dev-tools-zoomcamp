from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Housemate, Chore, ChoreLog

class ChoreFlowModelTests(TestCase):
    def setUp(self):
        self.alice = Housemate.objects.create(name="Alice Smith", email="alice@example.com")
        self.bob = Housemate.objects.create(name="Bob Jones", email="bob@example.com")

    def test_create_chore(self):
        chore = Chore.objects.create(
            title="Clean Microwave",
            recurrence=Chore.Recurrence.WEEKLY,
            assigned_to=self.alice,
            due_date=timezone.now().date()
        )
        self.assertEqual(str(chore), "Clean Microwave (PENDING)")
        self.assertEqual(chore.assigned_to.name, "Alice Smith")
        self.assertEqual(chore.status, Chore.Status.PENDING)

    def test_chore_log_creation(self):
        chore = Chore.objects.create(title="Vacuum Living Room", assigned_to=self.bob)
        log = ChoreLog.objects.create(chore=chore, completed_by=self.bob, notes="Done thoroughly")
        self.assertEqual(log.chore, chore)
        self.assertEqual(log.completed_by, self.bob)
        self.assertIn("Vacuum Living Room completed by Bob Jones", str(log))

class ChoreFlowViewTests(TestCase):
    def setUp(self):
        self.alice = Housemate.objects.create(name="Alice", email="alice@example.com")
        self.chore = Chore.objects.create(
            title="Take out Trash",
            assigned_to=self.alice,
            due_date=timezone.now().date()
        )

    def test_chore_list_view(self):
        response = self.client.get(reverse('chore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ChoreFlow")
        self.assertContains(response, "Take out Trash")

    def test_add_chore_post(self):
        response = self.client.post(reverse('add_chore'), {
            'title': 'Wipe Countertops',
            'assigned_to': self.alice.id,
            'recurrence': Chore.Recurrence.DAILY,
            'due_date': '2026-09-12'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Chore.objects.filter(title='Wipe Countertops').exists())

    def test_toggle_chore_status(self):
        self.assertEqual(self.chore.status, Chore.Status.PENDING)
        response = self.client.post(reverse('toggle_chore_status', args=[self.chore.id]))
        self.assertEqual(response.status_code, 302)
        
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, Chore.Status.DONE)
        self.assertTrue(ChoreLog.objects.filter(chore=self.chore).exists())

    def test_add_housemate_post(self):
        response = self.client.post(reverse('add_housemate'), {
            'name': 'Charlie',
            'email': 'charlie@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Housemate.objects.filter(email='charlie@example.com').exists())

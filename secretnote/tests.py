from django.test import TestCase, Client
from secretnote.models import Note
from datetime import datetime
from django.urls import reverse
import json
from django.utils import timezone
import uuid
from datetime import datetime, timedelta



# Create your tests here.
class NoteModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('note')  # URL for creating a note
    def test_createNote(self):
        """
        The Note create
        returns a 200
        """
        note = Note.objects.create(note_text = "Test Note", note_remvisit = 5, expiry_date =  (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
        response = self.client.post(self.create_url, data={
            'text': 'Test Note',
            'maxVisit': 5,
            'expireDate': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 2)
        note = Note.objects.first()
        self.assertEqual(note.note_text, 'Test Note')
        self.assertEqual(note.note_remvisit, 5)

    def test_createNoteMissingFields(self):
        """
        The Note create with missing fields
        returns array msg filled with problems
        """
        response = self.client.post(self.create_url, data={
            'text': 'Test Note'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('no maximum number of visits provieded', response.context['msg'])
        self.assertIn('no expire date provided', response.context['msg'])

    def test_retrieveNote(self):
        """
        The Note retrieve
        returns a 200
        """
        note = Note.objects.create(
            note_text='Test Note',
            note_remvisit=5,
            expiry_date=datetime.now() + timedelta(days=1)
        )
        retrieve_url = reverse('noteview', args=[str(note.note_url)])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['note'].note_text, 'Test Note')
        self.assertEqual(response.context['note'].note_remvisit, 4)

    def test_retrieveInvalidNote(self):
        """
        retrieve note with invalid id
        returns a 200
        """
        retrieve_url = reverse('noteview', args=[str(uuid.uuid4())])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, 404)

import unittest
from app import create_app, db
from app.models import Note
from datetime import datetime

class NoteTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a new database
        db.create_all()

        # Create a new note
        self.note = Note()
        self.note.CustomerId = 1
        self.note.UserId = 1
        self.note.Note = 'Test Note'
        self.note.DateCreated = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

        # Add the note to the database
        db.session.add(self.note)
        db.session.commit()

        # Get database Note
        self.dbNote = Note.query.filter_by(Note='Test Note').first()

    def tearDown(self):
        # Remove the note from the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_note_exists(self):
        self.assertTrue(self.dbNote is not None)

    def test_note_customerid(self):
        self.assertEqual(self.dbNote.CustomerId, 1)

    def test_note_userid(self):
        self.assertEqual(self.dbNote.UserId, 1)

    def test_note_note(self):
        self.assertEqual(self.dbNote.Note, 'Test Note')

    def test_note_datecreated(self):
        self.assertEqual(self.dbNote.DateCreated, datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
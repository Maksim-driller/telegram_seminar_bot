import json
from datetime import datetime
class Notes:
    def __init__(self, id, title, content, timestamp):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp
class NoteManager:
    def __init__(self, filename = 'notes.json'):
        self.filename = filename
        self.notes = []
    def create_new_note(self, id, title, content):
        id = len(self.notes) + 1
        note = Notes(id,title,content)
    def get_all_notes(self):
        return self.notes
    def get_note(self):
        for note in self.notes:
            if note.id == id:
                return note
        return None
    def update_note(self, id, title, content,timestamp):
        note = self.get_note(id)
        if note:
            note.title = title
            note.content = content
            note.timestamp = datetime().strftime("%d-%m-%Y %H:%M:%S")
    def delete_note(self,id):
        note = self.get_note(id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            return 1
        return 0
    def save_notes(self):
        with open(self.filename, "w") as f:
            json.dump([note.to_dict() for note in self.notes], f, indent=2)
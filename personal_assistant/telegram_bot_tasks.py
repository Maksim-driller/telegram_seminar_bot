
from datetime import datetime
class Tasks:
    def __init__(self, id, title, description, done, priority, due_date):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date


class TaskManager:
    def __init__(self):
        self.tasks = []
    def create_new_task(self, id, title, description):
        id = len(self.tasks) + 1
        task = Tasks(id,title,description)
    def get_all_tasks(self):
        return self.tasks
    def get_task(self):
        for task in self.tasks:
            if task.id == id:
                return task
        return 0
    def update_task(self,id,title,description):
        task = self.get_task(id)
        if task:
            task.title = title
            task.description = description
            


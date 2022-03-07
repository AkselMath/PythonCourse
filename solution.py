import os
import tempfile
import random


class File():
    def __init__(self, file_name):
        self.file_name = file_name
        self.start = 0
        if not os.path.exists(self.file_name):
            self.write('')

        self.file_line = self.preservation()

    def __str__(self):
        return os.path.abspath(self.file_name)

    def __add__(self, obj):
        self.storage_path = os.path.join(tempfile.gettempdir(), str(random.randint(0,10)))
        new_file_obj = File(self.storage_path)
        new_file_obj.write(self.read() + obj.read())
        return new_file_obj

    def __iter__(self):
        return self

    def __next__(self):
        if self.start >= len(self.file_line):
            self.start = 0
            raise StopIteration
        else:
            self.start += 1
            return self.file_line[self.start-1]

    def preservation(self):
        with open(self.file_name, 'r') as f:
            return f.readlines()

    def write(self, text):
        with open(self.file_name, 'w') as f:
            f.write(text)

        self.file_line = self.preservation()

    def read(self):
        with open(self.file_name, 'r') as f:
            return f.read()
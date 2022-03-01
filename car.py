from functools import reduce
import os
import csv


class CarBase:
    required = []

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = self.validate_input(brand)
        self.photo_file_name = self.validate_photo_filename(photo_file_name)
        self.carrying = float(self.validate_input(carrying))
        self.car_type = None

    def validate_input(self, value):
        if value == '':
            raise ValueError
        return value

    def validate_photo_filename(self, filename):
        for ext in ('.jpg', '.jpeg', '.png', '.gif'):
            if filename.endswith(ext) and len(filename) > len(ext):
                return filename
        raise ValueError

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

    @classmethod
    def create_from_dict(cls, data):
        parameters = [data[parameter] for parameter in cls.required]
        return cls(*parameters)


class Car(CarBase):
    required = ['brand', 'photo_file_name', 'carrying', 'passenger_seats_count']

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(self.validate_input(passenger_seats_count))
        self.car_type = 'car'


class Truck(CarBase):
    required = ['brand', 'photo_file_name', 'carrying', 'body_whl']

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        try:
            self._b = [float(c) for c in body_whl.split("x", 2)]
        except Exception:
            self._b = [0. for i in range(3)]

        self._b = list(self._b)

        self.body_length = self._b[0]
        self.body_width = self._b[1]
        self.body_height = self._b[2]

    def get_body_volume(self):
        return reduce(lambda x, y: x*y, self._b)


class SpecMachine(CarBase):
    required = ['brand', 'photo_file_name', 'carrying', 'extra']

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = self.validate_input(extra)
        self.car_type = 'spec_machine'


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def get_car_list(csv_filename):

    car_types = {'car': Car, 'spec_machine': SpecMachine, 'truck': Truck}
    csv.register_dialect('cars', delimiter=';')
    car_list = []

    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file, dialect='cars')
        for row in reader:
            try:
                car_class = car_types[row['car_type']]
                car_list.append(car_class.create_from_dict(row))
            except Exception:
                pass

    return car_list
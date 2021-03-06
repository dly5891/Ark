import datetime
import pdb
from django.test import TestCase
from ..services import (RoomService,
                        AnimalService)
from ..models import (Animal,
                      AnimalToRoom)


class AnimalServiceTest(TestCase):
    def setUp(self):
        self.animal_service = AnimalService()
        self.animal_service.create_animal(
            name='Cookie',
            birth_date=datetime.date(2014, 1, 1),
            is_female=True,
            joined=datetime.date(2015, 8, 21),
            personal_history='Stray',
            preferences_cats='Absolutely!',
            preferences_dogs='It\'s a possibility!',
            preferences_kids='It\'s a possibility!',
            declawed=False,
            spay_neuter=True,
            health='Good, FELV+',
            pet_id='4356')

        self.animal_service.create_animal(
            name='Luca',
            birth_date=datetime.date(
                2010, 4, 20),
            is_female=True,
            joined=datetime.date(2015, 8, 21),
            personal_history='Stray',
            preferences_cats='No, Thank you',
            preferences_dogs='It\'s a possibility!',
            preferences_kids='It\'s a possibility!',
            declawed=False,
            spay_neuter=True,
            health='Good, FELV+',
            pet_id='0416')

        self.room_service = RoomService()
        self.room_service.create_room('Adult Cat Room')

    def test_get_all_animals(self):
        """ Test to retrieve ALL animals in the db.
        """
        actual = self.animal_service.get_all_animals()
        expected = f'''
            4356: Cookie, Cat
        '''
        self.assertEqual(str(actual[0]), expected)

    def test_get_animal(self):
        """ Test to retrieve a specific animal based on pk.
        """
        animal_pk = Animal.objects.get(name='Luca').pk
        actual = self.animal_service.get_animal(animal_pk)
        expected = f'''
            0416: Luca, Cat
        '''
        self.assertEqual(str(actual), expected)

    def test_assign_animal_to(self):
        """ Test to assign an animal to a specific room.
        """
        room = self.room_service.get_room(name='Adult Cat Room')
        self.animal_service.assign_animal_to_room(
            pet_pk=Animal.objects.get(
                pet_id='0416').pk, room_pk=room.pk)

        animals_in_rooms = AnimalToRoom.objects.all()
        self.assertGreater(len(animals_in_rooms), 0)

    def test_get_animal_from_room(self):
        """ Test to retrieve an animal from a room.
        """
        animal = Animal.objects.get(pet_id='0416')
        room = self.room_service.get_room(name='Adult Cat Room')
        self.animal_service.assign_animal_to_room(animal.pk, room.pk)

        actual = self.animal_service.get_animal_from_room(
            pet_pk=Animal.objects.get(
                pet_id='0416').pk, room_name='Adult Cat Room')
        expected = f'''
            0416: Luca, Cat
        '''
        self.assertEqual(str(actual), expected)

        actual = self.animal_service.get_animal_from_room(
            pet_pk=animal.pk, room_pk=4)
        self.assertEqual(str(actual), expected)

        actual = self.animal_service.get_animal_from_room(pet_pk=animal.pk)
        self.assertEqual(str(actual), expected)

    def test_get_animals_from_room(self):
        """ Test to get all animals from a specific room.
        """
        room = self.room_service.get_room(name='Adult Cat Room')
        animals = Animal.objects.all()
        for animal in animals:
            self.animal_service.assign_animal_to_room(animal.pk, room.pk)

        actual = self.animal_service.get_animals_from_room(room.pk)
        self.assertGreater(len(actual), 0)

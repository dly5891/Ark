from django.core import serializers
from django.test import TestCase, Client
from ..models import (Animal,
                      AnimalToRoom,
                      Room)
from rest_framework import status
from django.urls import reverse
from ..serializers import AnimalSerializer
from ..services import (AnimalService,
                        RoomService)
import datetime
import json
import pdb


class AnimalTests(TestCase):
    client = Client()

    def setUp(self):
        self.animal_service = AnimalService()
        self.room_service = RoomService()
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
            spay_neuter=False,
            health='Good, FELV+',
            pet_id='4356',
        )

        self.animal_service.create_animal(
            name='Georgie',
            birth_date=datetime.date(2014, 1, 1),
            is_female=False,
            joined=datetime.date(2015, 8, 21),
            personal_history='Stray',
            preferences_cats='Absolutely!',
            preferences_dogs='It\'s a possibility!',
            preferences_kids='It\'s a possibility!',
            declawed=False,
            spay_neuter=False,
            health='Good, FELV+',
            pet_id='4357',
        )

        self.animal_service.create_animal(
            name='Ben',
            birth_date=datetime.date(2014, 1, 1),
            is_female=False,
            joined=datetime.date(2015, 8, 21),
            personal_history='Stray',
            preferences_cats='Absolutely!',
            preferences_dogs='It\'s a possibility!',
            preferences_kids='It\'s a possibility!',
            declawed=False,
            spay_neuter=False,
            health='Good, FELV+',
            pet_id='4358',
        )

        self.animal_service.create_animal(
            name='Jane',
            birth_date=datetime.date(2014, 1, 1),
            is_female=False,
            joined=datetime.date(2015, 8, 21),
            personal_history='Stray',
            preferences_cats='Absolutely!',
            preferences_dogs='It\'s a possibility!',
            preferences_kids='It\'s a possibility!',
            declawed=False,
            spay_neuter=False,
            health='Good, FELV+',
            pet_id='4359',
        )

        self.room_service.create_room(
            name='Adult Cat Room'
        )

        self.room_service.create_room(
            name='Senior Cat Room'
        )

        self.animal_service.assign_animal_to_room(
            Animal.objects.get(name='Cookie').pk,
            self.room_service.get_room(name='Senior Cat Room').pk
        )
        self.animal_service.assign_animal_to_room(
            Animal.objects.get(name='Georgie').pk,
            self.room_service.get_room(name='Adult Cat Room').pk
        )

        self.animal_service.assign_animal_to_room(
            Animal.objects.get(name='Ben').pk,
            self.room_service.get_room(name='Adult Cat Room').pk
        )

        self.animal_service.assign_animal_to_room(
            Animal.objects.get(name='Jane').pk,
            self.room_service.get_room(name='Adult Cat Room').pk
        )

    def test_get_animals(self):
        """ Test to retrieve animals from the endpoint: get_animals
        """
        response = self.client.get(reverse('get_animals'))

        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_animal(self):
        """ Test to retrieve a specific animal from the endpoint: get_animal
        """
        cookie_pk = Animal.objects.get(name='Cookie').pk
        response = self.client.get(
            reverse('get_animal', kwargs={'pk': cookie_pk}))
        animal = self.animal_service.get_animal(cookie_pk)
        serializer = AnimalSerializer(animal)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_animal_from_room(self):
        """ Test getting all animals that belong to a room
        """
        room_id = Room.objects.get(name='Adult Cat Room').pk
        response = self.client.get(
            reverse('get_animals_in_room', kwargs={'room': room_id})
        )

        animals_in_room = Animal.objects.filter(animaltoroom__room=room_id)
        serializer = AnimalSerializer(animals_in_room, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(3, len(response.data))

        room_id = Room.objects.get(name='Senior Cat Room').pk
        response = self.client.get(
            reverse('get_animals_in_room', kwargs={'room': room_id})
        )

        animals_in_room = Animal.objects.filter(animaltoroom__room=room_id)
        serializer = AnimalSerializer(animals_in_room, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(1, len(response.data))

    def test_get_animal_list(self):
        """ Test getting list of animals from specific room.
        """

        room_id = Room.objects.get(name='Adult Cat Room').pk
        response = self.client.get(
            reverse('get_animals_list', kwargs={'room': room_id}))

        animals_in_room = Animal.objects.filter(animaltoroom__room=room_id)
        data = serializers.serialize(
            'json', animals_in_room, fields=('name'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'), data)
        self.assertEqual(3, len(json.loads(response.content.decode('utf-8'))))

from ..models import (CheckOut,
                      Room)
from ..services import (AnimalService)
import pdb


class CheckOutService:
    def __init__(self):
        self.animal_service = AnimalService()

    def get_checked_out_animal(self, animal_pk):
        '''Retrieve a checked out animal
        '''
        try:
            checked_out_animal = CheckOut.objects.get(animal_id=animal_pk)
            return checked_out_animal
        except Exception as e:
            return None

    def get_checked_out_animals(self):
        '''Retrieve a list of all checked out animals
        '''
        checked_out_animals = CheckOut.objects.all()
        return checked_out_animals

    def is_animal_checked_out(self, animal_pk):
        animal = self.get_checked_out_animal(animal_pk)
        if animal is None:
            return False
        return True

    def check_out_animal(self, pet_pk, room_pk, note):
        '''Check out an animal
        '''
        if self.is_animal_checked_out(pet_pk):
            raise Exception('Animal is already checked out.')

        animal = self.animal_service.get_animal_from_room(pet_pk, room_pk)
        if animal is None:
            raise Exception('Animal not in the room.')

        room = Room.objects.get(pk=room_pk)

        CheckOut.objects.create(
            animal_id=animal,
            room_id=room,
            checked_out=True,
            time_in=None,
            note=note
        )

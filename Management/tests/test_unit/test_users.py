from django.test import TestCase
from Management.models import *
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class UserTest(TestCase):
    def test_user_creation(self):
        # Crear un usuario
        user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='12345'
        )
        # Verificar que el usuario esté activo
        self.assertTrue(user.is_active)
        # Verificar que el usuario no sea staff por defecto
        self.assertFalse(user.is_staff)
        # Verificar que el usuario no sea superusuario por defecto
        self.assertFalse(user.is_superuser)


class VehicleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')

    def test_vehicle_creation(self):
        vehicle = Vehicle.objects.create(
            customer=self.user,
            brand='Test brand',
            model='Test model',
            patent='ABC123',
            year=2020,
        )
        self.assertEqual(str(vehicle), "Test brand Test model ~ Patente: ABC123")

# Repite la estructura similar para cada modelo
class WorkshopTest(TestCase):
    def test_workshop_creation(self):
        workshop = Workshop.objects.create(
            name='Test Workshop',
            address='Test Address',
            num_address=123,
        )
        self.assertEqual(str(workshop), "Test Workshop. Test Address # 123")

class MechanicTest(TestCase):
    def test_mechanic_creation(self):
        mechanic = Mechanic.objects.create(
            first_name='Test',
            last_name='Mechanic',
            phone='123456789',
            specialty='Mecánico',
        )
        self.assertEqual(str(mechanic), "Test Mechanic - Mecánico")

class AttentionTest(TestCase):
    def test_attention_creation(self):
        current_time = timezone.now()
        attention = Attention.objects.create(attention=current_time)
        formatted_time = attention.formatted_attention()
        self.assertIn(formatted_time[-2:], ["AM", "PM"])
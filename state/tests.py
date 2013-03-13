# -*- coding:utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from states.models import State, City


class StateTest(TestCase):

    def test_creation(self):

        instance = State.objects.create(name='Amazonas', uf='AM')
        self.assertTrue(instance.pk,'Could not Create Logistics Instance')


class CityTest(TestCase):

    fixtures = ['states.json']

    def test_creation(self):

        state = State.objects.all()[0]
        instance = City.objects.create(state=state, name='Manaus')
        
        
#Views test
class StateViewTest(TestCase):
    
    fixtures = ['states.json', 'cities.json']
    
    def test_json_combo(self):
        state = State.objects.all()[0]
        city = City.objects.filter(state=state)[0]
        
        url = reverse('states_json_combo')
        data = {'state_pk': state.pk}
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, city.name)


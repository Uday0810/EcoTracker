from django.forms import ModelForm
from .models import UserInput,UserChallenge
from django import forms

class UserInputForm(ModelForm):
    class Meta:
        #model = UserInput
        #fields = '__all__'
        model = UserInput
        fields = ['twoWheeler','bus','trains','car','longHaulFlights','shortFlights','shortHaulFlights','ferry','naturalGas','coal','lpg',
                  'oil','metalBurned','glassBurned','paperBurned','organicWaste','electricityConsumed','waterConsumed','paperConsumed','cf']
        
        labels = {
            'twoWheeler' : 'Distance Traveled by Two-Wheeler (km)',
            'bus' : 'Distance Traveled by Bus (km)',
            'car' : 'Distance Traveled by Car (km)',
            'longHaulFlights' : 'Distance traveled in a Long-Haul-Flight(>6000 km) (km)',
            'shortFlights' : 'Distance traveled in a Short-Flight',
            'shortHaulFlights' : 'Distance traveled by Short-Haul-Flights(>1500 Km ; <6000 km) (km)',
            'ferry' : 'Distance traveled by ferry',
            'naturalGas' : 'Natural Gas used (GJ)',
            'coal' : 'Coal Used (GJ)',
            'lpg' : 'LPG used (GJ)',
            'oil' : 'Oil used (GJ)',
            'metalBurned' : 'Amount of metal waste (kg)',
            'glassBurned' : 'Amount of glass waste (kg)',
            'organicWaste' : 'Amount of organic waste (kg)',
            'electricityConsumed' : 'Amount of electricity utilized (KWh)',
            'waterConsumed' : 'Estimated amount of water used (litres)',
            'paper' : 'Amount of paper used (kg)'

        }

        widgets = {
            'cf': forms.TextInput(attrs={'readonly': 'readonly', 'id': 'cf-input'}),
        }


class ChallengeLogForm(forms.ModelForm):
    confirmed = forms.BooleanField(initial=False, required=False)
    class Meta:
        model = UserChallenge
        fields = ['description','confirmed']
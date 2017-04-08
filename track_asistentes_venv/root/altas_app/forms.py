from django import forms
## {% load widget_tweaks %}
##  {{ form.rfid|attr:"placeholder:ingresa rfid"}}
CHOICES_CARGO=[('Maestro','Maestro'),
         ('Alumno','Alumno'),
         ('Director','Director')]

class AltaForm(forms.Form):
    rfid = forms.CharField(label='RFID', max_length=100)
    matricula = forms.CharField(label='ID', max_length=100)
    nombre = forms.CharField(label='NOMBRE', max_length=100)
    facultad = forms.CharField(label='FACULTAD', max_length=100)
    cargo = forms.ChoiceField(choices=CHOICES_CARGO, widget=forms.RadioSelect())
    suplente = forms.BooleanField(required=False)
    
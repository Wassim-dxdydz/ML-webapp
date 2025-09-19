from django import forms

SOIL_TYPES = [
    ('argile', 'Argile'),
    ('limons', 'Limons'),
    ('marne', 'Marne'),
    ('sable', 'Sable'),
]

TARGET_TYPES = [
    ('cu', 'CU'),
    ('uu', 'UU'),
    ('cd', 'CD'),
]

class TrainingForm(forms.Form):
    soil_type = forms.ChoiceField(label="Nature du sol", choices=SOIL_TYPES)
    target_type = forms.ChoiceField(label="Type de prédiction", choices=TARGET_TYPES)

    FC = forms.FloatField(label="FC (%)", min_value=0.0, max_value=100.0, initial=30.0)
    WL = forms.FloatField(label="WL", min_value=0.0, max_value=100.0, initial=40.0)
    IP = forms.FloatField(label="IP", min_value=0.0, max_value=100.0, initial=15.0)
    MC = forms.FloatField(label="MC (%)", min_value=0.0, max_value=100.0, initial=20.0)
    SR = forms.FloatField(label="SR (%)", min_value=0.0, max_value=150.0, initial=80.0, required=False)
    ROD = forms.FloatField(label="Masse volumique sèche (g/cm³)", min_value=1.0, max_value=2.5, initial=1.6)

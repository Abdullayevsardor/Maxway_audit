from django import forms
from .models import Branch, Item, Score

# Formada 0 dan 3 gacha ball tanlash imkonini beradi
SCORE_CHOICES = (
    (3, '3 (Yashil)'),
    (2, '2 (Sariq)'),
    (1, '1 (Qizil)'),
    (0, '0 (Qizil/Qo\'shilmagan)'),
)

class AuditForm(forms.Form):
    # 1. Filialni tanlash
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        label="Filialni Tanlang",
        empty_label="--- Filial ---",
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dinamik ravishda har bir Item uchun ball va rasm maydonlarini qo'shamiz
        for item in Item.objects.all():
            # Ball kiritish maydoni (0-3)
            self.fields[f'score_{item.id}'] = forms.ChoiceField(
                choices=SCORE_CHOICES,
                label=f'{item.category.name}: {item.text}', # Category va Item nomini ko'rsatish
                widget=forms.RadioSelect, # Radio tugmalar shaklida
                required=True
            )
            
            # Rasm yuklash maydoni (ixtiyoriy)
            self.fields[f'image_{item.id}'] = forms.ImageField(
                label="Rasm (ixtiyoriy)",
                required=False,
                help_text="Bu bandga tegishli rasm yuklang."
            )
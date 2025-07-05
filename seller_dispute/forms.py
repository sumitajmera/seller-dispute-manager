from django import forms
from .models import DisputeCase, Return
import uuid

class DisputeCaseForm(forms.ModelForm):
    class Meta:
        model = DisputeCase
        fields = ['reason', 'description', 'return_event', 'resolution_notes', 'disputed_amount']
        widgets = {
            'reason': forms.TextInput(attrs={'maxlength': 60, 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'maxlength': 120, 'class': 'form-control'}),
            'resolution_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'disputed_amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'min': '0'})
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'open'
        if not instance.case_number:
            instance.case_number = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class DisputeCaseStatusUpdateForm(forms.Form):
    status = forms.ChoiceField(choices=DisputeCase.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}), required=False) 
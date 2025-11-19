from django import forms
from .models import (
    CVSubmission, LanguageSkill, ComputerSkill, Education,
    ProfessionalMembership, ResearchArea, Training,
    ProfessionalProject, Award, Patent, Grant, OtherInstitution, Unit
)

class EmailVerificationForm(forms.Form):
    email = forms.EmailField(label='University Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your.email@abu.edu.ng'
    }))

class CVSubmissionForm(forms.ModelForm):
    class Meta:
        model = CVSubmission
        fields = ['name', 'tel_no', 'unit', 'age_bracket']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'tel_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'unit': forms.Select(attrs={
                'class': 'form-select',
            }),
            'age_bracket': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimize the unit queryset (e.g., order by name)
        self.fields['unit'].queryset = Unit.objects.all().order_by('name')

class LanguageSkillForm(forms.ModelForm):
    class Meta:
        model = LanguageSkill
        fields = ['language', 'proficiency']
        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
        }

class ComputerSkillForm(forms.ModelForm):
    class Meta:
        model = ComputerSkill
        fields = ['skill', 'proficiency']
        widgets = {
            'skill': forms.TextInput(attrs={'class': 'form-control'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'year']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProfessionalMembershipForm(forms.ModelForm):
    class Meta:
        model = ProfessionalMembership
        fields = ['organization', 'membership_type', 'year_joined']
        widgets = {
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'membership_type': forms.Select(attrs={'class': 'form-select'}),
            'year_joined': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ResearchAreaForm(forms.ModelForm):
    class Meta:
        model = ResearchArea
        fields = ['area']
        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['title', 'institution', 'year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProfessionalProjectForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProject
        fields = ['title', 'role', 'description', 'start_year', 'end_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['name', 'organization', 'year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PatentForm(forms.ModelForm):
    class Meta:
        model = Patent
        fields = ['title', 'patent_number', 'year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'patent_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class GrantForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = ['title', 'amount', 'year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class OtherInstitutionForm(forms.ModelForm):
    class Meta:
        model = OtherInstitution
        fields = ['name', 'purpose']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
        }
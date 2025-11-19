from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.forms import formset_factory
from django.forms import inlineformset_factory
from .models import CVSubmission, LanguageSkill, Grant, ComputerSkill, Education, ProfessionalMembership, ResearchArea, Training, ProfessionalProject, Award, Patent, OtherInstitution
from .forms import EmailVerificationForm, CVSubmissionForm, GrantForm, LanguageSkillForm, ComputerSkillForm, EducationForm, ProfessionalMembershipForm, ResearchAreaForm, TrainingForm, ProfessionalProjectForm, AwardForm, PatentForm, OtherInstitutionForm


import random
import string

def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def email_verification(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            verification_code = generate_verification_code()
            request.session['verification_email'] = email
            request.session['verification_code'] = verification_code
            
            send_mail(
                'ABUCONS CV Submission Verification',
                f'Your verification code is: {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('verify_code')
    else:
        form = EmailVerificationForm()
    
    return render(request, 'cv/email_verification.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        user_code = request.POST.get('verification_code', '')
        saved_code = request.session.get('verification_code', '')
        
        if user_code == saved_code:
            request.session['verified'] = True
            return redirect('cv_submission')
        else:
            messages.error(request, "Invalid verification code. Please try again.")
    
    return render(request, 'cv/verify_code.html')





def save_formset(formset, cv):
    """Helper method to save formset data with CV relation"""
    instances = formset.save(commit=False)
    for instance in instances:
        instance.cv = cv
        instance.save()
    for form in formset.deleted_objects:
        form.delete()

def cv_submission(request):
    if not request.session.get('verified'):
        return redirect('email_verification')

    # Define formset factory configurations with new names and ordering
    formset_classes = {
        'language': inlineformset_factory(CVSubmission, LanguageSkill, form=LanguageSkillForm, can_delete=True, extra=1),
        'education': inlineformset_factory(CVSubmission, Education, form=EducationForm, can_delete=True, extra=1),
        'training': inlineformset_factory(CVSubmission, Training, form=TrainingForm, can_delete=True, extra=1),
        'computer': inlineformset_factory(CVSubmission, ComputerSkill, form=ComputerSkillForm, can_delete=True, extra=1),
        'research': inlineformset_factory(CVSubmission, ResearchArea, form=ResearchAreaForm, can_delete=True, extra=1, max_num=10),
        'patent': inlineformset_factory(CVSubmission, Patent, form=PatentForm, can_delete=True, extra=1),
        'grant': inlineformset_factory(CVSubmission, Grant, form=GrantForm, can_delete=True, extra=1),
        'award': inlineformset_factory(CVSubmission, Award, form=AwardForm, can_delete=True, extra=1),
        'membership': inlineformset_factory(CVSubmission, ProfessionalMembership, form=ProfessionalMembershipForm, can_delete=True, extra=1),
        'project': inlineformset_factory(CVSubmission, ProfessionalProject, form=ProfessionalProjectForm, can_delete=True, extra=1),
        'institution': inlineformset_factory(CVSubmission, OtherInstitution, form=OtherInstitutionForm, can_delete=True, extra=1),
    }

    # Display names mapping
    display_names = {
        'language': 'Language Competency',
        'education': 'Tertiary Education',
        'training': 'Additional Qualifications/Trainings with Certificate',
        'computer': 'ICT Skills',
        'research': 'Core Research Areas',
        'patent': 'Patents',
        'grant': 'grants',
        'award': 'Awards/Recognitions',
        'membership': 'Professional Memberships',
        'project': 'Professional Projects',
        'institution': 'Other Institutions',
    }

    if request.method == 'POST':
        cv_form = CVSubmissionForm(request.POST)
        temp_cv = CVSubmission()  # Dummy instance to build inline formsets
        formsets = {name: factory(request.POST, prefix=name, instance=temp_cv) for name, factory in formset_classes.items()}

        all_valid = cv_form.is_valid() and all(fs.is_valid() for fs in formsets.values())

        if all_valid:
            cv = cv_form.save(commit=False)
            cv.email = request.session.get('verification_email')
            cv.save()

            for name, formset in formsets.items():
                formset.instance = cv
                save_formset(formset, cv)

            messages.success(request, "CV submitted successfully!")
            return redirect('success')
    else:
        cv_form = CVSubmissionForm()
        dummy_cv = CVSubmission()
        formsets = {name: factory(prefix=name, instance=dummy_cv) for name, factory in formset_classes.items()}

    context = {
        'cv_form': cv_form,
        'formsets': formsets,
        'display_names': display_names,
        'formset_order': ['language', 'education', 'training', 'computer', 'research', 'patent', 'grant', 'award', 'membership', 'project', 'institution'],
    }
    return render(request, 'cv/cv_submission.html', context)


def success(request):
    return render(request, 'cv/success.html')
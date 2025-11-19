from django.contrib import admin
from .models import (
    Unit, CVSubmission, LanguageSkill, ComputerSkill, Education,
    ProfessionalMembership, ResearchArea, Training, Grant,
    ProfessionalProject, Award, Patent, OtherInstitution
)

# Inline Models
class LanguageSkillInline(admin.TabularInline):
    model = LanguageSkill
    extra = 1

class ComputerSkillInline(admin.TabularInline):
    model = ComputerSkill
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class MembershipInline(admin.TabularInline):
    model = ProfessionalMembership
    extra = 1

class ResearchAreaInline(admin.TabularInline):
    model = ResearchArea
    extra = 1

class TrainingInline(admin.TabularInline):
    model = Training
    extra = 1

class ProjectInline(admin.TabularInline):
    model = ProfessionalProject
    extra = 1

class AwardInline(admin.TabularInline):
    model = Award
    extra = 1

class PatentInline(admin.TabularInline):
    model = Patent
    extra = 1

class GrantInline(admin.TabularInline):
    model = Grant
    extra = 1

class OtherInstitutionInline(admin.TabularInline):
    model = OtherInstitution
    extra = 1


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit_type', 'parent']
    list_filter = ['unit_type']
    search_fields = ['name']


@admin.register(CVSubmission)
class CVSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'tel_no', 'unit', 'age_bracket', 'status', 'submitted_at']
    list_filter = ['status', 'age_bracket', 'unit']
    search_fields = ['name', 'email', 'tel_no']
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']
    
    inlines = [
        LanguageSkillInline,
        ComputerSkillInline,
        EducationInline,
        MembershipInline,
        ResearchAreaInline,
        TrainingInline,
        ProjectInline,
        AwardInline,
        PatentInline,
        GrantInline,
        OtherInstitutionInline,
    ]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'tel_no', 'email', 'age_bracket')
        }),
        ('Institutional Info', {
            'fields': ('unit',)
        }),
        ('Status Tracking', {
            'fields': ('status',)
        }),
    )


@admin.register(LanguageSkill)
class LanguageSkillAdmin(admin.ModelAdmin):
    list_display = ['cv', 'language', 'proficiency']
    search_fields = ['language', 'cv__name']
    list_filter = ['proficiency']


@admin.register(ComputerSkill)
class ComputerSkillAdmin(admin.ModelAdmin):
    list_display = ['cv', 'skill', 'proficiency']
    search_fields = ['skill', 'cv__name']
    list_filter = ['proficiency']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['cv', 'degree', 'institution', 'year']
    search_fields = ['degree', 'institution', 'cv__name']
    list_filter = ['year']


@admin.register(ProfessionalMembership)
class ProfessionalMembershipAdmin(admin.ModelAdmin):
    list_display = ['cv', 'organization', 'membership_type', 'year_joined']
    list_filter = ['membership_type', 'year_joined']
    search_fields = ['organization', 'cv__name']


@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ['cv', 'area']
    search_fields = ['area', 'cv__name']


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['cv', 'title', 'institution', 'year']
    search_fields = ['title', 'institution', 'cv__name']
    list_filter = ['year']


@admin.register(ProfessionalProject)
class ProfessionalProjectAdmin(admin.ModelAdmin):
    list_display = ['cv', 'title', 'start_year', 'end_year']
    search_fields = ['title', 'cv__name']
    list_filter = ['start_year', 'end_year']


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['cv', 'name', 'organization', 'year']
    search_fields = ['name', 'organization', 'cv__name']
    list_filter = ['year']


@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = ['cv', 'title', 'patent_number', 'year']
    search_fields = ['title', 'patent_number', 'cv__name']
    list_filter = ['year']

@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ['cv', 'title', 'amount', 'year']
    search_fields = ['title', 'amount', 'cv__name']
    list_filter = ['year']


@admin.register(OtherInstitution)
class OtherInstitutionAdmin(admin.ModelAdmin):
    list_display = ['cv', 'name', 'purpose']
    search_fields = ['name', 'purpose', 'cv__name']

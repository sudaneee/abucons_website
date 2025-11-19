from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Unit(models.Model):
    UNIT_TYPE_CHOICES = [
        ('faculty', 'Faculty'),
        ('department', 'Department'),
        ('institute', 'Institute'),
        ('center', 'Center/Directorate'),
    ]
    name = models.CharField(max_length=200, unique=True)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.name}"

class CVSubmission(models.Model):
    name = models.CharField(max_length=100)
    tel_no = models.CharField(max_length=20)
    email = models.EmailField()
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

    AGE_BRACKETS = [
        ('20-30', '20-30 years'),
        ('31-40', '31-40 years'),
        ('41-50', '41-50 years'),
        ('51-60', '51-60 years'),
        ('61+', '61+ years'),
    ]
    age_bracket = models.CharField(max_length=5, choices=AGE_BRACKETS)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.name} - {self.unit.name if self.unit else 'No Unit'}"

class LanguageSkill(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=50)
    PROFICIENCY_LEVELS = [
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('fluent', 'Fluent'),
    ]
    proficiency = models.CharField(max_length=12, choices=PROFICIENCY_LEVELS)

    class Meta:
        unique_together = ('cv', 'language')

    def __str__(self):
        return f"{self.language} ({self.get_proficiency_display()})"

class ComputerSkill(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='computer_skills')
    skill = models.CharField(max_length=100)
    PROFICIENCY_LEVELS = [
        ('basic', 'Basic'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ]
    proficiency = models.CharField(max_length=9, choices=PROFICIENCY_LEVELS)

    def __str__(self):
        return f"{self.skill} ({self.get_proficiency_display()})"

class Education(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.degree} - {self.institution} ({self.year})"

class ProfessionalMembership(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='memberships')
    organization = models.CharField(max_length=150)
    MEMBERSHIP_TYPES = [
        ('graduate', 'Graduate Member'),
        ('associate', 'Associate Member'),
        ('full', 'Full Member'),
        ('fellow', 'Fellow'),
    ]
    membership_type = models.CharField(max_length=9, choices=MEMBERSHIP_TYPES)
    year_joined = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )

    def __str__(self):
        return f"{self.organization} ({self.get_membership_type_display()})"

class ResearchArea(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='research_areas')
    area = models.CharField(max_length=200)

    def __str__(self):
        return self.area

class Training(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='trainings')
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=150)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} - {self.institution} ({self.year})"

class ProfessionalProject(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    role = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    start_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )
    end_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        blank=True,
        null=True
    )

    def clean(self):
        if self.end_year and self.start_year > self.end_year:
            raise ValidationError("End year cannot be before start year")

    def __str__(self):
        period = f"{self.start_year}-{self.end_year}" if self.end_year else f"{self.start_year}"
        return f"{self.title} ({period})"

class Award(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='awards')
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=150)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.name} - {self.organization} ({self.year})"

class Grant(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='grants')
    title = models.CharField(max_length=200)
    amount = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} ({self.year})"


class Patent(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='patents')
    title = models.CharField(max_length=200)
    patent_number = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} ({self.year})"

class OtherInstitution(models.Model):
    cv = models.ForeignKey(CVSubmission, on_delete=models.CASCADE, related_name='other_institutions')
    name = models.CharField(max_length=150)
    purpose = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.purpose}"

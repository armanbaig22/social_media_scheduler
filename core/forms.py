from django import forms

from django.utils import timezone


class CreatePostForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    media = forms.FileField(label='Media (Image/Video)', required=False)
    post_type = forms.ChoiceField(choices=[('draft', 'Draft'), ('schedule', 'Schedule')], initial='draft', label='Post Type')
    schedule_datetime = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), label='Schedule Date & Time')

    def clean_schedule_datetime(self):
        schedule_datetime = self.cleaned_data['schedule_datetime']

        # Ensure the scheduled datetime is in the future
        if schedule_datetime <= timezone.now():
            raise forms.ValidationError("Scheduled date and time must be in the future.")

        return schedule_datetime

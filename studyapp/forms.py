from django import forms
from .models import Meeting

class MeetingCreateForm(forms.ModelForm):
    class Meta:
        model = Meeting
        # no idea if this is right
        # start_time = forms.DateTimeField()
        # end_time = forms.DateTimeField()
        fields = [
            'location',
            'course',
            'start_time',
            'end_time',
            'post_text', 
        ]
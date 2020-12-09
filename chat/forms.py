from django.forms import ModelForm

from chat.models import LOG

class CALForm(ModelForm):
    class Meta:
        model = LOG
        fields = ['expression']

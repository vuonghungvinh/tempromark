
from django import forms


class ShareForm(forms.Form):
    def __init__(self, *args, **kwargs):
        path = kwargs.pop('path')
        super(ShareForm, self).__init__(*args, **kwargs)
        self.fields['body'].initial = '{}{}'.format(
            self.fields['body'].initial, path)

    from_address = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Your e-mail address'}),
        label='From',
        required=True,)

    to_address = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Their e-amil address'}),
        label='To',
        required=True,)

    subject = forms.CharField(
        initial='Share Page: Tepromark',
        widget=forms.TextInput(),
        required=True,)

    body = forms.CharField(
        initial="I have shared a page with you on Tepromark:\nhttp://tepromark.com",
        widget=forms.Textarea(),
        label="message",
        required=True,)

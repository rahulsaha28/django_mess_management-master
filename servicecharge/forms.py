from django import forms


class ServiceForm(forms.Form):
    service_name = forms.CharField(max_length=20, label="Service Name : ")
    debit_tk = forms.FloatField(label="Amount : ")
    check = forms.CharField(label="Select all Member", widget=forms.CheckboxInput, required=False)

    def clean(self):
        cleaned_data = super(ServiceForm, self).clean()
        return cleaned_data
    '''
    This is the most important part if you edit multi choice field 
    you should edit the __init__ method of the parent class
    '''




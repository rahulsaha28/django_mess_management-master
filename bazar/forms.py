from django import forms


class BazarForm(forms.Form):
    cradit_tk = forms.FloatField(label="Bazar Cost : ")
    def clean(self):
        cleaned_data = super(BazarForm, self).clean()
        cradit_tk = cleaned_data.get("cradit_tk")
        if cradit_tk < 0:
            print("hi")
            self.add_error("cradit_tk", "Bazar amount must be some positive value.")
        return cleaned_data
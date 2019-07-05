from django import forms


# poll creation form
class PollForm(forms.Form):
    poll_name = forms.CharField(max_length=20, label="Mess Name: ")
    start_date = forms.DateField(label="Start Date: ", widget=forms.SelectDateWidget)
    end_date = forms.DateField(label="End Date: ", widget=forms.SelectDateWidget)

    def clean(self):
        cleaned_data = super(PollForm, self).clean()
        if not cleaned_data["poll_name"]:
            self.add_error("poll_name", "Mess name must be Given")
        if len(cleaned_data["poll_name"]) < 4:
            self.add_error("poll_name", "Mess name must be gratter than 4 letter.")
        if cleaned_data["start_date"] > cleaned_data["end_date"]:
            self.add_error("start_date","Start date must small than End date.")
        return cleaned_data


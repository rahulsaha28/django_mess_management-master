from django import forms


# This is the signup form
class SignUpForm(forms.Form):
    email = forms.EmailField(label="Enter Email (Gmail) :")
    password = forms.CharField(label="Enter the password :", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Enter password (Again) :", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data["email"]
        password1 = cleaned_data["password"]
        password2 = cleaned_data["password2"]
        if not "@gmail.com" in email:
            self.add_error("email", "Email must be Gmail.")
        if len(password1) < 7:
            self.add_error("password", "Password must be gratter than 7.")
        if password1 != password2:
            self.add_error("password2", "Password must be match.")
        return cleaned_data


# login form
class LogInForm(forms.Form):
    email = forms.EmailField(label="Your Email : ")
    password = forms.CharField(label="Password : ", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LogInForm, self).clean()
        email = cleaned_data["email"]
        password = cleaned_data["password"]

        if not "@gmail.com" in email:
            self.add_error("email", "Email must be Gmail")

        return cleaned_data

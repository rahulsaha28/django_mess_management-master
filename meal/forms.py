from django import forms


# this is the meal initial creation form
class MealForm(forms.Form):
    brake_fast = forms.FloatField(label="BrakeFast : ")
    lunch = forms.FloatField(label="Lunch :")
    dinner = forms.FloatField(label="Dinne :")

    def clean(self):
        cleaned_data = super(MealForm, self).clean()
        '''
        Be careful here because when we use cleaned_data.get() 
        after we call it, it set the value of this disc is None  
        '''
        brake_fast = cleaned_data.get("brake_fast")
        lunch = cleaned_data.get("lunch")
        dinner = cleaned_data.get("dinner")
        if brake_fast > 10.0 :
            self.add_error("brake_fast"," Barke fast is not gratter than 10")
        if brake_fast < 0.0:
            self.add_error("brake_fast", " Barke fast is not less than 0")
        if lunch > 10.0:
            self.add_error("lunch", " Lunch fast is not gratter than 10")
        if lunch < 0.0:
            self.add_error("lunch", "Lunch is not less than 0")
        if dinner > 10.0:
            self.add_error("dinner", " Dinner fast not gratter than 10")
        if dinner < 0.0:
            self.add_error("dinner", "Dinner is not less than 0")
        return cleaned_data
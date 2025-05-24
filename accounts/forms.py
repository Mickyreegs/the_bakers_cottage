from django import forms

class CustomSignupForm(forms.Form):  
    first_name = forms.CharField(max_length=150, required=True, label="First Name")
    last_name = forms.CharField(max_length=150, required=True, label="Last Name")

    def signup(self, request, user):
        from allauth.account.forms import SignupForm  
        
        base_form = SignupForm(self.cleaned_data)  # ✅ Create an instance
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
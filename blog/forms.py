from django import forms
from .models import image, top_post, User, tags, response_post, Profile

class PostForm(forms.ModelForm):
    #author = forms.CharField(max_length=128)
    title = forms.CharField(max_length=128)
    text = forms.CharField(max_length=4000, widget=forms.Textarea(attrs={'rows':7, 'cols':77}))

    class Meta:
        model = top_post
        fields = ('title', 'text',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = image
        fields = ('image',)

class TagForm(forms.ModelForm):
    tag = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':2, 'cols':45}))

    class Meta:
        model = tags
        fields = ('tag',)

class SearchForm(forms.ModelForm):
    string = forms.CharField(max_length=200)

'''Uses old django girls post object
class PostForm(forms.ModelForm):

    class Meta:
        #model = Post
        fields = ('title', 'text',)
'''

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'rows':4, 'cols':50}),
                           label="")
    class Meta:
        model = response_post
        fields = ('text',)

####
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'city', 'zipcode')
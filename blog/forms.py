from django import forms
from .models import image, top_post, User, tags

class PostForm(forms.ModelForm):
    #author = forms.CharField(max_length=128)
    title = forms.CharField(max_length=128)
    text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':7, 'cols':77}))

    class Meta:
        model = top_post
        fields = ('title', 'text',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = image
        fields = ('image',)

class TagForm(forms.ModelForm):
    tag = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'rows':2, 'cols':45}))

    class Meta:
        model = tags
        fields = ('tag',)


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
        fields = ('username', 'first_name', 'last_name', 'email' )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

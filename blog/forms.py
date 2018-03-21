from django import forms
from .models import image, top_post
# from .models import Post

class PostForm(forms.ModelForm):
    author = forms.CharField(max_length=128)
    text = forms.CharField(max_length=245, label="Blog Text")

    class Meta:
        model = top_post
        fields = ('title', 'author',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = image
        fields = ('image',)

'''Uses old django girls post object
class PostForm(forms.ModelForm):

    class Meta:
        #model = Post
        fields = ('title', 'text',)
'''

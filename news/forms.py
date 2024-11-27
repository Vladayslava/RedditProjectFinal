from django import forms
from .models import Post, Comment, Category, Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category'] 
        labels = {
            'title': 'Title',
            'content': 'Content',
            'category': 'Category',
        }
        help_texts = {
            'title': 'Enter the title for your post.',
            'content': 'Write the content of the post here.',
            'category': 'Select a category for your post.',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Category Name',
        }
        help_texts = {
            'name': 'Enter the name of the new category.',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comment',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'cols': 80}),  
        }

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Password Confirmation')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }
        help_texts = {
            'username': 'Enter a unique username.',
            'email': 'Enter your email address.',
            'password': 'Create a strong password.',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {
            'avatar': 'Avatar',
        }
        help_texts = {
            'avatar': 'Select an image for your avatar.',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        self.validate_image_size(avatar)
        return avatar

    def validate_image_size(self, image):
        max_size = 2 * 1024 * 1024  # 2 MB
        if image.size > max_size:
            raise forms.ValidationError(f"The file size must not exceed {max_size / (1024 * 1024)} MB.")

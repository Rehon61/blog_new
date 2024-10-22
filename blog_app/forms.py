from django import forms
from .models import Comment, Category, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ваш комментарий...'}),
        }
        labels = {
            'text': 'Текст комментария',
        }


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название категории'}),
    )

    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название категории',
        }
        help_texts = {
            'name': 'Введите название категории (от 3 до 200 символов)',
        }
        min_length = {
            'name': 3,
        }
        max_length = {
            'name': 200,
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Категория с таким названием уже существует.")
        return name

class TagForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название тега'}),
        label='Название тега'
    )

    class Meta:
        model = Tag
        fields = ['name']

    def save(self, commit=True):
        return tag

    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError('Тег с таким названием уже существует')
        return name
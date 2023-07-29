from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3 ,  'id':"cMessage" ,'class': "h-full-width" , 'placeholder': "Comment"}),label="")

    class Meta:
        model = Comment
        fields = ('content',)



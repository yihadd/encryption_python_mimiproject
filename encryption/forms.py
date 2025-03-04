# Import Django forms module
from django import forms

# Form for handling document uploads with a title and secret message
class DocumentForm(forms.Form):
    # Title field with maximum length of 200 characters
    title = forms.CharField(max_length=200)
    # File upload field
    document = forms.FileField()
    # Text area for entering a secret message
    secret_message = forms.CharField(widget=forms.Textarea)

# Form for handling text encryption
class EncryptionForm(forms.Form):
    # Available encryption methods
    ENCRYPTION_CHOICES = [
        ('caesar', 'Caesar Cipher'),
        ('vigenere', 'Vigenère Cipher'),
        ('morse', 'Morse Code'),
    ]
    
    # Text area for entering text to encrypt
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    # Dropdown for selecting encryption type
    encryption_type = forms.ChoiceField(choices=ENCRYPTION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # Optional key field for encryption methods that require it
    key = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

# Form for handling text decryption
class DecryptionForm(forms.Form):
    # Available decryption methods (same as encryption)
    ENCRYPTION_CHOICES = [
        ('caesar', 'Caesar Cipher'),
        ('vigenere', 'Vigenère Cipher'),
        ('morse', 'Morse Code'),
    ]
    
    # Optional text area for entering encrypted text
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 5,
        'placeholder': 'Enter encrypted text or upload a file'
    }))
    # Optional file upload field for encrypted files
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    # Dropdown for selecting decryption type
    encryption_type = forms.ChoiceField(choices=ENCRYPTION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # Optional key field for decryption methods that require it
    key = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Custom validation method
    def clean(self):
        # Get the cleaned form data
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        file = cleaned_data.get('file')
        
        # Ensure either text or file is provided
        if not text and not file:
            raise forms.ValidationError("Please either enter text or upload a file")
        
        return cleaned_data 
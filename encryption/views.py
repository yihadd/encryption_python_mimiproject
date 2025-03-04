# Import necessary Django modules and forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EncryptionForm, DecryptionForm
import datetime

# Encrypt text using Caesar cipher with default shift of 3
def encrypt_caesar(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            # Determine ASCII offset based on case
            ascii_offset = ord('A') if char.isupper() else ord('a')
            # Apply shift and wrap around alphabet
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

# Encrypt text using Vigenère cipher with provided key
def encrypt_vigenere(text, key):
    result = ""
    key = key.upper()
    key_length = len(key)
    # Convert key to list of integer shifts
    key_as_int = [ord(i) - ord('A') for i in key]
    
    for i, char in enumerate(text):
        if char.isalpha():
            # Determine ASCII offset based on case
            ascii_offset = ord('A') if char.isupper() else ord('a')
            key_idx = i % key_length
            # Apply shift from key and wrap around alphabet
            shifted = (ord(char) - ascii_offset + key_as_int[key_idx]) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    return result

# Dictionary mapping characters to Morse code
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ' ':'/' }

# Convert text to Morse code
def encrypt_morse(text):
    text = text.upper()
    result = ""
    for char in text:
        if char in MORSE_CODE_DICT:
            result += MORSE_CODE_DICT[char] + " "
    return result.strip()

# Decrypt Caesar cipher by using negative shift
def decrypt_caesar(text, shift=3):
    return encrypt_caesar(text, -shift)  # Decryption is just encryption with negative shift

# Decrypt text encrypted with Vigenère cipher
def decrypt_vigenere(text, key):
    result = ""
    key = key.upper()
    key_length = len(key)
    # Convert key to list of integer shifts
    key_as_int = [ord(i) - ord('A') for i in key]
    
    for i, char in enumerate(text):
        if char.isalpha():
            # Determine ASCII offset based on case
            ascii_offset = ord('A') if char.isupper() else ord('a')
            key_idx = i % key_length
            # Subtract the key (instead of adding) for decryption
            shifted = (ord(char) - ascii_offset - key_as_int[key_idx]) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    return result

# Create reverse lookup dictionary for Morse code decryption
MORSE_CODE_REVERSE = {value: key for key, value in MORSE_CODE_DICT.items()}

# Convert Morse code back to text
def decrypt_morse(text):
    words = text.strip().split('   ')
    result = ""
    for word in words:
        letters = word.split()
        for letter in letters:
            if letter in MORSE_CODE_REVERSE:
                result += MORSE_CODE_REVERSE[letter]
        result += ' '
    return result.strip()

# Handle downloading encrypted text as a file
def download_text(request):
    if request.method == 'POST':
        text = request.POST.get('encrypted_text', '')
        # Create the response with the encrypted text
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="encrypted_text_{timestamp}.txt"'
        return response
    return redirect('encrypt_text')

# Handle text encryption requests
def encrypt_text(request):
    result = None
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            # Get form data
            text = form.cleaned_data['text']
            encryption_type = form.cleaned_data['encryption_type']
            key = form.cleaned_data['key']
            
            # Apply selected encryption method
            if encryption_type == 'caesar':
                result = encrypt_caesar(text)
            elif encryption_type == 'vigenere':
                if key:
                    result = encrypt_vigenere(text, key)
                else:
                    result = "Please provide a key for Vigenère cipher"
            elif encryption_type == 'morse':
                result = encrypt_morse(text)
    else:
        form = EncryptionForm()
    
    # Render template with results
    return render(request, 'encryption/encrypt.html', {
        'form': form,
        'result': result,
        'show_download': result is not None and result != "Please provide a key for Vigenère cipher"
    })

# Handle text decryption requests
def decrypt_text(request):
    result = None
    original_text = None
    if request.method == 'POST':
        form = DecryptionForm(request.POST, request.FILES)
        if form.is_valid():
            # Get text from either file upload or text input
            if 'file' in request.FILES:
                text = request.FILES['file'].read().decode('utf-8')
            else:
                text = form.cleaned_data['text']
            
            # Get form data
            encryption_type = form.cleaned_data['encryption_type']
            key = form.cleaned_data['key']
            original_text = text
            
            # Apply selected decryption method
            if encryption_type == 'caesar':
                result = decrypt_caesar(text)
            elif encryption_type == 'vigenere':
                if key:
                    result = decrypt_vigenere(text, key)
                else:
                    result = "Please provide a key for Vigenère cipher"
            elif encryption_type == 'morse':
                result = decrypt_morse(text)
    else:
        form = DecryptionForm()
    
    # Render template with results
    return render(request, 'encryption/decrypt.html', {
        'form': form,
        'result': result,
        'original_text': original_text
    })

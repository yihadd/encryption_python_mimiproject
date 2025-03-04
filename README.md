# Text Encryption Tool

A web-based encryption tool built with Django that provides multiple encryption methods for text encryption and decryption. This tool allows users to encrypt text using Caesar Cipher, Vigenère Cipher, and Morse Code, with options to download encrypted text and upload files for decryption.

![Image](https://github.com/user-attachments/assets/f2bc3583-eb8f-4fb7-a03a-64fa520e46be)
![Image](https://github.com/user-attachments/assets/e89b6268-647c-437d-9e53-0410f8555e66)

## Features

### Encryption Methods
1. **Caesar Cipher**
   - Classic substitution cipher
   - Shifts each letter by 3 positions in the alphabet
   - Example: 'HELLO' → 'KHOOR'

2. **Vigenère Cipher**
   - Polyalphabetic substitution cipher
   - Uses a keyword for encryption
   - Example:
     ```
     Text: HELLO
     Key:  KEYKE
     Result: RIJVS
     ```

3. **Morse Code**
   - Converts text to dots and dashes
   - Supports letters, numbers, and basic punctuation
   - Example: 'SOS' → '... --- ...'

### Additional Features
- Download encrypted text as .txt files
- Upload encrypted files for decryption
- Clean, responsive Bootstrap interface
- Support for both uppercase and lowercase letters
- Preserves non-alphabetic characters
- Real-time encryption/decryption

## Installation

### Prerequisites
- Python 3.x
- Django 5.0+
- Web browser


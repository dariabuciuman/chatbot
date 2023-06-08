from unidecode import unidecode


def remove_diacritics(text):
    # Convert the text to ASCII characters
    ascii_text = unidecode(text)
    # Replace specific characters with their non-diacritic counterparts
    replacements = {
        'ă': 'a',
        'â': 'a',
        'î': 'i',
        'ș': 's',
        'ț': 't',
        'Ă': 'A',
        'Â': 'A',
        'Î': 'I',
        'Ș': 'S',
        'Ț': 'T'
        # Add more replacements as needed
    }
    for original, replacement in replacements.items():
        ascii_text = ascii_text.replace(original, replacement)
    return ascii_text


def clean_up_diacritics(sentence):
    special_chars = {
        'Äƒ': 'ă',
        'Ã¢': 'â',
        'Ã®': 'î',
        'È™': 'ș',
        'È›': 'ț'
    }
    for special_char, regular_char in special_chars.items():
        sentence = sentence.replace(special_char, regular_char)
    return sentence

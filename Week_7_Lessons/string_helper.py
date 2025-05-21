def reverse(string):
    return string[::-1]

def remove_vowels(string):
    return ''.join(char for char in string if char.lower() not in 'aeiou')
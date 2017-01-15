from random_words import RandomWords

rw = RandomWords()


# create a temporary randomish password
def generate_password():
    words = rw.random_words(count=2)
    return ''.join(words)

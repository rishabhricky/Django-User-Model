import random
import string

from django.conf import settings

# Create a random string for activation key

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 15)

def code_generator(size=SHORTCODE_MIN, char=string.ascii_lowercase + string.digits):
    # new_code = ''
    # for _ in range(size):
    #     new_code+ = random.choice(char)
    # return new_code

    return ''.join(random.choice(char) for _ in range(size))

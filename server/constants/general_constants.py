import random
import string

_accepted_file_list = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']  # private property

accepted_file_list = lambda: _accepted_file_list
generate_guid = lambda n: ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

DialogClose = "השיחה הסתיימה"

true_string = ["true", "1", "yes"]

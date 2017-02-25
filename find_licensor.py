from slugify import slugify


def find_licensor(title, clients):
    for key, value in clients.iteritems():
        if slugify(key) in slugify(title):
            return value
    return "nil"

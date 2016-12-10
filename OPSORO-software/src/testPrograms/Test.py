
class a(object):
    def __init__(self):
        self.count = 1

class b(object):
    def __init__(self):
        self.val1 = None


i1 = b()
a  = a()
i1.val1 = a
a.count = a.count + 1
i1.val1.count = i1.val1.count +1

print a.count



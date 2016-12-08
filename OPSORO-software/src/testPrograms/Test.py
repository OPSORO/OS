
class a(object):
    def blink(self):
        print "uitvoeren van blinkfunctie"



blink = getattr(a, "blink", None)
print blink
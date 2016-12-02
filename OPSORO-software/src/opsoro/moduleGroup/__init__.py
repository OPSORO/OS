
class moduleGroup(object):
    """
        this is a help class to contol the modules verry easely. This class
        is not intended to make instances of if but is a base class for
        inheretance of other subclasses.

        de modulles worden opgeslagen en gegroupeerd in een dictionairy. Een modulle
        kan behoren tot meerdere groupen binnen de dictionary. Tot welke groepen een
        modulle behoort word bepaald doot de tags die worden opgegeven bij initialisatie.
        elke modulle die wordt toegevoegt behoort automatisch tot de groep 'all'

        vb. module 'left_front_wheel' heeft tags: left, front, all(default)
    """

    #opm: omdat doorheen het programma meestal 'name' wordt gebruikt gebruik ik nu ook name maar ik denk dat het mischien overzichteliijker zou zijn mar 'id'
    def __init__(self, name):
        self.name = name
        self.modules = {"all": []}

    def __repr__(self):
        return self.name

    def add(self,module,tags=[]):
        for t in tags:
            self.modules["all"] = self.modules["all"] + [module]
            if t in self.modules:
                self.modules[t] = self.modules[t] + [module]
            else:
                self.modules[t] = [module]

    def getModules(self, tags=[]):
        result = []
        for t in tags:
            result += self.modules[t]
        result = {obj.name: obj for obj in result}.values()
        return result

    def __str__(self):
        return str(self.name)

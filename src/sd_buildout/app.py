import grok

from sd_buildout import resource

class Sd_buildout(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def update(self):
        resource.style.need()

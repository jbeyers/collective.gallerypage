from zope import schema
from five import grok

from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.textfield import RichText

from collective.gallerypage import MessageFactory as _


class IGalleryPage(form.Schema, IImageScaleTraversable):
    """
    A Gallery Page
    """
    text = RichText(title = _(u'Text'),
        required = False)


class GalleryPage(dexterity.Container):
    grok.implements(IGalleryPage)
    

class View(grok.View):
    grok.context(IGalleryPage)
    grok.require('zope2.View')
    grok.name('view')

    def get_images(self):
        return self.context.listFolderContents(contentFilter={
            'portal_type': 'Image',
            'sort_on': 'getObjPositionInParent'})

    def get_first_image(self):
        images = self.get_images()
        if not images:
            return None
        return images[0]

    def get_files(self):
        return self.context.listFolderContents(contentFilter={
            'portal_type': 'File',
            'sort_on': 'getObjPositionInParent'})

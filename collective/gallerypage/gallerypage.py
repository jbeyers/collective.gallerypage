from Products.CMFCore.utils import getToolByName
from plone.supermodel import model
from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.textfield import RichText

from collective.gallerypage import MessageFactory as _
from Products.Five.browser import BrowserView
from zope.interface import implementer


class IGalleryPage(model.Schema, IImageScaleTraversable):
    """
    A Gallery Page
    """

    text = RichText(title=_(u"Text"), required=False)


@implementer(IGalleryPage)
class GalleryPage(Container):
    def SearchableText(self):
        value = ""
        if self.text:
            transforms = getToolByName(self, "portal_transforms")
            try:
                stream = transforms.convertTo(
                    "text/plain", self.text.output, mimetype="text/html"
                )
            except TypeError:
                return u""

            value = stream.getData().strip()

        subjects = u" ".join([i for i in self.subject])
        title = str(self.Title())
        description = str(self.Description())
        terms = u" ".join([title, description, value, subjects])
        return terms


class View(BrowserView):
    def get_images(self):
        return self.context.listFolderContents(
            contentFilter={"portal_type": "Image", "sort_on": "getObjPositionInParent"}
        )

    def get_first_image(self):
        images = self.get_images()
        if not images:
            return None
        return images[0]

    def get_files(self):
        return self.context.listFolderContents(
            contentFilter={"portal_type": "File", "sort_on": "getObjPositionInParent"}
        )

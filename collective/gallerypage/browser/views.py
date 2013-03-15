from zope import schema
from zope.interface import implements, Interface
from zope.app.component.hooks import getSite
from five import grok
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATTopic


from collective.gallerypage.interfaces import IAddOnInstalled

grok.templatedir('templates')

class IGalleryPageListView(Interface):
    """ Allowed template variables exposed from the view.
    """

    # Item list as iterable Products.CMFPlone.PloneBatch.Batch object
    contents = schema.Object(Interface)

class GalleryPageListView(grok.View):
    """ Show gallery pages in a list.
    """
    grok.context(Interface)
    grok.layer(IAddOnInstalled)
    implements(IGalleryPageListView)

    index = grok.PageTemplateFile("templates/gallerypagelistview.pt")

    def query(self, start, limit, contentFilter):
        """ Make catalog query for the folder listing.

        @param start: First index to query

        @param limit: maximum number of items in the batch

        @param contentFilter: portal_catalog filtering dictionary with index -> value pairs.

        @return: Products.CMFPlone.PloneBatch.Batch object
        """

        # Batch size
        b_size = limit

        # Batch start index, zero based
        b_start = start

        # We use different query method, depending on
        # whether we do listing for topic or folder
        if IATTopic.providedBy(self.context):
            # ATTopic like content
            # Call Products.ATContentTypes.content.topic.ATTopic.queryCatalog()
            # method
            # This method handles b_start internally and
            # grabs it from HTTPRequest object
            return self.context.queryCatalog(contentFilter, batch=True)
        else:
            # Folder or Large Folder like content
            # Call CMFPlone(/skins/plone_scripts/getFolderContents Python
            # script This method handles b_start parameter internally and grabs
            # it from the request object
            return self.context.getFolderContents(contentFilter, batch=True, b_size=b_size)

    def __call__(self):
        """ Render the content item listing.
        """

        # How many items is one one page
        limit = 20

        # Limit to gallerypage content type
        filter = { "portal_type" : "collective.gallerypage.gallerypage" }

        start = self.request.get("b_start", 0)

        # Perform portal_catalog query
        self.contents = self.query(start, limit, filter)

        return self.index.render(self) 

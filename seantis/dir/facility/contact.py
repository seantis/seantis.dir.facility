from zope.schema import TextLine

from plone.directives import form
from plone.dexterity.content import Item
from collective.dexteritytextindexer import searchable

from seantis.dir.base.schemafields import Email
from seantis.dir.facility import _


class IContactPerson(form.Schema):
    """ Facility Contact Person """

    searchable('first_name')
    first_name = TextLine(
        title=_(u'First Name'),
    )

    searchable('last_name')
    last_name = TextLine(
        title=_(u'Last Name'),
    )

    searchable('street')
    street = TextLine(
        title=_(u'Street'),
        required=False,
        default=u''
    )

    searchable('zipcode')
    zipcode = TextLine(
        title=_(u'Zipcode'),
        required=False,
        default=u''
    )

    searchable('town')
    town = TextLine(
        title=_(u'Town'),
        required=False,
        default=u''
    )

    searchable('phone')
    phone = TextLine(
        title=_(u'Phone'),
        required=False,
        default=u''
    )

    searchable('fax')
    fax = TextLine(
        title=_(u'Fax'),
        required=False,
        default=u''
    )

    searchable('email')
    email = Email(
        title=_(u'Email'),
        required=False,
        default=u''
    )

    searchable('function')
    function = TextLine(
        title=_(u'Function'),
        required=False,
        default=u''
    )


class ContactPerson(Item):
    @property
    def title(self):
        """Computes the title every time the person is shown."""
        if hasattr(self, 'first_name') and hasattr(self, 'last_name'):
            return u'%s %s' % (self.first_name, self.last_name)
        return u''

    #Dexterity expects this function to be here
    setTitle = lambda self, value: None

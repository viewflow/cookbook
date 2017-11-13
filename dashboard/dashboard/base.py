import warnings

from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import MediaDefiningClass
from django.template.loader import get_template
from django.utils import six, translation
from django.utils.text import slugify


class LayoutNode(six.with_metaclass(MediaDefiningClass, object)):
    """Base class for self-rendered nodes."""

    span_columns = 1
    template_name = None

    def get_template(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "Dasbboard node requires either a definition of "
                "'template_name' or an implementation of 'get_template()'")
        return get_template(self.template_name)

    def get_context_data(self):
        """Additional context data to render node template.
        Subclasses could override it.
        """
        return {
            'parent': self
        }

    def render(self, context, **options):
        with context.push(**self.get_context_data()):
            template = self.get_template()
            return template.render(context.flatten())


class Callable(LayoutNode):
    def __init__(self, handler):
        self.handler = handler

    def render(self, context, **options):
        return self.handler(context)


def _convert_to_nodes(children):
    result = []
    for child in children:
        if isinstance(child, LayoutNode):
            result.append(child)
        elif isinstance(child, (list, tuple)):
            result.append(Row(*child))
        elif callable(child):
            result.append(Callable(child))
        else:
            raise ImproperlyConfigured('Unknown child type {}'.format(child))
    return result


class Row(LayoutNode):
    template_name = 'dashboard/row.html'

    def __init__(self, *children):
        self.children = _convert_to_nodes(children)

    @property
    def media(self):
        """Return all media required to render the element on this dashboard."""
        media = self.media
        for child in self.chipdren:
            media = media + child.media
        return media

    def children_span(self):
        total_span = sum(
            child.span_columns for child in self.children
        )
        if 12 % total_span != 0:
            warnings.warn(
                "Can't equally divide container {} for {} span elements"
                .format(12, self.elements)
            )

        span_multiplier = 12 // total_span
        for child in self.children:
            yield child, child.span_columns * span_multiplier


class Column(LayoutNode):
    template_name = 'dashboard/column.html'

    def __init__(self, *children):
        self.children = _convert_to_nodes(children)

    @property
    def media(self):
        """Return all media required to render the element on this dashboard."""
        media = self.media
        for child in self.chipdren:
            media = media + child.media
        return media


class Dashboard(LayoutNode):
    template_name = 'dashboard/dashboard.html'

    def __init__(self, name, children, permission=None, permission_obj=None):
        self.name = name
        self.children = _convert_to_nodes(children)
        self.permission = permission
        self.permission_obj = permission_obj

    @property
    def slug(self):
        with translation.override('en'):
            return slugify(self.name)

    @property
    def media(self):
        """Return all media required to render the element on this dashboard."""
        media = self.media
        for child in self.chipdren:
            media = media + child.media
        return media

    def has_perm(self, user):
        if self.permission is None:
            return True
        elif self.permission_obj is None:
            return user.has_perm(self.permission)
        elif callable(self.permission_obj):
            pass

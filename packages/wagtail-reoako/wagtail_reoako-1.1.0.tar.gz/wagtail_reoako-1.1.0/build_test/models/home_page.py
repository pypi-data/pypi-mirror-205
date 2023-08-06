from pkg_resources import parse_version
from wagtail import __version__ as WAGTAIL_VERSION

if parse_version(WAGTAIL_VERSION) < parse_version('3.0'):
    from wagtail.core.models import Page
    from wagtail.admin.edit_handlers import StreamFieldPanel
    from wagtail.core.fields import RichTextField
    rich_text_panel = StreamFieldPanel
else:
    from wagtail.models import Page
    from wagtail.admin.panels import FieldPanel
    from wagtail.fields import RichTextField
    rich_text_panel = FieldPanel

class HomePage(Page):
    subpage_types = [
    ]

    content = RichTextField(
        default='',
    )

    content_panels = Page.content_panels + [
        rich_text_panel('content'),
    ]


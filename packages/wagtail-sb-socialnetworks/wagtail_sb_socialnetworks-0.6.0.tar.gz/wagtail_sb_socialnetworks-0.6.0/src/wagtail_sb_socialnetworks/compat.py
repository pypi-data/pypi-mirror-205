try:
    from wagtail.models import Orderable
except ImportError:
    try:
        from wagtail.core.models import Orderable  # type: ignore
    except ImportError:
        from wagtail.admin.edit_handlers import Orderable

try:
    from wagtail.contrib.settings.models import BaseSiteSetting

    class BaseSetting(BaseSiteSetting):
        class Meta:
            abstract = True

except ImportError:
    from wagtail.contrib.settings.models import BaseSetting  # type: ignore


try:
    from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

    ImageChooserPanel = FieldPanel
    SnippetChooserPanel = FieldPanel

except ImportError:
    from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
    from wagtail.images.edit_handlers import ImageChooserPanel  # type: ignore
    from wagtail.snippets.edit_handlers import SnippetChooserPanel  # type: ignore


__all__ = [
    "BaseSetting",
    "FieldPanel",
    "ImageChooserPanel",
    "InlinePanel",
    "MultiFieldPanel",
    "Orderable",
    "SnippetChooserPanel",
]

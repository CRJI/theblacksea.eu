from __future__ import absolute_import, unicode_literals

from django import forms

from wagtail.core.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, \
    CharBlock, RichTextBlock, RawHTMLBlock, BooleanBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from .fields import LinkFields, RelatedLink


class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"

class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width')
    ))

class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock(required=False)
    alignment = ImageFormatChoiceBlock()

class EmbeddedImageBlock(StructBlock):
    image = ImageChooserBlock()
    clickable = BooleanBlock(required=False)
    caption = CharBlock(required=False)

class HalfImageBlock(StructBlock):
    image = ImageChooserBlock()
    h1 = CharBlock(required=False)
    h2 = CharBlock(required=False)
    h3 = CharBlock(required=False)
    text_position = forms.ChoiceField(choices=(
        ('left', 'Left'), ('right', 'Right')
    ), required=False)

class FullImageBlock(StructBlock):
    image = ImageChooserBlock()
    h1 = CharBlock(required=False)
    h2 = CharBlock(required=False)
    h3 = CharBlock(required=False)
    text = RichTextBlock(required=False)
    text_position = forms.ChoiceField(choices=(
        ('left', 'Left'), ('right', 'Right')
    ), required=False)

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"

class ImageGalleryBlock(ListBlock):

    class Meta:
        template = 'blacktail/image_gallery.html'

class StoryStreamBlock(StreamBlock):
    subheadline = CharBlock(icon="title", classname="title")
    embedded_image = EmbeddedImageBlock()
    half_image = HalfImageBlock()
    full_image = FullImageBlock()
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    embed = EmbedBlock(help_text="URL for media to embed")
    document = DocumentChooserBlock(icon="doc-full-inverse")
    image_gallery = ImageGalleryBlock(ImageChooserBlock(label='Image'))

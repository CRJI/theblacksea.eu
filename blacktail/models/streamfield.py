from __future__ import absolute_import, unicode_literals

from django import forms

from wagtail.core.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, \
    CharBlock, RichTextBlock, RawHTMLBlock, BooleanBlock, ListBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Filter
from wagtail.images.shortcuts import get_rendition_or_not_found
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from .fields import LinkFields, RelatedLink


class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"

class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=[
        ('embed', 'Embed'),
        ('medium', 'Medium'),
        ('parallax', 'Parallax'),
    ])

class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(required=False)
    alignment = ImageFormatChoiceBlock()

class EmbeddedImageBlock(StructBlock):
    image = ImageChooserBlock()
    clickable = BooleanBlock(required=False)
    caption = CharBlock(required=False)

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"

class ImageGalleryItemBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(required=False)

class ImageGalleryBlock(ListBlock):

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        if value:
            width = 1110
            img0 = value[0]['image']
            ratio = img0.width / img0.height
            filter = Filter(spec=f'fill-{width}x{int(width/ratio)}')

            context['images'] = [
                (item, get_rendition_or_not_found(item['image'], filter))
                for item in value
            ]
            context['carousel_id'] = f'carousel-{img0.pk}'

        return context

    class Meta:
        template = 'blacktail/image_gallery.html'

class ClassyParagraphClassBlock(FieldBlock):
    field = forms.MultipleChoiceField(choices=[
        ('center', "Center"),
        ('infobox', "InfoBox"),
    ])

class ClassyParagraph(StructBlock):
    text = RichTextBlock()
    cls = ClassyParagraphClassBlock(label="class")

class StoryStreamBlock(StreamBlock):
    subheadline = CharBlock(icon="title", classname="title")
    embedded_image = EmbeddedImageBlock()
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    classy_paragraph = ClassyParagraph(icon="pilcrow")
    image = ImageBlock(label="Image", icon="image")
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    embed = EmbedBlock(help_text="URL for media to embed")
    document = DocumentChooserBlock(icon="doc-full-inverse")
    image_gallery = ImageGalleryBlock(ImageGalleryItemBlock)

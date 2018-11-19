from django.utils.html import format_html
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from wagtail.core import hooks
from wagtail.core.models import Orderable, Page
from wagtail.images import formats
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Author
from .models import StoryType
from .models import StoryDossier
from .models import BlogCategory


@hooks.register('insert_editor_css')
def editor_css():
    css = format_html('<link rel="stylesheet" href="' + settings.STATIC_URL + 'css/editorhacks.css">')
    css += format_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/css/select2.min.css">')
    return css


@hooks.register('insert_editor_js')
def editor_js():
    js = format_html('<script src="' + settings.STATIC_URL + 'js/editorhacks.js"></script>')
    return js


@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.6-rc.0/js/select2.min.js"></script>'
    )


@hooks.register('construct_explorer_page_queryset')
def show_more_properties(parent_page, pages, request):
    print(pages[0])
    # if parent_page.slug == 'user-profiles':
    #     pages = pages.filter(owner=request.user)

    return pages


@hooks.register('register_rich_text_features')
def register_image_feature(features):
    formats.unregister_image_format('fullwidth')
    formats.unregister_image_format('left')
    formats.unregister_image_format('right')
    formats.register_image_format(formats.Format('fullwidth', _('Full width'), 'richtext-image full-width', 'max-1600x800'))
    formats.register_image_format(formats.Format('left', _('Left-aligned'), 'richtext-image left', 'max-1000x500'))
    formats.register_image_format(formats.Format('right', _('Right-aligned'), 'richtext-image right', 'max-1000x500'))


class AuthorModelAdmin(ModelAdmin):
    model = Author
    menu_label = 'Authors'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'occupation', 'email', 'url')
    list_filter = ('occupation',)
    search_fields = ('name', 'bio', 'occupation', 'email', 'url')


class StoryTypeModelAdmin(ModelAdmin):
    model = StoryType
    menu_label = 'Story types'
    menu_icon = 'folder'
    menu_order = 201  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name',)
    search_fields = ('name',)


class StoryDossierModelAdmin(ModelAdmin):
    model = StoryDossier
    menu_label = 'Story dossiers'
    menu_icon = 'folder-open-1'
    menu_order = 202  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name',)
    search_fields = ('name',)


class BlogCategoryModelAdmin(ModelAdmin):
    model = BlogCategory
    menu_label = 'Blog categories'
    menu_icon = 'folder-open-1'
    menu_order = 203  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'color')
    search_fields = ('name', 'color')


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(AuthorModelAdmin)
modeladmin_register(StoryTypeModelAdmin)
modeladmin_register(StoryDossierModelAdmin)
modeladmin_register(BlogCategoryModelAdmin)

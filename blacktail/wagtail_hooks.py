from django.utils.html import format_html
from django.conf import settings

from wagtail.wagtailcore import hooks

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import Author
from .models import StoryType
from .models import StoryDossier

# @hooks.register('insert_editor_css')
# def editor_css():
#     return format_html('<link rel="stylesheet" href="' + settings.STATIC_URL + 'blacktail/css/admin-streamfield-styles.css">')

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

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(AuthorModelAdmin)
modeladmin_register(StoryTypeModelAdmin)
modeladmin_register(StoryDossierModelAdmin)

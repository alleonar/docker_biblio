from django.contrib import admin
from django.utils.html import format_html
from backoffice.models import Authors, Publishers, Titles, Reservation

# Register your models here.
admin.site.register(Authors)
admin.site.register(Publishers)


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover_preview')

    def cover_preview(self, obj):
        if obj.cover and obj.cover != '':
            return format_html('<img src="{}" style="width: 50px; height: auto;">', obj.cover.url)
        return format_html('<img src="{}" style="width: 50px; height: auto;">', '/media/images/nocover.jpg')
    
    cover_preview.short_description = "aperçu de l'image"

admin.site.register(Titles, TitlesAdmin)

class ReservationsAdmin(admin.ModelAdmin):
    list_filter = ('user', 'title', 'close')
admin.site.register(Reservation, ReservationsAdmin)
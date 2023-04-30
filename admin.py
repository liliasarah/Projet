from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.
class ProduitAdmin(admin.ModelAdmin):
    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50"/>'.format(obj.image.url))
    display_image.short_description = 'Image'

    list_display = ('nom', 'display_image', 'prix')
    list_filter = ('categorie',)
    search_fields = ('nom',)

class CommandeAdmin(admin.ModelAdmin):
    list_display = ('produit', 'client', 'quantite', 'wilaya')
    search_fields = ('produit__nom',)
    list_filter = ('wilaya',)
    
class LivraisonAdmin(admin.ModelAdmin):
    def commandes(self, obj):
        s = 0
        for c in obj.commande.all():
            s += 1
        return s
    list_display = ('commandes', 'valide', 'prix_total', 'adresse_livraison', 'date_livraison')
    list_filter = ('date_livraison',)
    list_display_links = ('commandes', 'prix_total')



admin.site.register(Livraison, LivraisonAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Wishlist)
admin.site.register(Cart)








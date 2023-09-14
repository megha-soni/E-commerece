from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Product,Cart,ItemModel
admin.site.register(Product)
admin.site.register(ItemModel)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

class sessionAdmin(admin.ModelAdmin):
    def _session_data(self,obj):
        return obj.get_decoded()
    list_display=['session_key','_session_data','expire_date']
admin.site.register(Session,sessionAdmin)

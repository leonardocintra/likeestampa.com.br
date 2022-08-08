from django.contrib.admin import AdminSite


class LikeEstampaSite(AdminSite):
    AdminSite.site_header = 'Like Estampa Administrativo'
    AdminSite.index_title = 'Administração Like Estampa'
    AdminSite.site_title = 'Like Estampa'

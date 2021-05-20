from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"

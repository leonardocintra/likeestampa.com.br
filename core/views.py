from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"

class TrocaCancelamentoView(TemplateView):
    template_name = "troca-e-cancelamento.html"

class TermosDeUsoView(TemplateView):
    template_name = "termos-de-uso.html"
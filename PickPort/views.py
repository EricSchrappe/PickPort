from django.views.generic import TemplateView

class IndexView(TemplateView):
	template_name = 'index.html'

class SuccessPage(TemplateView):
	template_name = 'successful_login.html'

class ThanksPage(TemplateView):
	template_name = 'thanks.html'
		
		
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from braces.views import SelectRelatedMixin

from django.views import generic, View
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

from categories.models import Category, CategorySubscriber, CategoryLike, CategoryContributor
from items.models import Items

# Create your views here.

class CreateCategoryView(LoginRequiredMixin, generic.edit.CreateView):
	fields = ('name', 'description')
	model = Category

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()

		return super().form_valid(form)

class ListCategoryView(generic.ListView):
	model = Category
	

	def get_context_data(self, **kwargs):
		latest = Category.objects.order_by('-created_date')[:5]
		most_likes = Category.objects.annotate(num_likes = Count('likes')).order_by('-num_likes')[:5]
		context = super().get_context_data(**kwargs)
		context['latest_cat'] = latest
		context['most_likes'] = most_likes

		return context


class UserListCategoryView(LoginRequiredMixin, generic.ListView):
	model = Category
	template_name = 'categories/category_user_list.html'

	def get_queryset(self):
		#Processing the queryset
		queryset = super().get_queryset()
		return queryset.filter(user_id=self.request.user.id)

class SubListCategoryView(LoginRequiredMixin, generic.ListView):
	model = Category
	template_name = 'categories/category_sub_list.html'
	context_object_name = 'category_sub_list'

	def get_queryset(self):
		queryset = super().get_queryset()

		return queryset.filter(subscribers=self.request.user.id)

class DetailCategoryView(LoginRequiredMixin, generic.DetailView):
	model = Category


class UpdateCategoryView(LoginRequiredMixin, generic.edit.UpdateView):
	model = Category
	fields = ['name', 'description']
	template_name_suffix = '_update_form'

	def get_success_url(self):
		return reverse_lazy('categories:userlist', kwargs={'pk': self.request.user.id})

class DeleteCategoryView(LoginRequiredMixin, generic.edit.DeleteView):
	model = Category
	
	def get_success_url(self):
		return reverse_lazy('categories:userlist', kwargs={'pk': self.request.user.id})

class SearchCategoryView(View):
	template_name = 'categories/category_search_results.html'

	def get_queryset(self):
		queryset = Category.objects.order_by('name')
		
		return queryset

	def post(self, request):
		cats = self.get_queryset()
		result = cats.filter(name__contains=request.POST['search_name'])

		return render(request, self.template_name, {'result': result})


class SubCategoryView(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		return reverse('categories:single', kwargs={'slug': self.kwargs.get('slug')})

	def get(self, request, *args, **kwargs):

		cat = get_object_or_404(Category, slug=self.kwargs.get('slug'))

		try:
			CategorySubscriber.objects.create(user=self.request.user, category=cat)

		except IntegrityError:
			messages.warning(self.request, "Warning, already subscriber of {} category".format(cat.name))

		else:
			messages.success(self.request, "You are successfully subscribed to the {} category".format(cat.name))

		return super().get(request, *args, **kwargs)

class UnSubCategoryView(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		return reverse('categories:single', kwargs={'slug': self.kwargs.get('slug')})

	def get(self, request, *args, **kwargs):

		try:
			sub = CategorySubscriber.objects.filter(user=self.request.user, category__slug=self.kwargs.get('slug')).get()

		except CategorySubscriber.DoesNotExist:
			messages.warning(self.request, "You aren`t even a subscriber")

		else:
			sub.delete()
			messages.success(self.request, 'You successfully unsubscribed to')

		return super().get(request, *args, **kwargs)

class LikeCategoryView(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		return reverse('categories:single', kwargs={'slug': self.kwargs.get('slug')})

	def get(self, request, *args, **kwargs):

		cat = get_object_or_404(Category, slug=self.kwargs.get('slug'))

		try:
			CategoryLike.objects.create(user=self.request.user, category=cat)

		except IntegrityError:

			messages.warning(self.request, 'You already liked this category')

		else:

			messages.success(self.request, 'You liked this category')

		return super().get(request, *args, **kwargs)


class UnLikeCategoryView(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		return reverse('categories:single', kwargs={'slug': self.kwargs.get('slug')})

	def get(self, request, *args, **kwargs):

		try:
			like = CategoryLike.objects.filter(user= self.request.user, category__slug=self.kwargs.get('slug')).get()

		except CategoryLike.DoesNotExist:

			messages.warning(self.request, 'You didn`t even liked the category')

		else:
			like.delete()
			messages.success(self.request, 'You removed your like now')

		return super().get(request, *args, **kwargs)

class RequestContribView(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		return reverse('categories:single', kwargs={'slug': self.kwargs.get('slug')})

	def get(self, request, *args, **kwargs):
		cat = get_object_or_404(Category, slug=self.kwargs.get('slug'))

		try:
			CategoryContributor.objects.create(user=self.request.user, category=cat)

		except IntegrityError:

			messages.warning(self.request, "You already ask to be a contributor")

		else:

			messages.success(self.request, 'You successfully requested to be a contributor')

		return super().get(request, *args, **kwargs)

class RequestListContribView(LoginRequiredMixin, generic.ListView):
	model = Category
	template_name = 'categories/category_requested_contrib.html'
	context_object_name = 'requested_contribs'

	def get_queryset(self):
		queryset = super().get_queryset()
		current_user_cats = queryset.filter(user = self.request.user.id)
		usr = User.objects.filter(id__in=current_user_cats.values_list('contributors', flat=True))
		
		usr_status_dict = {}

		for u in usr:

			usr_status_dict[u] = u.user_contrib.values_list('approved', flat=True)[0]

		return usr_status_dict

class ApproveContribView(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self, **kwargs):
		return reverse('categories:contriblist', kwargs={'pk': self.kwargs.get('owner')})

	def get(self, request, *args, **kwargs):

		contrib_usr = get_object_or_404(CategoryContributor, user=self.kwargs.get('pk'))

		if contrib_usr.approved == False:
			contrib_usr.approved = True
			contrib_usr.save()
			messages.success(self.request, "Successfully approved")

		else:
			messages.warning(self.request, "You already approved this request")			


		return super().get(request, *args, **kwargs)

class RemoveContribView(LoginRequiredMixin, generic.RedirectView):

	def get_redirect_url(self, **kwargs):
		return reverse('categories:contriblist', kwargs={'pk': self.kwargs.get('owner')})

	def get(self, request, *args, **kwargs):

		contrib_usr = get_object_or_404(CategoryContributor, user=self.kwargs.get('pk'))

		if True:
			contrib_usr.delete()
			messages.success(self.request, 'Successfully declined')
			
		elif contrib_usr.DoesNotExist:
			messages.warning(self.request, 'You already declined the request')
			

		return super().get(request, *args, **kwargs)


class TestView(generic.ListView):
	model= CategoryLike
























from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.contrib.auth import get_user_model
User = get_user_model()

from items.models import Items
from items.forms import ItemForm
from categories.models import Category


# Create your views here.
'''
class ItemCreateView(LoginRequiredMixin, SelectRelatedMixin, CreateView):
	fields = ('name',)
	model = Items
	#select_related = ('user', 'category')

	def getCat(request, id):
		return Category.objects.get(id=id)


	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.category_id = self.getCat(id)
		self.object.save()

		return super().form_valid(form)
'''

@login_required
def CreateItem(request, pk):
	cat = get_object_or_404(Category, pk=pk)

	if request.method == 'POST':

		form = ItemForm(request.POST)

		if form.is_valid():
			item = form.save(commit=False)
			item.category = cat
			item.user = request.user
			item.save()

			return redirect('categories:single', slug=cat.slug)

	else:

		form = ItemForm()

	return render(request, 'items/items_form.html', {'form': form, 'cat': cat })

@login_required
def DeleteItem(request, pk):
	item = get_object_or_404(Items, pk=pk)

	#POST request
	if request.method == 'POST':
		#confirming delete
		item.delete()

		return redirect('categories:single', slug=item.category.slug)

	return render(request, 'items/items_confirm_delete.html', {'object': item})

@login_required
def UpdateItem(request, pk):
	item = get_object_or_404(Items, pk=pk)
	cat_id = item.category

	form = ItemForm(request.POST or None, instance=item)

	if form.is_valid():
		item = form.save(commit=False)
		item.category = cat_id
		item.user = request.user
		item.save()

		return redirect('categories:single', slug=item.category.slug)


	return render(request, 'items/items_update_form.html', {"form": form, 'cat': cat_id })

@login_required
def ShuffleItem(request, pk):
	item_list = Items.objects.filter(category__pk=pk)
	cat = get_object_or_404(Category, pk=pk)

	if request.method == 'POST':
		item_list = item_list.order_by('?')[:int(request.POST['number'])]

		return render(request, 'items/items_shuffle.html', {'item_list': item_list, 'cat': cat})	


	



















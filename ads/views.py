from django.http import request
from .models import Ad, Comment, Fav
from .owner import OwnerCreateView, OwnerDeleteView, OwnerDetailView, OwnerListView, OwnerUpdateView
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy, reverse
from .forms import CommentForm, CreateForm
from django.contrib.humanize.templatetags.humanize import naturaltime
from ads.utils import dump_queries
from django.db.models import Q, query
from taggit.models import Tag



class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"

    def get(self, request):
        srchval = request.GET.get("search", False)
        favorites = list()

        if request.user.is_authenticated:
            rows = request.user.favorite_ads.values('id')

            favorites = [row['id'] for row in rows]

        if srchval:
            query = Q(title__icontains=srchval) | Q(text__icontains=srchval)
            ad_list = Ad.objects.filter(query).select_related().order_by("-updated_at")
            
        else:
            ad_list = Ad.objects.all().order_by("-updated_at")

        for ad in ad_list:
            ad.natural_updated = naturaltime(ad.updated_at)

        ctx = {'ad_list': ad_list, 'favorites': favorites, 'search': srchval}
        return render(request, self.template_name, ctx)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    def get(self, request, pk):
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad':x, 'comments': comments, 'comment_form':comment_form}
        return render (request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all') 

    def get(self, request):
        form = CreateForm()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = self.request.user
            ad.save()
            form.save_m2m()
            return redirect(self.success_url)
        ctx = {'form':form}
        return render(request, self.template_name, ctx)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form':form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = self.request.user
            ad.save()
            form.save_m2m()
            return redirect(self.success_url)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)
    

class AdDeleteView(OwnerDeleteView):
    model = Ad


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response



class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/ad_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

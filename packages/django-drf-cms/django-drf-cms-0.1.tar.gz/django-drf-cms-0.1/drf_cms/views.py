from django.shortcuts import render
from rest_framework import generics, mixins
from .models import Text
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from cms.shortcuts import get_current_site


class TextView(
		mixins.ListModelMixin, 
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin,
		generics.GenericAPIView):
	serializer_class = TextSerializer
	permission_classes = [IsOwnerOrReadOnly]
	lookup_field = 'key'

	def get_queryset(self):
		page_key = self.kwargs.get('page_key')
		site = get_current_site(self.request)
		return Text.objects.filter(page__key=page_key, page__site=site)

	def get(self, request, *args, **kwargs):
		key = self.kwargs.get('key')
		if (key):
			return self.retrieve(request, *args, **kwargs)
		return self.list(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)



class PageView(
		mixins.ListModelMixin,
		mixins.RetrieveModelMixin,
		generics.GenericAPIView):
	serializer_class = PageSerializer
	permission_classes = [IsOwnerOrReadOnly]
	lookup_field = 'key'

	def get_queryset(self):
		site = get_current_site(self.request)
		return Page.objects.filter(site=site)

	def get(self, request, *args, **kwargs):
		key = self.kwargs.get('key')
		if (key):
			return self.retrieve(request, *args, **kwargs)
		return self.list(request, *args, **kwargs)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from models import Version, Configuracion, TituloValor, Estado

'''
def get_version(request):
	if request.is_ajax():
		if request.method == 'GET':
			req = request.GET

'''

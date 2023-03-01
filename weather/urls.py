from django.urls import path
from . import views

urlpatterns = [
	path(' ', views.index),
	path('url-fetch-data/',views.word_frequencies),
	path('integer-data/',views.integer_data),
]

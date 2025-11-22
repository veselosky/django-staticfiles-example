from django.shortcuts import render

def home(request):
	"""Render a simple home page demonstrating the `static` template tag."""
	return render(request, "home.html")

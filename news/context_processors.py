from django.shortcuts import render
from news.models import Category


def categories(request):
    category_list = Category.objects.all()
    return {"categories": category_list}


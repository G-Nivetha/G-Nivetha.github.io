import random
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from . import util

class SearchEntry(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}))

class CreateEntry(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={"placeholder": "Article Content using Github Markdown"}))

class EditEntry(forms.Form):
    rename = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={"placeholder": "Rename (optional)"}))
    text = forms.CharField(label='', widget=forms.Textarea())

class DeleteEntry(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Delete Article"}))


def index(request):

    if not util.list_entries():
        return render(request, "encyclopedia/error.html")
    elif request.method == "POST":

        form = DeleteEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            util.delete_entry(title)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"encyclopedia/index.html",{
                "form": form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "titles": util.list_entries(),
            "search_entry": SearchEntry(),
            "delete_entry": DeleteEntry()
        })

def entry(request, title):

    entry_mdfile = util.get_entry(title)

    if entry_mdfile != None:
        entry_html = Markdown().convert(entry_mdfile)
        return render(request, "encyclopedia/entry.html", {
          "title": title,
          "entry": entry_html,
          "search_entry": SearchEntry(),
          })
    else:
        related_titles = util.related_entries(title)
        return render(request, "encyclopedia/error.html", {
          "title": title,
          "titles": util.list_entries(),
          "related_titles": related_titles,
          "search_entry": SearchEntry(),
          })

def search(request):

    if request.method == "POST":
        form = SearchEntry(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_mdfile = util.get_entry(title)

            if entry_mdfile:
                return redirect(reverse('entry', args=[title]))

            else:
                related_titles = util.related_entries(title)

                return render(request, "encyclopedia/search.html", {
                "title": title,
                "related_titles": related_titles,
                "search_entry": SearchEntry()
                })

    return HttpResponseRedirect(reverse("index"))

def create(request):

    if request.method == "POST":
        form = CreateEntry(request.POST)

        if form.is_valid():
          title = form.cleaned_data['title']
          text = form.cleaned_data['text']
        else:
          messages.error(request, 'Entry form not valid, please try again!')
          return render(request, "encyclopedia/create.html", {
            "create_entry": form,
            "search_entry": SearchEntry()
          })

        if util.get_entry(title):
            messages.error(request, 'This article already exists! Please go to that article page and edit it instead!')
            return render(request, "encyclopedia/create.html", {
              "create_entry": form,
              "search_entry": SearchEntry()
            })
        else:
            util.save_entry(title, text)
            messages.success(request, f'New article "{title}" created successfully!')
            return redirect(reverse('entry', args=[title]))

    else:
        return render(request, "encyclopedia/create.html", {
          "create_entry": CreateEntry(),
          "search_entry": SearchEntry()
        })

def edit(request,title):
    if request.method == "GET":
        text = util.get_entry(title)

        if text == None:
            messages.error(request, f'No article exist in the name - "{title}" , please create a new article instead!')
            return HttpResponseRedirect(reverse("create"))
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_entry": EditEntry(initial={'text':text}),
            "search_entry": SearchEntry()
        })

    elif request.method == "POST":
        form = EditEntry(request.POST)

        if form.is_valid():
            rename = form.cleaned_data['rename']
            text = form.cleaned_data['text']
            if rename :
                util.delete_entry(title)
                util.save_entry(rename, text)
                messages.success(request, f'Article "{title}" is renamed as "{rename}" and updated successfully!')
                return redirect(reverse('entry', args=[rename]))

            else:
                util.save_entry(title, text)
                messages.success(request, f'Article "{title}" updated successfully!')
                return redirect(reverse('entry', args=[title]))

        else:
          messages.error(request, f'Invalid, please try again!')
          return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_entry": form,
            "search_entry": SearchEntry()
          })



def random_entry(request):
    titles = util.list_entries()
    title = random.choice(titles)

    return redirect(reverse('entry', args=[title]))
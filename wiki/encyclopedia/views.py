from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown2

class searchform(forms.Form):
    query = forms.CharField()

class CTform(forms.Form):
    title = forms.CharField(label="TITLE")
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Content Here', 'rows': 18, 'cols': 90}), label='')

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 23, 'cols': 92}), label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    }) 

def entry_page(request, title):
    single_entry = util.get_entry(title)
    if single_entry is None:
        return  render(request, "encyclopedia/error.html", {
            "message": "Page Not Found"
            })
    else:
        html_content = markdown2.markdown(single_entry)
        return render(request, "encyclopedia/entry.html", {
            "single_entry": html_content,
            "title": title
            })


def search(request):
    if request.method == "POST":
        form = searchform(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            single_entry = util.get_entry(query)
            if single_entry is None:
                all_entries = util.list_entries()

                partial_matches = []
                for entry in all_entries:
                    if query.lower() in entry.lower():
                        partial_matches.append(entry)
                if partial_matches:
                    return render(request, "encyclopedia/search_results.html", {
                        "partial_matches": partial_matches
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "message": "Page Not Found!"
                    })
            else:
                html_content = markdown2.markdown(single_entry)
                return render(request, "encyclopedia/entry.html", {
                    "single_entry": html_content,
                    "title": query
                })
    else:
        return render(request, "encyclopedia/layout.html", {
            "form": searchform()
        })
    
def create_page(request):
    if request.method == "POST":
        form = CTform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            created = util.get_entry(title)
            if created is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry_page", args=[title]))
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "A Page With That Title Already Exist!"
                })
    return render(request, "encyclopedia/create.html", {
        "form": CTform()
    })

def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content'].replace('\r', '')
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry_page", args=[title]))
    else:
        form = EditForm(initial={'content': content})
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def random_page(request):
    every_entry = util.list_entries()
    random_entry = random.choice(every_entry)
    if random_entry is not None:
        return HttpResponseRedirect(reverse("entry_page", args=[random_entry]))
    return render(request, "encyclopedia/layout.html")

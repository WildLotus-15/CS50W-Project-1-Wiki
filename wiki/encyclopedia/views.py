from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}) ,max_length=24)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', "rows": 10}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markDowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonExisting.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markDowner.convert(entryPage),
            "entryTitle": entry
        })


def search(request):
    value = request.GET.get('q', '')
    if util.get_entry(value) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": value}))
    else:
        subStringQuery = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringQuery.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": subStringQuery,
            "search": True,
            "value": value
        })

def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form": form,
                    "existingEntry": True,
                    "entry": title
                })
        else: 
            return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "existingEntry": False
            })

    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm()
        })

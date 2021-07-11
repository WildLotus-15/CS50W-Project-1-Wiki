from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse


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

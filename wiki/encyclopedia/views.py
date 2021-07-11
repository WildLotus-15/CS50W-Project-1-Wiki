from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markDowner = Markdown()
    entryPage = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": markDowner.convert(entryPage),
        "entryTitle": entry
    })
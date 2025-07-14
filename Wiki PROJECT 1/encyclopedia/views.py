from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
from django.urls import reverse
import sys
import random


def conversion(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = conversion(title)
    if html is None:
        return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "message": "This content does not exist.",
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html,
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html = conversion(entry_search)
        if html is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html
            })
        else:
            entries = util.list_entries()
            recommendation = [entry for entry in entries if entry_search.lower() in entry.lower()]
            if recommendation:
                return render(request, "encyclopedia/search.html", {
                    "recommendation": recommendation  
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "text": "Error",
                    "message": "Entry not found or does not exist."
                })
            
def create(request):
    if request.method == "GET":
        return render(request,"encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        exists = util.get_entry(title)
        if exists is not None:
            return render(request,"encyclopedia/error.html",{
                "message": "This entry already exists."
            })
        else:
            util.save_entry(title,content)
            html = conversion(title)
            return render(request,"encyclopedia/entry.html",{
                "title": title,
                "content": html
            })
def edit(request):
    print(reverse("edit"), file=sys.stderr)
    if request.method == 'POST':
        title=request.POST['e_title']
        content=util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title":title,
            "content":content
        })
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']    
        util.save_entry(title,content)
        html = conversion(title)
        return render(request,"encyclopedia/entry.html",{
                "title": title,
                "content": html
        })
def choice(request):
    entries = util.list_entries()
    choice_entry = random.choice(entries)
    html = conversion(choice_entry)
    return render(request, "encyclopedia/entry.html",{
        "title":choice_entry,
        "content":html
    })
def delete(request, title):
    util.delete_entry(title)
    return redirect('index')

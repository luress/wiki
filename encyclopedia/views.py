from re import X
from django.http.response import HttpResponseRedirect
import markdown as md
import random
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms.fields import CharField
from django import forms


from . import util

class NewTitleForm(forms.Form):
    new_title = CharField(label="New Title")
    title_content = CharField(label="Write an article", widget=forms.Textarea)

class ChangeTitle(forms.Form):
    change_form = CharField(label="Change title")
    form_content = CharField(label="Write an article", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request):
    return render(request, "encyclopedia/wiki.html")

def fail(request):
    return(render(request, "encyclopedia/fail.html"))

def create(request):
    if request.method == "POST":
        form = NewTitleForm(request.POST)
        form_content = NewTitleForm(request.POST)
        if form.is_valid() and form_content.is_valid():
            tit = form.cleaned_data["new_title"]
            content = form_content.cleaned_data["title_content"]
            util.save_entry(tit, content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/create.html",{
                "form" : form
            })

    return render(request, "encyclopedia/create.html",{
        "form" : NewTitleForm(),
    })



def change(request, name):
    body_content = ChangeTitle(request.POST)
    form_change = ChangeTitle(request.POST)
    form = ChangeTitle(initial={'change_form': f"{name}", 'form_content' : util.get_entry(f"{name}")})
    if form_change.is_valid() and body_content.is_valid():
        tit = body_content.cleaned_data["change_form"]
        content = form_change.cleaned_data["form_content"]
        util.save_entry(tit, content)
        return HttpResponseRedirect(reverse(f"encyclopedia:index"))
    return render(request, "encyclopedia/change.html", {
        "form": form,
    })

def chan(request):
    return render(request, "encyclopedia/chan.html")

def title(request, name):
    if not util.get_entry(f"{name}"):
        return HttpResponseRedirect(reverse("encyclopedia:fail"))
    return render(request, "encyclopedia/title.html", {
        "bod" : md.markdown(util.get_entry(f"{name}")),
        "name" : name.capitalize()
    })

def random_choice(request):
    titles = util.list_entries()
    random_title = random.choice(titles)
    return render(request, "encyclopedia/title.html", {
        "bod" : md.markdown(util.get_entry(f"{random_title}")),
        "name" : random_title.capitalize()
    })
    
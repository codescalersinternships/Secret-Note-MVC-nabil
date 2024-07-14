from django.shortcuts import render
from django.http import HttpResponse
from secretnote.models import Note
from datetime import datetime
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone



@csrf_exempt
def createNote(request):
    isDone = True
    msg = []
    if(request.method == "POST"):
        data = request.POST
        text = data.get("text")
        if not text:
            msg.append("no text provided")
            isDone = False
        maxVisit = data.get("maxVisit")
        if not maxVisit:
            msg.append("no maximum number of visits provieded")
            isDone = False
        expireDate = data.get("expireDate")
        if not expireDate:
            msg.append("no expire date provided")
            isDone = False
        if ( isDone):
            note = Note(note_text = text, note_remvisit = maxVisit, expiry_date = datetime.strptime(expireDate, '%Y-%m-%d').date())
            note.save()
            link = request.build_absolute_uri(f"/secretnote/{str(note.note_url)}")
            return render(request, "secretnote/noteView.html",{"note": note, "link":link})
    return render(request, "secretnote/index.html",{"msg":msg})

@csrf_exempt
def retrieveNote(request, id):
    note = get_object_or_404(Note, note_url=id)
    note.note_remvisit-=1
    note.save()
    if (note.note_remvisit<=0 or timezone.now() >= note.expiry_date):
        note.delete()
        return render(request, "secretnote/index.html",{"msg":["note is expired or not found"]})
    link = request.build_absolute_uri(f"/secretnote/{str(note.note_url)}")
    return render(request, "secretnote/noteView.html", {"note": note, "link":link})


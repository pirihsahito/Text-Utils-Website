from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def analyze(request):
    # Get the text using POST
    djtext = request.POST.get('text', 'default')

    # Check box values
    removepunc = request.POST.get('removepunc', 'off')
    allcaps = request.POST.get('allcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charcounter = request.POST.get('charcounter', 'off')

    purpose = []
    char_count = None
    analyzed = djtext

    # Check which checkbox is on
    if removepunc == "on":
        punctuations = '''!()-{}[]—;:'"\,<>./?@#$%^&*_...~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        purpose.append('Removed Punctuations')
        djtext = analyzed

    if allcaps == "on":
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()
        purpose.append('Changed to uppercase')
        djtext = analyzed

    if newlineremover == "on":
        analyzed = ""
        for char in djtext:
            if char != "\n" and char != "\r":
                analyzed = analyzed + char
        purpose.append('New Line Removed')
        djtext = analyzed

    if extraspaceremover == "on":
        analyzed = ""
        for index, char in enumerate(djtext):
            if index + 1 < len(djtext):
                if djtext[index] == " " and djtext[index + 1] == " ":
                    continue  # Skip this extra space
                else:
                    analyzed = analyzed + char
            else:
                analyzed = analyzed + char
        purpose.append('Extra Space Removed')
        djtext = analyzed

    if charcounter == "on":
        char_count = 0
        for char in djtext:
            if char != " ":
                char_count = char_count + 1
        purpose.append('Characters Counted (No Spaces)')

    if removepunc != "on" and allcaps != "on" and newlineremover != "on" and extraspaceremover != "on" and charcounter != "on":
        return HttpResponse("Please select any operation and try again")
    
    # Pack everything safely into the final context object
    params = {
        'purpose': ", ".join(purpose), 
        'analyzed_text': analyzed,
        'character_count': char_count
    }

    return render(request, 'analyze.html', params)
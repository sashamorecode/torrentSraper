from django.shortcuts import render
from a_search.Scraper import metaFinder
from a_search.models import MagnetLink

# Create your views here.

finder = metaFinder()

def search_view(request):

    try:
        searchTerm = request.GET['searchTerm']
        resCount = int(request.GET['resCount'])
        assert searchTerm.rstrip() != ""
    except:
        return render(request, "index.html", {"magnetUrls": []})
    
    magnetUrls, magnetNames = getMagnet(searchTerm, resCount)
    magnets = dict(zip(magnetNames, magnetUrls))
    return render(request, "index.html", {"magnets": magnets, "userSearch": " for " + searchTerm})

def getMagnet(searchTerm, resCount):
    localMagnets = MagnetLink.objects.filter(magnetName__contains=searchTerm)
    if localMagnets and 2*len(localMagnets) > resCount: #rescount is number or res per site so we mutl by 2 to account for duplicates
        magnetUrls = [magnet.magnetUrl for magnet in localMagnets]
        magnetNames = [magnet.magnetName for magnet in localMagnets]
        return magnetUrls[:min(resCount,len(magnetUrls)-1)], magnetNames[:min(resCount,len(magnetNames)-1)]

    magnetUrls, magnetNames = finder.query(searchTerm, resCount)
    for i in range(len(magnetUrls)):
        magnet = MagnetLink(magnetName=magnetNames[i], magnetUrl=magnetUrls[i])
        magnet.save()   
    return magnetUrls, magnetNames
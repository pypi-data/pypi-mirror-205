import requests
from .config import *
import treelib as tl

def isEmpty(x):

    funcname = '[isEmpty]: '
    try:
        if type(x).__name__ in ['list', 'ndarray', 'str']:
            if len(x): return 0
            else: return 1
        elif type(x).__name__ == 'NoneType': return 1
        else: return 0
    except NameError: return 1

def sanitize(id):

    if '&' in id: new_id = id.replace('&', '%26')
    else: new_id = id
    return new_id

def getArticle(id):

    """
    Gets an article and all its desired properties
    """

    headers = {'Authorization':'Bearer {token}'.format(token=ads_token)}
    url = generalQuery.format(id=sanitize(id))
    r = requests.get(url, headers=headers)
    rjson = r.json()
    if 'error' in list(rjson.keys()):
        print('Error occurred: {err}'.format(err=rjson['error']))
        exit()
    
    paper_attrs = rjson['response']['docs'][0]

    return paper_attrs

def getAllReferences(id): 

    """
    Get all references of an article
    Simple wrapper
    Returns a list of article ids referenced by the article id in argument
    """
    
    try: referenceList = getArticle(id)['reference']
    except KeyError:
        # This is probably because the ADS can not resolve the author-supplied tex.
        # Searching for this entry on the web ADS would probably show a greyed-out References section.  
        referenceList = [None]
    return referenceList
        
def getAllCitations(id): 

    """
    Get all citations of an article
    Simple wrapper
    Returns a list of article ids which cited the article id in argument
    """
    
    try: citeList = getArticle(id)['citation']
    except KeyError: citeList = [None]
    return citeList

def getTitle(id): 
    if id is not None: return getArticle(id)['title'][0]
    else: return 'None'
            



    




    
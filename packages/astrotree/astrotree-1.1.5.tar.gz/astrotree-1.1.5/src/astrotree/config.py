import os

ads_token = os.environ['ADSTOKEN']
generalQuery = 'https://api.adsabs.harvard.edu/v1/search/query?q=bibcode:{id}&fl=author,year,id,doi,arxiv_class,title,abstract,reference,citation'
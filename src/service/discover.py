import requests
from os import getenv
from dotenv import find_dotenv, load_dotenv
import requests
load_dotenv(find_dotenv())

DISCOVER_HOST = getenv('DISCOVER_HOST')
DISCOVER_SUBSCRIPTION_KEY = getenv('DISCOVER_SUBSCRIPTION_KEY')

def getAllCategories():
    url = f"{DISCOVER_HOST}/categories"

    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': DISCOVER_SUBSCRIPTION_KEY,
        'Accept-Language': 'en',
        'CategoryVersion': 'sui'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def getCategoryTree(category, language = 'en', version = 'sui'):
    url = f"{DISCOVER_HOST}/categories/{category}/tree"

    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': DISCOVER_SUBSCRIPTION_KEY,
        'Accept-Language': language,
        'CategoryVersion': version
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def getTypesTree(language = 'en'):
    url = f"{DISCOVER_HOST}/types/tree"

    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': DISCOVER_SUBSCRIPTION_KEY,
        'Accept-Language': language
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def getAmenityFeatures(language = 'en'):
    url = f"{DISCOVER_HOST}/amenities"

    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': DISCOVER_SUBSCRIPTION_KEY,
        'Accept-Language': language
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()
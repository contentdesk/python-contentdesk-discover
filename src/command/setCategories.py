import json
import sys
sys.path.append("..")

from service.discover import getCategoryTree
from akeneo.akeneo import Akeneo
from os import getenv
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

AKENEO_HOST = getenv('AKENEO_HOST')
AKENEO_CLIENT_ID = getenv('AKENEO_CLIENT_ID')
AKENEO_CLIENT_SECRET = getenv('AKENEO_CLIENT_SECRET')
AKENEO_USERNAME = getenv('AKENEO_USERNAME')
AKENEO_PASSWORD = getenv('AKENEO_PASSWORD')


def setCategories(category, parentCategory = None, akeneoCategories = {}, language = 'en_US'):
    # check if category is a list
    if isinstance(category, list):
        for cat in category:
            print("Category: ")
            print(cat['identifier'])
            print(cat['name'])
            if cat['identifier'] not in akeneoCategories:
                akeneoCategories[cat['identifier']] = {}
            akeneoCategories[cat['identifier']]["code"] = cat['identifier']
            akeneoCategories[cat['identifier']]["parent"] = parentCategory
            if 'labels' not in akeneoCategories[cat['identifier']]:
                akeneoCategories[cat['identifier']]["labels"] = {}
            akeneoCategories[cat['identifier']]["labels"][language] = cat['name']
            if 'children' in cat:
                setCategories(cat['children'], cat['identifier'], akeneoCategories, language)
    else:
        print("Category: ")
        print(category['identifier'])
        print(category['name'])
        if category['identifier'] not in akeneoCategories:
            akeneoCategories[category['identifier']] = {}
        akeneoCategories[category['identifier']]["code"] = category['identifier']
        akeneoCategories[category['identifier']]["parent"] = parentCategory
        if 'labels' not in akeneoCategories[category['identifier']]:
            akeneoCategories[category['identifier']]["labels"] = {}
        akeneoCategories[category['identifier']]["labels"][language] = category['name']
        if 'children' in category:
            setCategories(category['children'], category['identifier'], akeneoCategories, language)

    return akeneoCategories

def setAttributeOptions(options, attribute, akeneoAttirbuteOptions = {}, language = 'en_US'):
    if isinstance(options, list):
        for opt in options:
            print("Option: ")
            print(opt['identifier'])
            print(opt['name'])
            if opt['identifier'] not in akeneoAttirbuteOptions:
                akeneoAttirbuteOptions[opt['identifier']] = {}
            akeneoAttirbuteOptions[opt['identifier']]["code"] = opt['identifier']
            akeneoAttirbuteOptions[opt['identifier']]["attribute"] = attribute
            if 'labels' not in akeneoAttirbuteOptions[opt['identifier']]:
                akeneoAttirbuteOptions[opt['identifier']]["labels"] = {}
            akeneoAttirbuteOptions[opt['identifier']]["labels"][language] = opt['name']
            if 'children' in opt:
                setAttributeOptions(opt['children'], attribute, akeneoAttirbuteOptions, language)
    else:
        print("Option: ")
        print(options['identifier'])
        print(options['name'])
        if options['identifier'] not in akeneoAttirbuteOptions:
            akeneoAttirbuteOptions[options['identifier']] = {}
        akeneoAttirbuteOptions[options['identifier']]["code"] = options['identifier']
        akeneoAttirbuteOptions[options['identifier']]["attribute"] = attribute
        if 'labels' not in akeneoAttirbuteOptions[options['identifier']]:
            akeneoAttirbuteOptions[options['identifier']]["labels"] = {}
        akeneoAttirbuteOptions[options['identifier']]["labels"][language] = options['name']
        if 'children' in options:
            setAttributeOptions(options['children'], attribute, akeneoAttirbuteOptions, language)
    
    return akeneoAttirbuteOptions

def patchCategories(code, body):
    akeneo = Akeneo(
        AKENEO_HOST,
        AKENEO_CLIENT_ID,
        AKENEO_CLIENT_SECRET,
        AKENEO_USERNAME,
        AKENEO_PASSWORD
    )
    try:
        response = akeneo.patchCategoryByCode(code, body)
    except Exception as e:
        print("Error: ", e)
        print("patch Family: ", code)
        print("Response: ", response)
    return response

def patchAttributeOptions(code, attribute, body):
    akeneo = Akeneo(
        AKENEO_HOST,
        AKENEO_CLIENT_ID,
        AKENEO_CLIENT_SECRET,
        AKENEO_USERNAME,
        AKENEO_PASSWORD
    )
    try:
        response = akeneo.patchAttributOptionsByCode(code, attribute, body)
    except Exception as e:
        print("Error: ", e)
        print("patch Family: ", code)
        print("Response: ", response)
    return response

def setCategoriesInAkeneo(akeneoCategories):
    for code, body in akeneoCategories.items():
        print("Code: ", code)
        print("Body: ", body)
        response = patchCategories(code, body)
        print("Response: ", response)

def setAttributeOptionsAkeneo(akeneoCategories, attribute):
    for code, body in akeneoCategories.items():
        print("Code: ", code)
        print("Body: ", body)
        response = patchAttributeOptions(code, attribute, body)

def main():
    category = 'sui_root'
    categoriesEN = getCategoryTree(category, 'en')
    categoriesDE = getCategoryTree(category, 'de')
    categoriesFR = getCategoryTree(category, 'fr')
    categoriesIT = getCategoryTree(category, 'it')

    akeneoCategories = setCategories(categoriesEN)
    akeneoCategories = setCategories(categoriesDE, None, akeneoCategories, 'de_CH')
    akeneoCategories = setCategories(categoriesFR, None, akeneoCategories, 'fr_FR')
    akeneoCategories = setCategories(categoriesIT, None, akeneoCategories, 'it_IT')

    # DEBUG
    #with open("../../output/akeneoCategories.json", "w") as file:
    #    json.dump(akeneoCategories, file)

    attribute = 'leisure'

    #setCategoriesInAkeneo(akeneoCategories)
    print("SET ATTRIBUTE OPTIONS")
    akeneoAttributeOptions = setAttributeOptions(categoriesEN, attribute)
    akeneoAttributeOptions = setAttributeOptions(categoriesDE, attribute, akeneoAttributeOptions, 'de_CH')
    akeneoAttributeOptions = setAttributeOptions(categoriesFR, attribute, akeneoAttributeOptions, 'fr_FR')
    akeneoAttributeOptions = setAttributeOptions(categoriesIT, attribute, akeneoAttributeOptions, 'it_IT')

    # DEBUG
    with open("../../output/akeneoAttributeOptions.json", "w") as file:
        json.dump(akeneoAttributeOptions, file)

    print("PATCH ATTRIBUTE OPTIONS")
    setAttributeOptionsAkeneo(akeneoAttributeOptions, attribute)

if __name__ == "__main__":
    main()

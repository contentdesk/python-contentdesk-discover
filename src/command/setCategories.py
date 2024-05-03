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

def setCategoriesInAkeneo(akeneoCategories):
    for code, body in akeneoCategories.items():
        print("Code: ", code)
        print("Body: ", body)
        response = patchCategories(code, body)
        print("Response: ", response)

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

    with open("../../output/akeneoCategories.json", "w") as file:
        json.dump(akeneoCategories, file)

    setCategoriesInAkeneo(akeneoCategories)

if __name__ == "__main__":
    main()

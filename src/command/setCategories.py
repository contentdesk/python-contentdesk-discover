import json
import sys
sys.path.append("..")

from service.discover import getCategoryTree

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

# set Label for each language
def addLabeltoCategory(category, language, akeneoCategories):
    for key in akeneoCategories:
        print("Category: ")
        print(category)
        akeneoCategories[key]["labels"][language] = category[key]

    return akeneoCategories

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

if __name__ == "__main__":
    main()

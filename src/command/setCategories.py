import json
import sys
sys.path.append("..")

from service.discover import getCategoryTree

def setCategories(category, parentCategory = None, akeneoCategories = {}):
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
            akeneoCategories[cat['identifier']]["labels"]["en_US"] = cat['name']
            if 'children' in cat:
                setCategories(cat['children'], cat['identifier'], akeneoCategories)
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
        akeneoCategories[category['identifier']]["labels"]["en_US"] = category['name']
        if 'children' in category:
            setCategories(category['children'], category['identifier'], akeneoCategories)

    return akeneoCategories

def main():
    category = 'sui_root'
    categories = getCategoryTree(category)
    akeneoCategories = setCategories(categories)

    with open("../../output/akeneoCategories.json", "w") as file:
        json.dump(akeneoCategories, file)

if __name__ == "__main__":
    main()

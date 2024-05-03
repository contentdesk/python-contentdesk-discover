import sys
sys.path.append("..")

from service.discover import getCategoryTree

def setCategories(category, parentCategory):
    # check if category is a list
    if isinstance(category, list):
        for cat in category:
            print("Category: ")
            print(cat['identifier'])
            print(cat['name'])
            if 'children' in cat:
                setCategories(cat['children'], cat['identifier'])
        return
    else:
        print("Category: ")
        print(category['identifier'])
        print(category['name'])
        if 'children' in category:
            setCategories(category['children'], category['identifier'])

def main():
    parentCategory = 'sui_root'
    categories = getCategoryTree(parentCategory)
    setCategories(categories, parentCategory)

if __name__ == "__main__":
    main()

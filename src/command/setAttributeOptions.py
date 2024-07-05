import json
from akeneo.akeneo import Akeneo
import sys
sys.path.append("..")

from service.discover import getCategoryTree
import service.cliArguments as cliArguments
from service.loadEnv import loadEnv

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

def setAttributeOptionsAkeneo(attributeOptions, attribute, akeneo):
    for attributOption in attributeOptions:
        print("Attribute: ", attributOption['attribute'])
        print("Code: ", attributOption['code'])
        code = str(attributOption['code'])
        body = {
            "code": str(attributOption['code']),
            "attribute": attributOption['attribute'],
            "sort_order": attributOption['sort_order'],
            "labels": {
                "en_US": attributOption['labels.en_US'],
                "de_CH": attributOption['labels.de_CH'],
                "fr_FR": attributOption['labels.fr_FR'],
                "it_IT": attributOption['labels.it_IT'],
            }
        }
        try:
            response = akeneo.patchAttributOptionsByCode(code, attribute, body)
            print("Response: ", response)
            print(response.status_code)
            print(response.json())
        except Exception as e:
            print("Error: ", e)
            print("patch Family: ", code)
            print("Response: ", response)

def main():
    environments = cliArguments.getEnvironment(sys)
    arguments = cliArguments.getArguments(sys)
    
    category = 'sui_root'
    categoriesEN = getCategoryTree(category, 'en')
    categoriesDE = getCategoryTree(category, 'de')
    categoriesFR = getCategoryTree(category, 'fr')
    categoriesIT = getCategoryTree(category, 'it')

    attribute = 'leisure'

    print("SET ATTRIBUTE OPTIONS")
    akeneoAttributeOptions = setAttributeOptions(categoriesEN, attribute)
    akeneoAttributeOptions = setAttributeOptions(categoriesDE, attribute, akeneoAttributeOptions, 'de_CH')
    akeneoAttributeOptions = setAttributeOptions(categoriesFR, attribute, akeneoAttributeOptions, 'fr_FR')
    akeneoAttributeOptions = setAttributeOptions(categoriesIT, attribute, akeneoAttributeOptions, 'it_IT')

    # remove the first element
    akeneoAttributeOptions.pop('sui_root')

    # DEBUG
    with open("../../output/akeneoAttributeOptions.json", "w") as file:
        json.dump(akeneoAttributeOptions, file)

    print("PATCH ATTRIBUTE OPTIONS")
    for environment in environments:
        print(f"Environment: {environment}")
        targetCon = loadEnv(environment)
        target = Akeneo(targetCon["host"], targetCon["clientId"], targetCon["secret"], targetCon["user"], targetCon["passwd"])
        print(target)
        setAttributeOptionsAkeneo(akeneoAttributeOptions, attribute, target)

if __name__ == "__main__":
    main()

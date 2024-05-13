import json
import sys
sys.path.append("..")

from service.discover import getTypesTree
from akeneo.akeneo import Akeneo
from os import getenv
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

AKENEO_HOST = getenv('AKENEO_HOST')
AKENEO_CLIENT_ID = getenv('AKENEO_CLIENT_ID')
AKENEO_CLIENT_SECRET = getenv('AKENEO_CLIENT_SECRET')
AKENEO_USERNAME = getenv('AKENEO_USERNAME')
AKENEO_PASSWORD = getenv('AKENEO_PASSWORD')

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

def setTypes(types, akeneoTypes = {}, language = 'en_US'):
    # check if category is a list
    if isinstance(types, list):
        for typ in types:
            print("Type: ")
            print(typ['entityType'])
            print(typ['name'])
            if 'additionalType' in typ:
                if typ['additionalType'] not in akeneoTypes:
                    akeneoTypes[typ['additionalType']] = {}
                akeneoTypes[typ['additionalType']]["code"] = typ['additionalType']
                if 'labels' not in akeneoTypes[typ['additionalType']]:
                    akeneoTypes[typ['additionalType']]["labels"] = {}
                akeneoTypes[typ['additionalType']]["labels"][language] = typ['name']
                if 'types' in typ:
                    setTypes(typ['types'], akeneoTypes, language)
            else:
                if typ['entityType'] not in akeneoTypes:
                    akeneoTypes[typ['entityType']] = {}
                akeneoTypes[typ['entityType']]["code"] = typ['entityType']
                if 'labels' not in akeneoTypes[typ['entityType']]:
                    akeneoTypes[typ['entityType']]["labels"] = {}
                akeneoTypes[typ['entityType']]["labels"][language] = typ['name']
                if 'types' in typ:
                    setTypes(typ['types'], akeneoTypes, language)
    else:
        print("Type: ")
        print(types['entityType'])
        print(types['name'])
        if types['entityType'] not in akeneoTypes:
            akeneoTypes[types['entityType']] = {}
        akeneoTypes[types['entityType']]["code"] = types['entityType']
        if 'labels' not in akeneoTypes[types['entityType']]:
            akeneoTypes[types['entityType']]["labels"] = {}
        akeneoTypes[types['entityType']]["labels"][language] = types['name']
        if 'types' in types:
            setTypes(types['types'], akeneoTypes, language)

    return akeneoTypes

def main():
    typesEN = getTypesTree('en')
    typesDE = getTypesTree('de')
    typesFR = getTypesTree('fr')
    typesIT = getTypesTree('it')

    akeneoTypes = setTypes(typesEN)
    akeneoTypes = setTypes(typesDE, akeneoTypes, 'de_CH')
    akeneoTypes = setTypes(typesFR, akeneoTypes, 'fr_FR')
    akeneoTypes = setTypes(typesIT, akeneoTypes, 'it_IT')

    # DEBUG
    with open("../../output/types.json", "w") as file:
        json.dump(akeneoTypes, file)

if __name__ == "__main__":
    main()

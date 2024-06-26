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

def setTypes(types, akeneoTypes = {}, language = 'en_US', parent = None):
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
                akeneoTypes[typ['additionalType']]["parent"] = parent
                if 'labels' not in akeneoTypes[typ['additionalType']]:
                    akeneoTypes[typ['additionalType']]["labels"] = {}
                akeneoTypes[typ['additionalType']]["labels"][language] = typ['name']
                if 'types' in typ:
                    setTypes(typ['types'], akeneoTypes, language, typ['entityType'])
            else:
                if typ['entityType'] not in akeneoTypes:
                    akeneoTypes[typ['entityType']] = {}
                akeneoTypes[typ['entityType']]["code"] = typ['entityType']
                akeneoTypes[typ['entityType']]["parent"] = parent
                if 'labels' not in akeneoTypes[typ['entityType']]:
                    akeneoTypes[typ['entityType']]["labels"] = {}
                akeneoTypes[typ['entityType']]["labels"][language] = typ['name']
                if 'types' in typ:
                    setTypes(typ['types'], akeneoTypes, language, typ['entityType'])
    else:
        print("Type: ")
        print(types['entityType'])
        print(types['name'])
        if types['entityType'] not in akeneoTypes:
            akeneoTypes[types['entityType']] = {}
        akeneoTypes[types['entityType']]["code"] = types['entityType']
        akeneoTypes[types['entityType']]["parent"] = parent
        if 'labels' not in akeneoTypes[types['entityType']]:
            akeneoTypes[types['entityType']]["labels"] = {}
        akeneoTypes[types['entityType']]["labels"][language] = types['name']
        if 'types' in types:
            setTypes(types['types'], akeneoTypes, language)

    return akeneoTypes

def patchTypes(code, body):
    akeneo = Akeneo(
        AKENEO_HOST,
        AKENEO_CLIENT_ID,
        AKENEO_CLIENT_SECRET,
        AKENEO_USERNAME,
        AKENEO_PASSWORD
    )
    try:
        response = akeneo.patchFamily(code, body)
    except Exception as e:
        print("Error: ", e)
        print("patch Family: ", code)
        print("Response: ", response)
    return response

def setTypesInAkeneo(akeneoTypes):
    for code, body in akeneoTypes.items():
        print("Code: ", code)
        print("Body: ", body)
        response = patchTypes(code, body)

def main():
    typesEN = getTypesTree('en')
    typesDE = getTypesTree('de')
    typesFR = getTypesTree('fr')
    typesIT = getTypesTree('it')

    akeneoTypes = setTypes(typesEN)
    akeneoTypes = setTypes(typesDE, akeneoTypes, 'de_CH')
    akeneoTypes = setTypes(typesFR, akeneoTypes, 'fr_FR')
    akeneoTypes = setTypes(typesIT, akeneoTypes, 'it_IT')


    # replace "-" with "" in key fields
    akeneoTypes = {k.replace("-", ""): v for k, v in akeneoTypes.items()}

    # DEBUG
    with open("../../output/types.json", "w") as file:
        json.dump(akeneoTypes, file)

    #setTypesInAkeneo(akeneoTypes)

    # Save as csv with UTF-8 encoding and replace "None" in every field with empty string
    with open("../../output/types.csv", "w", encoding='utf-8') as file:
        for code, body in akeneoTypes.items():
            parent = body['parent'] if body['parent'] else ''
            en = body['labels']['en_US'] if 'en_US' in body['labels'] else ''
            de = body['labels']['de_CH'] if 'de_CH' in body['labels'] else ''
            fr = body['labels']['fr_FR'] if 'fr_FR' in body['labels'] else ''
            it = body['labels']['it_IT'] if 'it_IT' in body['labels'] else ''
            file.write(f"{code};{parent};{en};{de};{fr};{it}\n")


if __name__ == "__main__":
    main()

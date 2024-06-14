import json
import sys
sys.path.append("..")

from service.discover import getAmenityFeatures

def setAmenityFeatures(amenityFeatures, akeneoAmenityFeatures = {}, language = 'en_US', parent = None):
    # check if category is a list
    if isinstance(amenityFeatures, list):
        for typ in amenityFeatures:
            print("AmenityFeatures: ")
            print(typ['propertyId'])
            print(typ['name'])
            if typ['propertyId'] not in akeneoAmenityFeatures:
                    akeneoAmenityFeatures[typ['propertyId']] = {}
            akeneoAmenityFeatures[typ['propertyId']]["code"] = typ['propertyId']
            akeneoAmenityFeatures[typ['propertyId']]["parent"] = None
            akeneoAmenityFeatures[typ['propertyId']]["labels"][language] = typ['name']
            akeneoAmenityFeatures[typ['propertyId']]["additionalType"] = typ['additionalType']

            if 'propertyId' in typ:
                if typ['propertyId'] not in akeneoAmenityFeatures:
                    akeneoAmenityFeatures[typ['propertyId']] = {}
                akeneoAmenityFeatures[typ['propertyId']]["code"] = typ['additionalType']
                akeneoAmenityFeatures[typ['propertyId']]["parent"] = parent
                if 'labels' not in akeneoAmenityFeatures[typ['propertyId']]:
                    akeneoAmenityFeatures[typ['propertyId']]["labels"] = {}
                akeneoAmenityFeatures[typ['propertyId']]["labels"][language] = typ['name']
                if 'types' in typ:
                    setAmenityFeatures(typ['types'], akeneoAmenityFeatures, language, typ['propertyId'])
            else:
                if typ['propertyId'] not in akeneoAmenityFeatures:
                    akeneoAmenityFeatures[typ['propertyId']] = {}
                akeneoAmenityFeatures[typ['propertyId']]["code"] = typ['propertyId']
                akeneoAmenityFeatures[typ['propertyId']]["parent"] = parent
                if 'labels' not in akeneoAmenityFeatures[typ['propertyId']]:
                    akeneoAmenityFeatures[typ['propertyId']]["labels"] = {}
                akeneoAmenityFeatures[typ['propertyId']]["labels"][language] = typ['name']
                if 'types' in typ:
                    setAmenityFeatures(typ['types'], akeneoAmenityFeatures, language, typ['propertyId'])


def main():
    amenityFeaturesEN = getAmenityFeatures('en')
    amenityFeaturesDE = getAmenityFeatures('de')
    amenityFeaturesFR = getAmenityFeatures('fr')
    amenityFeaturesIT = getAmenityFeatures('it')

    akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesEN)
    #akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesDE, akeneoAmenityFeatures, 'de_DE')
    #akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesFR, akeneoAmenityFeatures, 'fr_FR')
    #akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesIT, akeneoAmenityFeatures, 'it_IT')

    # DEBUG
    with open("../../output/akeneoAmenityFeatures.json", "w") as file:
        json.dump(akeneoAmenityFeatures, file)

    # Save as csv with UTF-8 encoding and replace "None" in every field with empty string
    with open("../../output/akeneoAmenityFeatures.csv", "w", encoding='utf-8') as file:
        for code, body in akeneoAmenityFeatures.items():
            en = body['labels']['en_US'] if 'en_US' in body['labels'] else ''
            de = body['labels']['de_DE'] if 'de_DE' in body['labels'] else ''
            fr = body['labels']['fr_FR'] if 'fr_FR' in body['labels'] else ''
            it = body['labels']['it_IT'] if 'it_IT' in body['labels'] else ''
            file.write(f"{code},{en},{de},{fr},{it}\n")

if __name__ == "__main__":
    main()
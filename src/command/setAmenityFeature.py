import json
import os
from datetime import datetime
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
            if 'labels' not in akeneoAmenityFeatures[typ['propertyId']]:
                akeneoAmenityFeatures[typ['propertyId']]["labels"] = {}
            akeneoAmenityFeatures[typ['propertyId']]["labels"][language] = typ['name']
            if 'additionalType' in typ:
                akeneoAmenityFeatures[typ['propertyId']]["parent"] = typ['additionalType']
            if 'valueType' in typ:
                akeneoAmenityFeatures[typ['propertyId']]["valueType"] = typ['valueType']

    return akeneoAmenityFeatures

def main():
    amenityFeaturesEN = getAmenityFeatures('en')
    amenityFeaturesDE = getAmenityFeatures('de')
    amenityFeaturesFR = getAmenityFeatures('fr')
    amenityFeaturesIT = getAmenityFeatures('it')

    akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesEN)
    akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesDE, akeneoAmenityFeatures, 'de_DE')
    akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesFR, akeneoAmenityFeatures, 'fr_FR')
    akeneoAmenityFeatures = setAmenityFeatures(amenityFeaturesIT, akeneoAmenityFeatures, 'it_IT')

    # replace "-" with "_" in key fields
    akeneoAmenityFeatures = {k.replace("-", "_"): v for k, v in akeneoAmenityFeatures.items()}
    
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    str_current_datetime = str(current_datetime)
        
    with open("../../output/akeneoAmenityFeatures.json", "w") as file:
        json.dump(akeneoAmenityFeatures, file)
            
    # Save as csv with UTF-8 encoding and replace "None" in every field with empty string
    with open("../../output/akeneoAmenityFeatures.csv", "w", encoding='utf-8') as file:
        for code, body in akeneoAmenityFeatures.items():
            en = body['labels']['en_US'] if 'en_US' in body['labels'] else ''
            de = body['labels']['de_DE'] if 'de_DE' in body['labels'] else ''
            fr = body['labels']['fr_FR'] if 'fr_FR' in body['labels'] else ''
            it = body['labels']['it_IT'] if 'it_IT' in body['labels'] else ''
            parent = body['parent'] if 'parent' in body else ''
            valueType = body['valueType'] if 'valueType' in body else ''
            file.write(f"{code};{en};{de};{fr};{it};{valueType};{parent}\n")

if __name__ == "__main__":
    main()
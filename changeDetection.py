import csv
import json

def read_csv_file(file_name):
    with open(file_name) as csvfile:
        data = list(csv.reader(csvfile))
    return data

def createFeatureDict(features):
    featureDict = {}
    for i in range(2, len(features)):
        featureDict[features[i]] = []
    return featureDict

def extractFeatureAngles(data, featureAngleDict, features):
    for i in range(len(data)):
        for j in range(2, len(data[i])):
            featureAngleDict[features[j]].append(float(data[i][j]))

def extractFeatureChange(featureAngleDict, featureChangeAngleDict, featureChangeNameDict):
    for key in featureAngleDict:
        changesPositively = True
        for i in range(len(featureAngleDict[key]) - 1): 
            if featureAngleDict[key][i] > featureAngleDict[key][i + 1] and changesPositively:
                # if previous change and current angle i differ by more than 20 degrees
                if len(featureChangeAngleDict[key]) == 0 or abs(featureChangeAngleDict[key][-1] - featureAngleDict[key][i]) > 20:
                    state = getAngleState(featureAngleDict[key][i])
                    if len(featureChangeNameDict[key]) == 0 or state != featureChangeNameDict[key][-1]:
                        featureChangeNameDict[key].append(state)
                    featureChangeAngleDict[key].append(featureAngleDict[key][i])
                changesPositively = False
            elif featureAngleDict[key][i] < featureAngleDict[key][i + 1] and not changesPositively:
                # if previous change and current angle i differ by more than 20 degrees
                if len(featureChangeAngleDict[key]) == 0 or abs(featureChangeAngleDict[key][-1] - featureAngleDict[key][i]) > 20:
                    state = getAngleState(featureAngleDict[key][i])
                    if len(featureChangeNameDict[key]) == 0 or state != featureChangeNameDict[key][-1]:
                        featureChangeNameDict[key].append(state)
                    featureChangeAngleDict[key].append(featureAngleDict[key][i])
                changesPositively = True

def getAngleState(angle):
    if angle < 20 and angle > -20:
        return "fully open"
    elif (angle < 120 and angle > 60) or (angle < -60 and angle > -120):
        return "half bent"
    elif (angle < 190 and angle > 150) or (angle < -150 and angle > -190):
        return "fully bent"
    else:
        return str(angle)
    


file_name = './results/v2_BLAZEPOSE_angles.csv'
data = read_csv_file(file_name)
features = data[2]
data = data[4:]
featureAngleDict = createFeatureDict(features)
featureChangeAngleDict = createFeatureDict(features)
featureChangeNameDict = createFeatureDict(features)
extractFeatureAngles(data, featureAngleDict, features)
extractFeatureChange(featureAngleDict, featureChangeAngleDict, featureChangeNameDict)

# write featureChangeDict to a json file test.json
with open('testAngle.json', 'w') as f:
    json.dump(featureChangeAngleDict, f)
with open('testName.json', 'w') as f:
    json.dump(featureChangeNameDict, f)


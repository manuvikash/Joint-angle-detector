import GenerateAngles
import DynamicTimeWarping
import Jerk

def calcScore(similarity, smoothness):

    score = ((0.8 * similarity) + (0.2 * smoothness)).round(3)
    
    return score

# standardFile = 'v1'
# testFile = 'test2'

# # GenerateAngles.detectAngles(testFile)
# # GenerateAngles.displayJA(testFile)

# diff, similarity, simDict = DynamicTimeWarping.dtw(standardFile, testFile)
# jerk, smoothness = Jerk.getJerk(testFile)

# score = calcScore(similarity, smoothness)

# print(similarity, smoothness)
# print(score)


GenerateAngles.detectAngles('CP1')
GenerateAngles.displayJA('CP1')
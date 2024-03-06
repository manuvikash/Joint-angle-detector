import GenerateAngles
import DynamicTimeWarping
import Jerk

def calcScore(dtw, smooth):
    return ((0.8 * dtw) + (0.2 * smooth)).round(3)

standardFile = 'v2'
testFile = 'test2'

# GenerateAngles.detectAngles(testFile)
# GenerateAngles.displayJA(testFile)

diff, similarity, simDict = DynamicTimeWarping.dtw(standardFile, testFile)
jerk, smoothness = Jerk.jerk(testFile)

score = calcScore(similarity, smoothness)

print(similarity, smoothness)
print(score)


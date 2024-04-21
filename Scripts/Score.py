import GenerateAngles
import DynamicTimeWarping
import Jerk

def calcScore(similarity, smoothness):

    score = ((0.6 * similarity) + (0.4 * smoothness)).round(3)
    
    return score

def runDemo(testFile, standardFile):
    diff, similarity, simDict, graphs = DynamicTimeWarping.dtw(standardFile, testFile)
    jerk, smoothness, smoothnessDict = Jerk.getJerk(testFile)

    # Calculate overall score
    score = calcScore(similarity, smoothness)

    # Create a dictionary to store all results
    results = {
        "Overall score": score,
        "Overall Similarity": similarity,
        "Overall Smoothness": smoothness,
        "Per Joint values": {}
    }

    # Add per joint values
    for joint, sim_value in simDict.items():
        jointScore = calcScore(sim_value, smoothnessDict[joint])
        results["Per Joint values"][joint] = {
            "Score": jointScore,
            "Similarity": sim_value,
            "Smoothness": smoothnessDict[joint]
        }

    # Return the results dictionary
    return results, graphs

import skipgram
import wv
import neg_samples
import globalVar

sampleNum = 20 # 把没有相关关系的推开
windowLength = 5 # 5 就有前后10个词语够了

def singleEntry(entry):
    cost = 0
    trainingPairs, tokens, wordVectors = wv.getDataset(entry[2], windowLength)
    for pair in trainingPairs:
        centerword, contextWords = pair        
        negSamples_list = neg_samples.get(contextWords, sampleNum)
        if len(negSamples_list) == 0: return 
        assert type(negSamples_list[0]) == dict
        _cost = skipgram.run(centerword, contextWords, negSamples_list)
        cost += _cost
    if len(trainingPairs) != 0:
        avgCost = cost/len(trainingPairs)
        print(avgCost)
    else:
        return 0
    
    if avgCost <= 2:
        globalVar.set('step',0.01) # 0.3 的效果不好
        print('调整step为：0.01')
    else:
        if avgCost <= 20:
            globalVar.set('step',0.05) # 0.3 的效果不好
            print('调整step为：0.05')

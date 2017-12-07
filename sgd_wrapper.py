import numpy as np
import random
import skipgram
import json
import db_model
import wv
import neg_samples
import globalVar
import voca_model

globalVar._init()
globalVar.set('step',0.1) # 0.3 的效果不好
try:
    model = voca_model.readJson()
    globalVar.set('voca_model',model)
except FileNotFoundError:
    voca_model.createJson()
    globalVar.set('voca_model',[]) 
    # print('FileNotFoundError-FileNotFoundError-FileNotFoundError')



sampleNum = 10
version = 0
windowLength = 5
repeatedTimes_forTheSameNegSample = 15 # 这个太高，貌似会出现inf 

def word2vec_sgd_wrapper(entry):
    cost = 0
    trainingPairs, tokens, wordVectors = wv.getDataset(entry[2], windowLength)
    for pair in trainingPairs:
        centerword, contextWords = pair
        # print(centerword)
        
        negSamples_list = neg_samples.get(contextWords, sampleNum)
        
        if negSamples_list == None: return 
        
        assert type(negSamples_list[0]) == dict
        _cost = skipgram.run(centerword, contextWords, negSamples_list)
        cost += _cost
    
    avgCost = cost/len(trainingPairs)
    print(avgCost)
    
    # if avgCost <= 3:
    #     globalVar.set('step',0.01) # 0.3 的效果不好
    #     print('调整step为1档：0.01')
    # else:
    #     if avgCost <= 7:
    #         globalVar.set('step',0.02) 
    #         print('调整step为2档：0.02')
    #     else:
    if avgCost <= 14:
        globalVar.set('step',0.1) # 0.3 的效果不好
        print('调整step为3档：0.05')

for i in range(10): 
    print('第 %d 次运行' % (i,))
    globalVar.set('step',0.2)
    # print('调整step为0.1')

    entry = db_model.fetch_entry_untreated(version)
    for j in range(repeatedTimes_forTheSameNegSample):
        word2vec_sgd_wrapper(entry)
    db_model.mark_entry_as_treated(entry[0], version)
voca_model.saveJson()

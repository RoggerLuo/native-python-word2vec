import train
import db_model
import globalVar
import voca_model
import numpy as np
globalVar._init()
model = voca_model.readJson()
globalVar.set('vocabulary', model) 

def findWord(word,length=10):
    entrys = voca_model.getWordEntrys(word)
    if len(entrys) == 0:
        print('没找到')
    cen_entry = entrys[0]
    
    vocabulary = globalVar.get('vocabulary')    
    allEntrys = vocabulary

    unsortedList = []
    for et in allEntrys:
        deviationArr = cen_entry['vector'] - et['vector']
        # deviationArr = np.fabs(deviationArr)
        deviationArr = [round(de, 5) for de in deviationArr.tolist()]
        deviationArr = np.square(np.array(deviationArr))
        deviation = np.sum(deviationArr)
        unsortedList.append({'deviation': deviation, 'id': et['id']})
    
    sortedList = sorted(unsortedList, key=lambda dic: dic['deviation'])
    
    for nearId in sortedList[0:length]:
        print(voca_model.getWordById(nearId['id'])['word'])




findWord('效率',20)

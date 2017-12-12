import train
import db_model
import globalVar
import voca_model
import json
import numpy as np

def normalizeRows(x):
    assert type(x) == np.ndarray
    transposeX = x.T
    x = (transposeX / np.sqrt(np.sum(transposeX**2, axis=0))).T
    return x

def get(entryId,length):
    providedEntry = db_model.fetch_by_id(entryId)
    providedVector = providedEntry[10]
    print('原文章：')
    print(providedEntry[2])
    print('---- ---- ---- ----')

    allEntrys = db_model.fetch_all()
    unsortedList = []
    for dbEntry in allEntrys:
        targetVector = dbEntry[10]
        if targetVector != None:
            deviationArr = np.array(json.loads(providedVector)) - np.array(json.loads(targetVector))
            # deviationArr = normalizeRows(deviationArr)
            # deviationArr = np.fabs(deviationArr)
            deviationArr = [round(de, 5) for de in deviationArr.tolist()]
            deviationArr = np.square(np.array(deviationArr))
            deviation = np.sum(deviationArr)
            unsortedList.append(
                {'deviation': deviation, 'id': dbEntry[0], 'text': dbEntry[2]})


    sortedList = sorted(unsortedList, key=lambda dic: dic['deviation'])
    for element in sortedList[0:length]:
        print(element['text'])
        print('---- ---- ---- ----')


get(5957,10)
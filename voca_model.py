import json
import numpy as np
import globalVar

def createJson():
    voca_model = []
    with open("./data.json", 'w', encoding='utf-8') as json_file:
        json.dump(voca_model, json_file, ensure_ascii=False)

def saveJson():
    voca_model = globalVar.get('voca_model')  # 0.3 的效果不好
    # voca_model = {'test': 'testValue'}  # 存放读取的数据
    with open("./data.json", 'w', encoding='utf-8') as json_file:
        json.dump(voca_model, json_file, ensure_ascii=False)


def readJson():
    with open("./data.json", 'r', encoding='utf-8') as json_file:
        voca_model = json.load(json_file)
        globalVar.set('voca_model', voca_model)  # 0.3 的效果不好
        return voca_model


def update_vec(entry, vec):  # entry 直接传这个词所在的index
    # if type(vec) == np.ndarray:
        # vec = vec.tolist()            
    # assert type(vec) == np.ndarray
    # vec = [round(v, 5) for v in vec]
    # vec = json.dumps(vec)
    assert type(vec) == np.ndarray

    voca_model = globalVar.get('voca_model')
    voca_model[entry['id']]['vector'] = vec


def getWordEntrys(word):
    voca_model = globalVar.get('voca_model')
    value = []
    for ind in range(len(voca_model)):
        if word == voca_model[ind]['word']:
            value = [ voca_model[ind] ]
    return value


def insertVocabulary(word, startVector):
    assert type(startVector) == np.ndarray
    # startVector = [round(v, 5) for v in startVector]
    # startStr = json.dumps(startVector)
    voca_model = globalVar.get('voca_model')
    insert_id = len(voca_model)-1
    voca_model.append({'word':word,'vector': startVector,'id':insert_id})
    return insert_id


def getNegSameples(contextWords, k=10):
    voca_model = globalVar.get('voca_model')
    num = len(voca_model) - 1
    voca_model = globalVar.get('voca_model')
    values = [] 
    for index in range(50):
        values.append(voca_model[np.random.randint(num)])
    return values

# def getAll():

#     cursor.execute('select * from t_vocabulary')
#     values = cursor.fetchall()
#     return values


def getWordById(entryId):
    voca_model = globalVar.get('voca_model')
    return voca_model[entryId]
    # cursor.execute('select * from t_vocabulary where id = %s', (entryId,))
    # values = cursor.fetchall()
    # return values[0]



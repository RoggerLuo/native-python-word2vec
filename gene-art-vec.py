import train
import db_model
import globalVar
import voca_model
import wv
import numpy as np

globalVar._init()

try:
    model = voca_model.readJson()
    globalVar.set('voca_model', model)
except FileNotFoundError:
    voca_model.createJson()
    globalVar.set('voca_model', [])


def normalizeRows(x):
    assert type(x) == np.ndarray
    transposeX = x.T
    x = (transposeX / np.sqrt(np.sum(transposeX**2, axis=0))).T
    return x

allEntrys = db_model.fetch_all()
counter = 1

for entry in allEntrys:
    vec = []
    content = entry[2]
    content = wv.segment(content)
    filteredArr = wv.filterWord(content)

    for word in filteredArr:
        insert_id, wordvec = wv.getIdAndVector(word)
        assert type(wordvec) == np.ndarray
        if len(vec) == 0:
            vec = wordvec
        else:
            vec += wordvec
    if len(vec) != 0:
        vec = normalizeRows(vec)
        vec = vec.tolist()
        db_model.update_entry_vector(entry[0], vec)
        print('完成第%d篇文章的vector计算' % counter)
    else:

        print('第%d篇文章的filteredArr为空' % counter)
    counter += 1

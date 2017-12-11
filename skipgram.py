import numpy as np
import random
import wv
import json
import db_model
import negSampling
import globalVar
import voca_model

def update_o_grad(entry, grad):
    # print('entry')
    # print(type(entry['vector']))
    # print(entry['vector'])

    assert type(entry['vector']) == np.ndarray

    step = globalVar.get('step')
    # vec = np.array(entry['vector'])
    vec = entry['vector']
    zeroArr = np.zeros(int(len(vec) / 2))
    vec_grad = np.concatenate((zeroArr, np.array(grad)), axis=0)
    return vec - vec_grad * step


def update_i_grad(entry, grad):
    step = globalVar.get('step')
    vec = entry['vector']
    zeroArr = np.zeros(int(len(vec) / 2))
    vec_grad = np.concatenate((np.array(grad), zeroArr), axis=0)
    return vec - vec_grad * step


def getEntry_and_makeList(centerword):
    entry = voca_model.getWordEntrys(centerword)[0]
    vec = entry['vector']
    return entry, vec


def run(centerword, contextWords, negSamples_list):
    assert type(centerword) == str
    assert type(contextWords) == list
    # print(type(negSamples_list))
    assert type(negSamples_list) == list
    assert type(negSamples_list[0]['vector']) == np.ndarray

    cen_entry, cent_vec = getEntry_and_makeList(centerword)
    cent_vec = np.array(cent_vec)
    cost = 0.0
    gradIn = []
    for targetword in contextWords:
        target_entry, target_vec = getEntry_and_makeList(targetword)

        # target_vec = json.loads(db_model.getWordEntrys(targetword)[0][2])
        ___cost, ___cen_i_grad, ___negSamples_grad, ___target_o_grad = negSampling.get_cost_and_grad(
            cent_vec, target_vec, negSamples_list)
        cost += ___cost

        if len(gradIn) == 0:
            gradIn = ___cen_i_grad
        else:
            gradIn += ___cen_i_grad

        # target word output忘记更新了
        new_target_vec = update_o_grad(target_entry, ___target_o_grad)
        assert type(new_target_vec) == np.ndarray
        assert len(new_target_vec) == 16
        voca_model.update_vec(target_entry, new_target_vec)


        for index in range(len(negSamples_list)):
            curr_entry = negSamples_list[index]

            assert type(curr_entry) == dict

            curr_grad = ___negSamples_grad[index]
            assert type(curr_grad) == np.ndarray

            curr_vec = update_o_grad(curr_entry, curr_grad)
            assert type(curr_vec) == np.ndarray
            # curr_vec = curr_vec.tolist()
            # assert type(curr_vec) == list
            assert len(curr_vec) == 16

            negSamples_list[index]['vector'] = curr_vec  # 更新完才开始下一轮

    if len(gradIn) == 0:
        return 0.0

    i_vec = update_i_grad(cen_entry, gradIn)
    assert type(i_vec) == np.ndarray
    assert len(i_vec) == 16
    voca_model.update_vec(cen_entry, i_vec)

    for sampleEntry in negSamples_list: 
        assert type(sampleEntry['vector']) == np.ndarray
        assert len(sampleEntry['vector']) == 16
        voca_model.update_vec(sampleEntry, sampleEntry['vector'])

    return cost


# db_model.mark_entry_as_treated(entry[0])

# entry = db_model.fetch_entry_untreated()
# string = entry[2]
# # print(string)
# windowLength = 3
# trainingPairs, tokens, wordVectors = wv.getDataset(string, windowLength)
# pair = trainingPairs[0]
# centerword = pair[0]
# contextWords = pair[1]
# sampleNum = 4
# centerword_vector = json.loads(db_model.getWordEntrys(centerword)[0][2])


# a = skipgram(centerword, contextWords)
# print(a)

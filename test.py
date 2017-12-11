import train
import db_model
import globalVar
import voca_model


version = 0
repeatedTimes_forTheSameNegSample = 10  # 这个太高，貌似会出现inf


globalVar._init()
globalVar.set('step', 0.1)  # 0.2 的效果不好

model = voca_model.readJson()
voca_model.test('效率',20)

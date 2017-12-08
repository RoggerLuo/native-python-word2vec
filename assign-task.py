import train
import db_model
import globalVar
import voca_model


version = 1
repeatedTimes_forTheSameNegSample = 10  # 这个太高，貌似会出现inf


globalVar._init()
globalVar.set('step', 0.1)  # 0.2 的效果不好

try:
    model = voca_model.readJson()
    globalVar.set('voca_model', model)
except FileNotFoundError:
    voca_model.createJson()
    globalVar.set('voca_model', [])

for i in range(1000000):
    print('第 %d 次运行' % (i,))
    globalVar.set('step', 0.1)
    entry = db_model.fetch_entry_untreated(version)
    
    if entry == False: 
        print('没有version为%s的entry了' % version)
        break
    
    for j in range(repeatedTimes_forTheSameNegSample):
        train.singleEntry(entry)
    
    db_model.mark_entry_as_treated(entry[0], version)
    if i%30 == 0:
        voca_model.saveJson()
        print('json自动保存成功')

voca_model.saveJson()
print('json保存成功')

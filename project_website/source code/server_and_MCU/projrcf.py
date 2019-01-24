from sklearn.ensemble import RandomForestClassifier
from pymongo import MongoClient
from sklearn import svm
from sklearn.externals import joblib
import numpy as np
conn = MongoClient()
db = conn.finalproject

both_set = db.both 
x= []
y = []
for i in both_set.find():
    print(len(i['data']))
    x.append(i["data"])
    y.append(i["type"])
x = np.array(x)
y = np.array(y)
print(x)
print(y)


# clf = RandomForestClassifier(n_estimators=100)
# clf.fit(x, y)
# joblib.dump(clf, 'bothrfc.pkl')
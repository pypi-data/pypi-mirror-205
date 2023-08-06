class data:
    def get(self):
        return """import pandas as pd  # pip install pandas

df = pd.read_excel('123.xlsx', sheet_name='2')

df[['E', 'F']] = df.pop('D').str.split(',', expand=True)  #以逗號分隔變數

df = df.apply(pd.to_numeric, errors='coerce')  #轉換為數字，無法轉換的值設為NaN

df.drop_duplicates(inplace=True)  #刪除重複值

df = df.query(' 0 <= B <= 100 & 0 <= C <= 100')  #刪除極端值

df.dropna(inplace=True)  #刪除缺失值
#df.fillna(0, inplace=True)  #填補缺失值為0
#df.fillna(df.mean(), inplace=True)  #填補缺失值為平均值

df.to_excel('data.xlsx', index=False)  #另存新檔
print(df)"""

class math:
    def get(self):
        return """import pandas as pd

df = pd.read_excel('123.xlsx', sheet_name='1')
X, y, z = df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, 3]

perc =[0.25, 0.75] 
X_de = X.describe(percentiles = perc)
print("統計:", X_de)

median = X.median()
print("中位数:", median)

mode = X.mode().to_list()
print("眾數:", mode)

count = X.value_counts()[55]
print("某數出現次數:", count)

corr_matrix = df.iloc[:, 1:4].corr()
print("相關係數矩陣:", corr_matrix)"""

class RF:
    def get(self):
        return """import pandas as pd
import matplotlib.pyplot as plt  # pip install matplotlib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, r2_score, mean_squared_error, mean_absolute_error

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBClassifier  # pip install xgboost
from lightgbm import LGBMClassifier  #pip install lightgbm
from catboost import CatBoostClassifier  #pip install catboost

df = pd.read_excel('123.xlsx', sheet_name='1')
X, y = df.iloc[:, 1:4], df.iloc[:, 0]

#拆分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# #建立、訓練模型、搜尋超參數
# RF0 = RandomForestClassifier(random_state=0)
# pm = {'n_estimators':[100,500,1000], 'min_samples_leaf':[2,10,20]}
# #pm = {'n_estimators':list(range(50, 151)), 'min_samples_leaf':list(range(1, 5))}
# RF = GridSearchCV(RF0, pm, cv=5)
# RF.fit(X_train, y_train)
# print(RF.best_params_)

#建立、訓練模型、超參數
RF = RandomForestClassifier(n_estimators=50, random_state=0)
RF.fit(X_train, y_train)
print(RF.get_params())

#評估迴歸模型
y_test2 = RF.predict(X_test)
r2 = r2_score(y_test, y_test2)
print("R2:", r2)
rmse = mean_squared_error(y_test, y_test2, squared=False)
print("RMSE:", rmse)
mae = mean_absolute_error(y_test, y_test2)
print("MAE:", mae)

#混淆矩陣
y_test2 = RF.predict(X_test)
cm = confusion_matrix(y_test, y_test2)
print("混淆矩陣:", cm)

#分類報告
cr = classification_report(y_test, y_test2)
print("分類報告:", cr)

#特徵重要性、將特徵重要性與特徵名稱存到DataFrame、按特徵重要性降序排序
imp = RF.feature_importances_
Ximp = pd.DataFrame({'feature': X.columns, 'importance': imp})
Ximp = Ximp.sort_values('importance', ascending=False)
print(Ximp)
plt.bar(Ximp['feature'], Ximp['importance'])
plt.title('Feature Importance')
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.show()

#分類、預測
X_new = df.iloc[0:2, 6:9].values
y_pred = RF.predict(X_new)
print(y_pred)"""

class OLS:
    def get(self):
        return """import pandas as pd
import statsmodels.api as sm  # pip install statsmodels、pip install scikit-learn
from sklearn.model_selection import train_test_split  #升級pip install -U scikit-learn
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target

#拆分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

#添加常數項
X_train = sm.add_constant(X_train)
X_test = sm.add_constant(X_test)

#建立模型
RF = sm.OLS(y_train, X_train).fit()
# RF = sm.QuantReg(y_train, X_train).fit(q=0.5)
print(RF.summary())  #訓練集的R2

#評估模型
y_test2 = RF.predict(X_test)
r2 = r2_score(y_test, y_test2)
print("R2:", r2)  #測試集的R2
rmse = mean_squared_error(y_test, y_test2, squared=False)
print("RMSE:", rmse)
mae = mean_absolute_error(y_test, y_test2)
print("MAE:", mae)

#預測
X_new = [[1, 5.8, 3.1 , 5, 1.7]]  #添加常數項1
y_pred = RF.predict(X_new)
print(y_pred)"""

class MLP:
    def get(self):
        return """import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, r2_score, mean_squared_error, mean_absolute_error

from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target

#拆分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

#建立、編譯、訓練模型
RF = Sequential()
RF.add(Dense(10, input_dim=4, activation='relu'))
RF.add(Dense(3, activation='softmax'))
RF.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#RF.add(Dense(1, activation='linear'))  #迴歸
#RF.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])  #迴歸
RF.fit(X_train, y_train, epochs=200, batch_size=10)

#混淆矩陣 
y_test2 = RF.predict(X_test).argmax(axis=-1)  #將結果由機率轉成分類值
cm = confusion_matrix(y_test, y_test2)
print("混淆矩陣:", cm)

#分類報告
cr = classification_report(y_test, y_test2)
print("分類報告:", cr)

#分類
X_new = [[5.8, 3.1 , 5, 1.7]]
y_pred = RF.predict(X_new).argmax(axis=-1)
print(y_pred)"""

class SVM:
    def get(self):
        return """import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, r2_score, mean_squared_error, mean_absolute_error

from sklearn.svm import SVC
#from sklearn.svm import SVR  #迴歸
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target

#拆分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

#建立、訓練模型、超參數
RF = SVC(kernel='linear')
# RF = SVC(kernel='poly')
# RF = SVC(kernel='rbf')
RF.fit(X_train, y_train)
print(RF.get_params())

#混淆矩陣
y_test2 = RF.predict(X_test)
cm = confusion_matrix(y_test, y_test2)
print("混淆矩陣:", cm)

#分類報告
cr = classification_report(y_test, y_test2)
print("分類報告:", cr)

#分類
X_new = [[5.8, 3.1 , 5, 1.7]]
y_pred = RF.predict(X_new)
print(y_pred)"""

class other:
    def get(self):
        return """混淆矩陣的列是實際值、欄是預測值，對角線上的數字代表被正確預測的樣本數，非對角線上的數字代表被錯誤預測的樣本數。
precision＝正確預測的樣本數/預測的樣本數，例如precision(類別0)＝5/(5+0+3)＝0.62。
f1-score＝所有正確預測的樣本數/所有預測的樣本數＝(5+1+3)/(5+1+2+0+1+4+3+1+3)＝0.45。

分類問題共有三個類別，分別為0、1、2。混淆矩陣顯示，類別0有5個樣本被正確預測，1個樣本被誤判為類別1，2個樣本被誤判為類別2。類別1有1個樣本被正確預測，4個樣本被誤判為類別2。類別2有3個樣本被正確預測，3個樣本被誤判為類別0，1個樣本被誤判為類別1。
分類報告顯示，模型的精確率為0.45，意味著模型在所有預測中有45%是正確的。對於每個類別而言，模型的精確率分別為0.62、0.33和0.33。此外，從recall和f1-score來看，模型對於類別0的表現較好，但對於其他兩個類別的表現則比較差。從特徵重要性表可以看出，這個隨機森林分類器中特徵C的重要性最高，其次是特徵D，最後是特徵B。

Bagging是一種集成學習方法，通過從原始數據中有放回的隨機抽樣，生成多個互相獨立的樣本集，分配給不同的子模型進行訓練，最後再將各子模型的結果合併為最終預測。Bagging可以降低過擬合（overfitting）的風險，提高模型的泛化能力，特別是對於高變異（high-variance）的模型更為有效。Bagging 利用多個基學習器的平均或投票來達到降低方差的目的，由於基學習器之間是相互獨立的，因此每個基學習器的權重是相同的，不會調整樣本的權重。

Boosting是一種集成學習方法，通過依次訓練多個弱分類器，並根據前一個分類器的誤差加權調整樣本權重，使得後一個分類器能夠更加關注先前分類錯誤的樣本，逐漸提高模型的預測性能，生成一個強的分類器，對於高偏差（high-bias）的模型有較好的效果，但也更容易出現過擬合的情況。高變異意味著模型太複雜，高偏差意味著模型太簡單。

隨機森林：
n_estimators：決策樹的數量，100到1000。
max_depth：決策樹的最大深度，5到50，若數據集較小，可選較小值，否則可選較大值。
max_features：每棵決策樹使用的最大特徵數量，總特徵數的平方根或三分之一。
min_samples_split：每個內部節點所需的最小樣本數，2到20。
min_samples_leaf：每個葉子節點所需的最小樣本數，1到10。

XGBoost：
n_estimators: 決策樹的數量，50到1000。
max_depth: 決策樹的最大深度，3到10。
subsample: 每棵樹使用的樣本比例，0.5到 1。
colsample_bytree: 每棵樹使用的特徵比例，0.5到 1。
reg_lambda: L2正則化參數，0到10。
learning_rate: 學習率，0.01到 0.2，較小的學習率可以使模型更穩定，但可能需要更多的迭代次數。

CatBoost：
n_estimators: 決策樹的數量，50到5000。
max_depth: 決策樹的最大深度，3到16。
subsample: 每棵樹使用的樣本比例，0.1到1。
colsample_bylevel: 每層樹使用的特徵比例，0.1到1。
l2_leaf_reg: L2正則化參數，0到10。
learning_rate: 學習率，0.001到0.5。

LightGBM：
num_leaves: 每棵決策樹的葉子數量，20到100。
max_depth: 決策樹的最大深度，5到20。
min_data_in_leaf: 每個葉子節點所需的最小樣本數，10到100。
bagging_fraction: 每棵樹使用的樣本比例，0.5到1。
feature_fraction: 每棵樹使用的特徵比例，0.5到1。
learning_rate: 學習率，0.01到0.1。

cd OneDrive，退出：cd ..，python 123.py
excel的資料分析：檔案、選項、增益集、執行

線性模型的調整後配適度為0.8，估計的X係數為 0.5，於1%水準下顯著，表示在其他條件相同下，X每增加1，Y會增加約0.5。

由於均數迴歸模型估計的是被解釋變數的條件均數，只能觀察解釋變數對於被解釋變數的平均邊際效果，無法完整描述外匯存底在三難指標總和之條件分配中可能出現的異質性。因此，本文再使用分量迴歸模型，並且以九個條件分量(0.1, 0.2, 0.3, 0.4, 0.5, 0.6,0.7, 0.8, 0.9)，觀察解釋變數對被解釋變數在每個特定分量的邊際效果，延伸解釋外匯存底對於不同三難指標總和水準之下的影響程度。

若以分量迴歸模型來看，不同條件分量的X係數大致為正向影響，若與OLS估計值相比，分量迴歸的估計值在Y分配的右尾有些差異，顯示平均邊際效果有高估或低估的情形。

Slide 1：封面。

Slide 2：內容大綱。

Slide 3：什麼是R2？
    被解釋變數的變異可由解釋變數解釋的比例，反映模型的解釋力。
    R2愈接近1，模型的解釋能力愈強。
    例如：建立一個預測房價的迴歸模型，發現模型的R2為0.8，這意味著模型能夠解釋80%的房價波動，剩下20%的波動可能來自於其他因素。

Slide 4：如何提高R2？資料處理方面
    去除重複、錯誤、與被解釋變數無關的資料。
    處理缺失值，選擇直接删除或使用統計、計量、機器學習方法估計並填補。
    處理極端值，選擇直接删除或使用分量迴歸、聚類模型等方法分段分析。
    將資料對數變換、平方根變換、標準化，使資料符合模型假設分配。

Slide 5：如何提高R2？解釋變數方面
    去除相關性或顯著性較低的變數。
    加入由兩個或多個變數形成的交叉項，進而捕捉變數之間的交互作用。
    加入虛擬變數，可增加解釋不同類別對被解釋變數的影響。
    將一個或多個變數作為工具變數，可改善模型的內生性問題。

Slide 6：如何提高R2？模型參數方面
    樹的深度可以控制模型的複雜度。
    學習率可以影響模型的收斂速度。
    使用交叉驗證、網格搜索選擇最優參數組合。

Slide 7：提高R2的注意事項
    使用正則化降低模型複雜度，避免過度擬合。
    當模型不含截距項時，R2不再適當且無意義。
    綜合考量其他指標，例如調整後R2、均方根誤差RMSE、平均絕對誤差MAE。

Slide 8：總結"""

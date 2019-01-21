import datetime
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QFont


data = pd.read_csv('Data/MER_T12_06.csv')
Coal = data[data.Column_Order == 1]
Coal = Coal[(Coal.YYYYMM-13) % 100 != 0]
Coal = Coal[Coal.YYYYMM < 200401]

NGas = data[data.Column_Order == 2]
NGas = NGas[(NGas.YYYYMM-13) % 100 != 0]
NGas = NGas[NGas.YYYYMM < 201601]
NGas = NGas[NGas.YYYYMM > 198901]

NGas.Value = NGas.Value.astype(float)
NGas.YYYYMM = [datetime.date(year = i // 100, month = i % 100, day = 1) for i in NGas.YYYYMM]
NGasTrain = NGas
NGasTrain = NGasTrain[NGasTrain.YYYYMM < datetime.date(2005, 1, 1)]
NGasTrain = NGasTrain.drop(['MSN','Column_Order','Description','Unit'], axis = 1)
NGasTrain = NGasTrain.set_index(NGasTrain.YYYYMM)
NGasTrain.YYYYMM = [str(i) for i in NGasTrain.YYYYMM]
NGasTrain = NGasTrain.drop(['YYYYMM'], axis =1)
print(NGasTrain)

model = SARIMAX(NGasTrain,
              order=(1,1,1),
              seasonal_order=(0,1,1,12),
              enforce_stationarity=False,
              enforce_invertibility=False)


def prediction(date):
    return model.predict(date)

def test(string):
    return string*3

class PredictApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('ComicSans', 10))

        self.setToolTip('Введите дату в формате ГГГГ.ММ.ДД')

        btn = QPushButton('Предсказать', self)
        btn.setToolTip('ПЫЩЬ!')
        btn.resize(btn.sizeHint())
        btn.move(220, 170)

        header = QLabel(self)
        header.setText('Предсказание выбросов СО2')
        header.move(70, 10)

        lbl = QLabel(self)
        lbl.move(90, 40)
        lbl.setText('57.5 миллионов тонн')

        qle = QLineEdit(self)
        qle.move(80, 110)

        btn.clicked.connect(self.onChanged)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Vanga Ex Machina: CO2 edition')
        self.show()

    def onChanged(self):
        text = prediction(str(self.qle.text()))
        self.lbl.SetText(str(text) + ' миллионов тонн')




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = PredictApp()
    sys.exit(app.exec_())
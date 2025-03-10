import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Labs/Cardio/cardio_train.csv', delimiter=';')

df['BMI'] = df['weight'] / (df['height']/100)**2

low = df[df['BMI'] < 17]
high = df[df['BMI'] > 45]
#Valde dessa gränser för att utesluta extrema värden men kan ändå bevara ca 99% av datan
#Jag kommer ändå kunna klassificera alla klasser från underweight(Tycker den är relevant även om det inte framkommer i uppgiften) till obese

df = df.drop(index=[*low.index, *high.index])
# print(len(low), len(high), len(df))
#df['BMI'].hist(bins=100)
#plt.show()

bins = [0, 18.5, 25, 30, 35, 40, 100]
labels = ['Underweight', 'Normal', 'Overweight', 'Obese 1', 'Obese 2', 'Obese 3']

df['BMI_class'] = pd.cut(df['BMI'], bins, labels=labels)

df['BMI_class'].hist(bins=100)
plt.show()

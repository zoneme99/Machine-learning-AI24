import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Labs/Cardio/cardio_train.csv', delimiter=';')

def BMI_features(df):
    df['BMI'] = df['weight'] / (df['height']/100)**2

    low = df[df['BMI'] < 17]
    high = df[df['BMI'] > 38]
    #Valde dessa gränser för att utesluta extrema värden men kan ändå bevara ca 95% av datan
    #Gränserna valde jag genom att kolla på boxplots och flyttade gränserna tills jag inte hade några outliers kvar
    #Jag kommer ändå kunna klassificera alla klasser från underweight(Tycker den är relevant även om det inte framkommer i uppgiften) till obese

    df = df.drop(index=[*low.index, *high.index])
    #plt.boxplot(df['BMI'])
    #plt.show()
    
    #print(len(low), len(high), len(df))
    #df['BMI'].hist(bins=100)
    #plt.show()

    bins = [0, 18.5, 25, 30, 35, 40, 100]
    labels = ['Underweight', 'Normal', 'Overweight', 'Obese 1', 'Obese 2', 'Obese 3']

    df['BMI_class'] = pd.cut(df['BMI'], bins, labels=labels)
    #print(len(df[df['BMI_class'] == 'Underweight']))
    return df

def blood_pressure(df):
    #Uteslut outliers, Utför samma procedur genom att plotta boxplots och justera gränser tills det att jag inte ser outliers längre
    outlier1 = df[(df['ap_lo'] > 105) | (df['ap_lo'] < 65)]
    outlier2 = df[(df['ap_hi'] > 170) | (df['ap_hi'] < 88)]
    df = df.drop(index=[*outlier1.index,*outlier2.index])

    #Gränserna för varje kategori läser jag av från tabellen given genom att göra en funktion med alla dess intervall och logiska uttryck
    def blood_category(hi, lo):
        if hi < 120 and lo < 80:
            return 'Healthy'
        elif 120 <= hi < 130 and lo < 80:
            return 'Elevated'
        elif 130 <= hi < 140 or 80 <= lo < 90:
            return 'Stage 1 Hypertension'
        elif 140 <= hi < 180 or 90 <= lo < 120:
            return 'Stage 2 Hypertension'
        else:
            return 'Hypertension Crisis'
    
    df['blood_pressure'] = df.apply(lambda row: blood_category(row['ap_hi'], row['ap_lo']), axis=1)

    
    #fig, axes = plt.subplots(1,2)
    #df['ap_lo'].hist(ax=axes[0], bins=100)
    #df['ap_hi'].hist(ax=axes[1], bins=100)
    #axes[0].boxplot(df['ap_lo'])
    #axes[1].boxplot(df['ap_hi'])
    #plt.show()
    return df

print(len(df))
df = BMI_features(df)
df = blood_pressure(df)
print(len(df))
print(df[df['blood_pressure'] == 'Healthy'])


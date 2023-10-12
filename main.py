import pandas as pd
import matplotlib.pyplot as plt

# https://www.kaggle.com/datasets/groundhogclub/groundhog-day
df = pd.read_csv('groundhog_day.csv')

print('Quais são as colunas presentes nessa base de dados?')
print(df.columns, end="\n\n")

print('É possível trocar o nome dessas colunas para algo de fácil compreensão/acesso?'
)
new_names = ['year', 'shadow', 'all_feb_avg', 'north_feb_avg', 'mid_feb_avg', 'penn_feb_avg', 'all_mar_avg', 'north_mar_avg', 'mid_mar_avg', 'penn_mar_avg']
# Modificando o nome das colunas do dataframe para facilitar o acesso posteriormente
df.rename(columns={df.columns[i]: new_names[i] for i in range(len(df.columns))}, inplace=True)
print(df.columns, end="\n\n")

# Mostrando descrição estatística do dataframe
print(df.describe(), end="\n\n")

# Mostrando tipos de valores e a contagem de valores não nulos por colunas do dataframe
print(df.info(), end="\n\n")

print('Há registros com informações faltantes na base de dados?')
print(df[df.isna().any(axis=1)])
# Removendo as linhas que contém valores faltantes e resetando o índice para a coluna de ano
df.dropna(axis=0, how='any', inplace=True)
df.year = df.year.astype(int)
df.set_index('year', inplace=True)
print(df.head(), end="\n\n")

print('Quais são as categorias presentes na coluna "shadow"?')
print(df.shadow.value_counts(), end="\n\n")
# Alterando os valores da coluna "shadow" para retirar os espaços e colocá-los com letras minúsculas
df.shadow = df.shadow.apply(lambda x: str.replace(x, ' ', '_').lower())
print(df.shadow.value_counts(), end="\n\n")

print('Qual a média da temperatura nos meses de fevereiro entre 1895 a 2016 em todas as regiões?')
T = df.all_feb_avg.sum() / df.shape[0]
print(f"T = {T:.3f}ºF = {(T - 32) * 5 / 9:.3f}ºC", end="\n\n")

print('Qual a variação média, entre os meses de março e fevereiro de um mesmo ano, da temperatura média de todas as regiões?')
var = ((df.all_mar_avg - df.all_feb_avg) / df.all_feb_avg).sum() / df.shape[0]
print(f"Variação = {var:.3%}", end="\n\n")

print('Qual a média das temperaturas médias de fevereiro das 3 regiões, por ano?')
df['three_regions_feb_avg'] = df[['north_feb_avg', 'mid_feb_avg', 'penn_feb_avg']].mean(axis=1)

print('Qual o desvio padrão das temperaturas médias de março das 3 regiões, por ano?')
df['three_regions_mar_std'] = df[['north_mar_avg', 'mid_mar_avg', 'penn_mar_avg']].std(axis=1)

# Mostrando as duas novas colunas
print(df.head(), end="\n\n")

print('Quais anos não possuem informação sobre a sombra avistada?')
print(df.query('shadow == "no_record"'))

print('Como as médias de temperaturas anuais de fevereiro e março se comparam pelas categorias em "shadow"?')
print(df.groupby('shadow')[['all_feb_avg', 'all_mar_avg']].mean(), end="\n\n")

print('Pode-se salvar os dados modificados como uma nova base de dados?')
df.to_csv('saved_dataframe.csv')

print('Como se comparam as médias de temperaturas de todas as regiões, em fevereiro e março, por ano?')
plt.plot(df[['all_feb_avg', 'all_mar_avg']])
plt.title('Average Temperatures by Month between 1895-2016')
plt.legend(['Feb', 'Mar'])
plt.xlabel('Year')
plt.ylabel('Average Temperatures (ºF)')
plt.show()
plt.clf()

print('Como se comparam as médias de temperaturas de todas as regiões, em fevereiro e março, por década?')
df['decade'] = pd.cut(df.index, bins=[i for i in range(1890, 2021, 10)], labels=[i for i in range(1890, 2020, 10)])
cut_df_by_decade = df.groupby('decade')[['all_feb_avg', 'all_mar_avg']].mean()
cut_df_by_decade.index = cut_df_by_decade.index.astype(float)
plt.bar(cut_df_by_decade.index - 1, cut_df_by_decade.all_feb_avg, 2)
plt.bar(cut_df_by_decade.index + 1, cut_df_by_decade.all_mar_avg, 2)
plt.title("Average Temperatures by Month by Decade")
plt.legend(['Feb', 'Mar'])
plt.xlabel('Decade')
plt.ylabel('Average Temperatures (ºF)')
plt.xticks(cut_df_by_decade.index, [i for i in range(1890, 2020, 10)], rotation=45)
plt.subplots_adjust(bottom=0.15)
plt.show()
plt.clf()

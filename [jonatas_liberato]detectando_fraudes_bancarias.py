# -*- coding: utf-8 -*-
"""[JONATAS-LIBERATO]detectando-fraudes-bancarias.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fK6D7V4-MaLzOlT-ICXowtLdikL_icG3

# **DETECÇÃO DE FRAUDES EM TRANSAÇÕES BANCÁRIAS**

# Sobre o problema

Infelizmente sabemos que as fraudes bancárias está no cotidiano do brasileiro, ainda mais em tempos de crise e para se ter uma noção de como anda difícil a vida do brasileiro, trago algumas notícias:

*Segundo um levantamento feito pela Serasa Experian mostrou que, em maio de 2021, um total de 331,2 mil brasileiros foram vítimas de algum tipo de fraude, sendo que mais de 176 mil ocorrências (53,3%) foram realizadas a partir de contas bancárias ou cartões de crédito. [Notícia](https://epocanegocios.globo.com/Brasil/noticia/2022/08/epoca-negocios-golpes-bancarios-disparam-e-devem-gerar-prejuizos-de-r-25-bilhoes-neste-ano.html)*

Fica claro que as instituições financeiras precisam investir em meios, principalmente tecnológicos, para se evitar as fraudes, pois o prejuízo não fica restrito somente ao consumidor. A instituição também sofre, pois é necessário fazer provisionamentos para arcar com os custos.

Uma prova da gravidade dos custos que as empresas enfrentam com esses crimes estão nesta matéria do **Bradesco**:

*"O tombo do primeiro trimestre de 2020 foi causado pelo forte aumento de reservas para cobrir eventuais calotes, consequência dos danos econômicos acusados pelo coronavírus..." * [Notícia](https://br.financas.yahoo.com/noticias/bradesco-aumenta-reserva-contra-calotes-104800525.html)

# Base de dados

Usaremos uma base de dados fictícios de uma instituição financeira para construir uma máquina preditiva.

O dataset é composto por:
* com mais de 200mil registros
* 490 operações fraudulentas
* 28 variáveis (explicativas)
* 1 target

Link do dataset: [Aqui](https://www.dropbox.com/s/4yv3fk3hnu52aeb/transferencias.csv?dl=0) (~42mb)

# Objetivos

1. Análise exploratória para entender as distribuição dos dados
2. Verificaremos os tipos e a qualidade dos dados
3. Verificaremos existência de dados missing
4. Identificaremos a target e as variáveis explicativas
5. Examinaremos possíveis correlações
6. Vamos separar dados de teste e de treino
7. Construiremos máquinas preditivas para treinar modelos
8. Analisaremos resultados

# 1º Análise Exploratória
"""

# Bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Bibliotecas para pré-processamento
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

# Bibliotecas para avaliação de máquinas preditivas
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score

# Bibliotecas para máquinas preditivas
# Para fins de estudo, utilizaremos mais de uma
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
import xgboost as xgb
import lightgbm as lgb

# Ignorando os warnings
import warnings
warnings.filterwarnings('ignore')
sns.set(style = 'darkgrid')

# Base de dados
dataset = pd.read_csv('transferencias.csv')
dataset

df = pd.DataFrame(dataset)

# Tipos das variáveis
dataset.info()

# Valores contidos na variável Target
dataset['Target'].value_counts()

# Verificando no geral presença de dados mising
dataset.isna().sum()

# Verificando quantidade de missing no Target
dataset['Target'].isna().value_counts()

"""Como o dataset possui poucos valores missing para o target, a exclusão deste valor não acarretará em maiores problemas para a análise."""

# Eliminando valores missing
dataset.dropna(inplace = True)

dataset.isna().sum()

# Gerando um gráfico para conferir a distribuição
dataset['Target'].value_counts()
sns.countplot(dataset['Target'])

# Estudando a correlação do Target com as demais variáveis
dataset.corr()['Target'].sort_values(ascending = True)

dataset.corr(method='spearman')

# Gerando uma matrix de correlação
correlation = dataset.corr()
sns.set(rc = {'figure.figsize':(25,18)})
plot = sns.heatmap(correlation, annot = True, fmt=".2f", linewidths=.6)
plot

"""**Detectando outliers**"""

dataset.describe()

dataset['tempo_transacao'].describe()

dataset['lim_crt'].describe()

"""# 2º Pré-Processamento

**Separando o target das variáveis explicativas**

Notamos que há um desbalanceamento da classe (Target), faremos o seu tratamento durante esta parte do código
"""

x = dataset.drop(['Target'], axis=1)
y = dataset['Target']

# Balanceamento da classe do Target
# Essa função cria um oversampling (que são registros da classe positiva)
smt = SMOTE()

x, y = smt.fit_resample(x, y)

"""**Atenção**: aqui será necessário converter de float para int para podermos utilizar a função de contagem bincount()"""

cont = y.astype(int) #conversão
np.bincount(cont)

# Verificando o balanceamento
sns.set(rc={'figure.figsize':(11.7,8.27)})
ax = sns.countplot(x = cont)

"""**Separando os dados de treino e de teste**"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=7, stratify = y)

"""# 3º Criando as Máquinas Preditivas

Como citado anteriormente, com o propósito de estudos, utilizaremos mais de um avaliador para máquinas preditivas, relizando uma comparação entre estas.

**XGBoost**
"""

# Modelo
from xgboost import XGBClassifier
model = XGBClassifier()

# Treinando o modelo
modelo = model.fit(x_train, y_train)
modelo

y_preditor = model.predict(x_test)

"""**Avaliação**

Para avaliarmos a eficácia dessa máquina, criamos um rascunho para realizarmos um comparativo.
"""

rasc = pd.DataFrame({'Resultado Rascunho: ': y_test, 'Previsões da Máquina: ': y_preditor})
rasc

"""**Métricas**"""

print('Classificação: \n', classification_report(y_test, y_preditor))
print('--------------------------- \n')
print('Acurácia: \n', accuracy_score(y_test, y_preditor))
print('--------------------------- \n')
print('Matrix de Confusão: \n', confusion_matrix(y_test, y_preditor))

"""*Valores bemn próximos como vericado nas métricas precision, recall, f1-score e support*

--------

**LightGBM**
"""

dados_treino = lgb.Dataset(x_train, label = y_train)

param = {'num_leaves':1000,         # quantidade de folhas em uma árvore - padrão = 31; type = int
         'objective':'binary',     
         'max_depth':7,
         'learning_rate':.01,
         'max_bin':200}

param['mtric'] = ['auc', 'binary_logloss']

# Treinando o modelo com LitghGBM
num_round = 50
lgbm = lgb.train(param, dados_treino, num_round)

# Usando os novos dados de teste no modelo
y_preditor = lgbm.predict(x_test)

"""**Avaliação**"""

rasc = pd.DataFrame({'Resultado Rascunho: ': y_test, 'Previsões da Máquina: ': y_preditor})
rasc

# Tamanho do Preditor
y_preditor.size

"""Acima foram mostradas probabilidades em **Previsões da Máquina**, para verificar as probabilidades, usaremos a seguinte regra:
* Acima de .5 ou (50%) = é fraude
* Abaixo de .5 ou (50%) = não é fraude

**[Lembrete]** É possível aprimorar ainda mais a acurácia, por exemplo:
Acima de **.8** ou (80%) deprobabilidade de ser fraude   
"""

# Criando as Probabilidades entre 0 e 1
for i in range(0,170589):
  if y_preditor[i] >= .5:
     y_preditor[i] = 1 # Fraude
else:
  y_preditor[i] = 0 # Não é fraude

"""**Métricas**"""

print('Classificação: \n', classification_report(y_test, y_preditor))
print('--------------------------- \n')
print('Acurácia: \n', accuracy_score(y_test, y_preditor))
print('--------------------------- \n')
print('Matrix de Confusão: \n', confusion_matrix(y_test, y_preditor))

"""*Este modelo também apresentou uma acurácia muito alto, idêntica a do XGBoost.*

------

**RandomForest**
"""

# Construindo o modelo
model = RandomForestClassifier()

# Treinando o modelo com RandomForest
modelo = model.fit(x_train, y_train)
modelo

# Usando os novos dados de teste no modelo
y_preditor = lgbm.predict(x_test)

"""**Avaliação**"""

rasc = pd.DataFrame({'Resultado Rascunho: ': y_test, 'Previsões da Máquina: ': y_preditor})
rasc

"""**Métricas**"""

print('Classificação: \n', classification_report(y_test, y_preditor))
print('--------------------------- \n')
print('Acurácia: \n', accuracy_score(y_test, y_preditor))
print('--------------------------- \n')
print('Matrix de Confusão: \n', confusion_matrix(y_test, y_preditor))

"""# Conclusão:

- Apesar da grande proximidade entre as avaliações dos modelos, XGBoost se mostrou mais eficaz para esses dados. 

- Além disso, é possível aumentar a faixa para avaliar as probabilidades de fraude ou não.

- Apesar de um projeto simples, algumas técnicas de avaliação foram bem implementadas.
"""

#Autor: Jonatas A. Liberato
#Ref: Eduardo Rocha
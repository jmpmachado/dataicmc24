import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

path = './iris.data'  # Caminho relativo para o arquivo iris.data

class Modelo():
    def __init__(self):
        self.svm_model = None
        self.lr_model = None
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def CarregarDataset(self, path):
        """
        Carrega o conjunto de dados a partir de um arquivo CSV.
        """
        names = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']
        self.df = pd.read_csv(path, names=names)

    def TratamentoDeDados(self):
        """
        Realiza o pré-processamento dos dados carregados.
        """
        # Visualiza as primeiras linhas do dataset
        print(self.df.head())

        # Verifica se existem valores ausentes
        print(self.df.isnull().sum())

        # Codifica as labels de 'Species' para valores numéricos
        label_encoder = LabelEncoder()
        self.df['Species'] = label_encoder.fit_transform(self.df['Species'])

        # Visualiza a distribuição dos dados com um gráfico
        sns.pairplot(self.df, hue='Species')
        plt.show()

    def Treinamento(self):
        """
        Treina tanto o modelo SVM quanto o modelo de Regressão Linear.
        """
        # Separa as variáveis independentes (X) e a dependente (y)
        X = self.df.drop(columns='Species')
        y = self.df['Species']

        # Divide os dados em treino e teste (80% treino, 20% teste)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treinamento do modelo SVM
        self.svm_model = SVC(kernel='linear')  # Modelo SVM com kernel linear
        self.svm_model.fit(self.X_train, self.y_train)

        # Treinamento do modelo de Regressão Linear
        self.lr_model = LinearRegression()  # Modelo de Regressão Linear
        self.lr_model.fit(self.X_train, self.y_train)

    def Teste(self):
        """
        Avalia o desempenho de ambos os modelos nos dados de teste e compara os resultados.
        """
        # Previsões no conjunto de teste para SVM
        y_pred_svm = self.svm_model.predict(self.X_test)

        # Previsões no conjunto de teste para Regressão Linear
        y_pred_lr = self.lr_model.predict(self.X_test)

        # Avaliação do modelo SVM
        print("\nAvaliação do modelo SVM:")
        accuracy_svm = accuracy_score(self.y_test, y_pred_svm)
        print(f"Acurácia (SVM): {accuracy_svm:.4f}")
        print("Relatório de Classificação (SVM):")
        print(classification_report(self.y_test, y_pred_svm))

        # Avaliação do modelo de Regressão Linear
        print("\nAvaliação do modelo de Regressão Linear:")
        r2_lr = self.lr_model.score(self.X_test, self.y_test)
        print(f"R² (Regressão Linear): {r2_lr:.4f}")

        # Análise das diferenças
        print("\nAnálise das diferenças:")
        print("O modelo SVM é adequado para problemas de classificação, portanto a métrica de acurácia é importante.")
        print("Já o modelo de Regressão Linear, embora também tenha sido treinado, é mais adequado para problemas de regressão.")
        print(f"Se a acurácia do SVM for muito alta, pode indicar overfitting, o que pode ser investigado com validação cruzada.")
        print(f"Se o R² da Regressão Linear for baixo, isso pode indicar que o modelo não se ajustou bem aos dados para um problema de classificação.")

    def ValidacaoCruzada(self):
        """
        Realiza a validação cruzada para ambos os modelos.
        """
        # Separa as variáveis independentes (X) e a dependente (y)
        X = self.df.drop(columns='Species')
        y = self.df['Species']

        # Validação cruzada para o modelo SVM
        scores_svm = cross_val_score(self.svm_model, X, y, cv=5)  # 5-fold cross-validation
        print(f"\nScores de Validação Cruzada (SVM): {scores_svm}")
        print(f"Acurácia média (SVM): {scores_svm.mean():.4f}")

        # Validação cruzada para o modelo de Regressão Linear
        scores_lr = cross_val_score(self.lr_model, X, y, cv=5)  # 5-fold cross-validation
        print(f"\nScores de Validação Cruzada (Regressão Linear): {scores_lr}")
        print(f"Acurácia média (Regressão Linear): {scores_lr.mean():.4f}")

    def Train(self):
        """
        Função principal para o fluxo de treinamento do modelo.
        """
        self.CarregarDataset(path)  # Carrega o dataset especificado

        # Tratamento de dados
        self.TratamentoDeDados()

        # Treinamento dos modelos
        self.Treinamento()

        # Teste dos modelos
        self.Teste()

        # Realizando validação cruzada
        self.ValidacaoCruzada()

# Criando e treinando o modelo
modelo = Modelo()
modelo.Train()

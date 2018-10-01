import os
import numpy as np

"""
A partir de um arquivo de texto, lê-se os dados
do dataset na memória

Args:
	filepath: diretório do arquivo

Retorno:
	dataset: lista (matriz) com os elementos do dataset
"""
def read_dataset(filepath):
	print("Arquivo de entrada:", filepath)
	with open(filepath) as f:
		return [list(map(float, x.split(","))) for x in f.readlines()]


"""
Gera-se aleatóriamente um conjunto de treinamento e outro de teste

Args:
	dataset: lista (matriz) com os elementos do dataset
	train_size: tamanho do conjunto de teste

Retorno:
	train: conjunto de treinamento
	test:  conjunto de teste
"""
def generate_sets(dataset, train_size):
	np.random.shuffle(dataset)
	train = dataset[:train_size]
	test = dataset[train_size:]
	return train, test


"""
Função de ativação

Args:
	x: valor de entrada

Retorno:
	Valor 0 ou 1
"""
def activation_fn(x):
	return 1 if x >= 0 else 0


"""
Função de treinamento do perceptron

Args:
	training_set: conjunto de treinamento

Retorno:
	weights: pesos aprendidos
"""
def perceptron(training_set):
	# parâmetros do perceptron
	learning_rate = 0.05
	epochs = 100

	# inicialização das estrturas do algoritmo
	weights = np.random.rand(len(training_set[0])-1)
	errors = []

	# iterações (épocas)
	for t in range(epochs):
		avg_error = 0
		for i in range(len(training_set)):
			sample = training_set[i][:-1]  # elemento
			label = training_set[i][-1]    # rótulo

			result = np.dot(sample, weights) # prod. escalar entre os pesos e os atrib. do elem.
			error = label - activation_fn(result) # erro (rótulo esperado - encontrado)

			if error != 0:
				avg_error += 1
				# em caso de erro, atualizamos os pesos
				for j in range(len(weights)):
					weights[j] += learning_rate * error * sample[j]

		errors.append(avg_error)

	# exibi-se os valorer dos erros ao usuário
	print("Erro do treinamento (por iteração):", errors)

	return weights


"""
Função que aplica os pesos ao conjunto de teste.
Ao término da execução, reporta-se o erro.

Args:
	test_set: conjunto de teste
	weights:  pesos obtidos pelo treinamento do perceptron
"""
def run_test(test_set, weights):
	avg_error = 0
	for i in range(len(test_set)):
		sample = test_set[i][:-1]         # elemento 
		label = test_set[i][-1]           # rótulo
		result = np.dot(sample, weights)  # prod. escalar entre os pesos e os atrib. do elem.
		error = label - activation_fn(result) # erro (rótulo esperado - encontrado)
		if error != 0:  # se necessário, incrementamos o erro
			avg_error += 1

	# exibi-se o valor do erro ao usuário
	print("Erro no conjunto de teste: ", avg_error)


if __name__ == "__main__":
	# leitura do dataset a partir do arquivo
	dataset = read_dataset("iris_data.txt")

	# geram-se os conjuntos de treinamento e de teste
	train_size = 25
	train, test = generate_sets(dataset, train_size)

	# realiza-se o treinamento
	weights = perceptron(train)

	# executa-se o teste e reporta-se os erros
	run_test(test, weights)

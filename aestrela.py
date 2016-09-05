# This Python file uses the following encoding: utf-8
import random
import math
import numpy as np

tamanhoGrafo = 10 #quantidade de cidades

DLRs = [[0 for x in range(tamanhoGrafo)] for y in range(tamanhoGrafo)]
distancias = [[0 for x in range(tamanhoGrafo)] for y in range(tamanhoGrafo)]

#vou gerar aleatoriamente a heurística da distância em linha reta
for origem in range(0, tamanhoGrafo):
	for destino in range (0, origem):
		if (origem == destino):
			DLRs[origem][destino] = DLRs[destino][origem] = 0
		else:
			DLRs[origem][destino] = DLRs[destino][origem] = random.randint(10, 100)
print ('Distâncias em linha reta:')
print(np.matrix(DLRs))

#e aqui as distâncias reais, garantindo que sejam pelo menos iguais à DLR
for origem in range(0, tamanhoGrafo):
	for destino in range (0, origem):
		if(origem != destino):
			distancias[origem][destino] = distancias[destino][origem] = random.randint(DLRs[origem][destino], 200)
		else:
			distancias[origem][destino] = distancias[destino][origem] = 0

#aqui eu desconecto aleatoriamente algumas cidades (tem o limite de cidades desconectadas)
#pode acabar desconectando menos por terem saído índices iguais
limite = int(round(2*math.sqrt(tamanhoGrafo), 0))
for i in random.sample(range(0, tamanhoGrafo), limite):
	for j in random.sample(range(0, tamanhoGrafo), limite):
		if(i != j):
			distancias[i][j] = distancias[j][i] = -1

print ('Distâncias reais (-1 representa a ausência de caminho)')
print(np.matrix(distancias))

#aqui sorteio a origem e destino
de_para = random.sample(range(0, tamanhoGrafo), 2)
partida = de_para[0]
chegada = de_para[1]

print ('Origem e destino:')
print de_para

#crio as listas que armazenarão o progresso do algoritmo
abertas = list()
fechadas = list()
caminho = [0 for x in range(tamanhoGrafo)]
custos = [0 for x in range(tamanhoGrafo)]

#e inicializo já com a partida
abertas.append(partida)
indiceM = partida

while len(abertas) != 0:
	menorCusto = 100000 #declaro esse menor custo enorme só pra comparação
	print('abertas')
	print abertas
	for i in abertas:
		if (custos[i] + DLRs[i][chegada]) < menorCusto:
			menorCusto = (custos[i] + DLRs[i][chegada])
			indiceM = i
	atual = indiceM #aqui consegui descobrir qual o menor custo g + h dentre os nós abertos

	print('atual')
	print atual
	if (atual == chegada): #se eu tiver chegado calculo o caminho até ali e saio do while
		indice = caminho[atual]
		print('caminho')
		print caminho
		custoTotal = distancias[indice][chegada] #aqui simula um do while (não tem em python)
		while indice != partida and indice != caminho[indice]:	#o valor presente no índice indica sua procedência
			custoTotal += distancias[indice][caminho[indice]]	#ex: caminho[5] = 6 significa que pra chegar na cidade 5 eu vim da 6
			print indiceM										#daí vou somando os custos reais entre essas cidades
			indice = caminho[indice]							#e tem que fazer isso de trás pra frente pra funcionar
		print('Custo total:')
		print custoTotal
		break #aqui saindo do while

	del abertas[abertas.index(atual)] 	#aqui eu tiro o nó atual das abertas e coloco nas fechadas
	fechadas.append(atual)				#porque se chegou aqui no código, então ainda não chegou no destino

	linhaAtual = [row[atual] for row in distancias] #aqui pego as distâncias reais da cidade atual (resgatei a linha da matriz de correlação)
	custoAtual = custos[atual] #e aqui recupero o custo acumulado até essa cidade atual

	for index, vizinhos in enumerate(linhaAtual):
		if (vizinhos != 0 and vizinhos != -1): #aqui to percorrendo todas as cidades vizinhas e calculando
			if (index not in fechadas): #só passo por uma cidade se ela não tiver sido fechada (evito ciclos)
				custoVizinho = linhaAtual[index] #pego a distância da atual pra essa
				if (index not in abertas): #se essa não tiver sido aberta ainda
					abertas.append(index) #eu abro
					custos[index] = (custoAtual + custoVizinho) #coloco que o custo dela é o acumulado até chegar nela
					caminho[index] = atual #e coloco a procedência
					#no vetor de caminhos, todos os nós abertos a partir do mesmo terão o mesmo valor
					#porém, como vou visitando de trás pra frente, pego apenas o caminho que chegou até ali mesmo
					#eu garanho isso colocando quem abriu aquele nó como procedência, independentemente dele estar conectado com outros

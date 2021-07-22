num_linhas, num_pontos = map(int, input().split())
matriz = [['0', '0', '0', '0', 'D'], ['0', 'A', '0', '0', '0'], ['0', '0', '0', '0', 'C'], ['R', '0', 'B', '0', '0']]

ponto_ini = input("Insira o ponto de início: ").upper()
ponto_fim = input("Insira o ponto de entrega: ").upper()

def calculo_distancia(num_linhas, num_pontos, ponto_ini, ponto_fim):
    cont1 = 0
    cont2 = 0
    x_ini = y_ini = 0
    x_fim = y_fim = 0
    while cont1 < num_linhas:
        while cont2 < num_pontos:
            if (matriz[cont1][cont2]) == ponto_ini:
                y_ini = cont1
                x_ini = cont2
                print("Início = ",y_ini, x_ini)
            elif (matriz[cont1][cont2]) == ponto_fim:
                y_fim = cont1
                x_fim = cont2
                print("Fim = ",y_fim, x_fim)
            cont2 += 1
        cont2 = 0
        cont1 += 1
    
    distancia = (abs(y_fim - y_ini) + abs(x_fim - x_ini))
    print("A distância do ponto", ponto_ini, "ao ponto", ponto_fim, "é de", distancia, "dronômetros.")

calculo_distancia(num_linhas, num_pontos, ponto_ini, ponto_fim)

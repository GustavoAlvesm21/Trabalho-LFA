#Codigo desenvolvido por: Gustavo Alves de Souza Marques, RGM:36133035

import json
import re
import random
from datetime import datetime, timedelta

class QualidadeDoArAutomato:
    def __init__(self):
        self.estado = "S0"  
        #Dicionario que armazena as trasições do automato e os parametros para as tais
        self.transicoes = {
            "S0": {"PM2.5": 50, "proximo": "S1"},
            "S1": {"PM2.5": 100, "proximo": "S2", "anterior": 50, "voltar": "S0"},
            "S2": {"PM2.5": 150, "proximo": "S3", "anterior": 100, "voltar": "S1"},
            "S3": {"PM2.5": 200, "proximo": "S4", "anterior": 150, "voltar": "S2"},
            "S4": {"anterior": 200, "voltar": "S3"}
        }
        #Dicionario que armazena os output's com base em cada estado do automato
        self.acoes = {
            "S0": "\033[1;32mQualidade do ar boa.\033[0m",
            "S1": "\033[1;92mQualidade do ar moderada. Tome cuidado.\033[0m",
            "S2": "\033[1;33mQualidade do ar ruim. Limite atividades ao ar livre.\033[0m",
            "S3": "\033[1;91mQualidade do ar muito ruim. Evite sair de casa.\033[0m",
            "S4": "\033[1;31mQualidade do ar perigosa. Emergência de saúde pública!\033[0m"
        }

    #Função que pega os dados e processa eles no automato
    def transicao(self, dados_json):
        nome = dados_json["Nome"]
        hora = dados_json["hora"]
        dados_poluição = dados_json["dados"][0]
        pm_value = float(dados_poluição["medida"])

        while True:
            limite_superior = self.transicoes[self.estado].get("PM2.5", float('inf'))
            limite_inferior = self.transicoes[self.estado].get("anterior", float('-inf'))
                
            if pm_value > limite_superior and "proximo" in self.transicoes[self.estado]:
                self.estado = self.transicoes[self.estado]["proximo"]
            elif pm_value <= limite_inferior and "voltar" in self.transicoes[self.estado]:
                self.estado = self.transicoes[self.estado]["voltar"]
            else: 
                break
        
        self.executar_acao(nome, hora)
    #Função que exibe os dados já processados
    def executar_acao(self,nome,hora):
        print('Região: '+nome + '\n' +'Horas: '+hora + '\n' + 'Situação: ' +self.acoes[self.estado])

#Função que abre os json's
def abrir_json(reg):

    nome = {1:"regiao_a.json",
            2:"regiao_b.json",
            3:"regiao_c.json",}
    
    for i, arq in nome.items():
        if i == reg:
            abrir = arq

    with open(abrir, 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    return dados

#Função que armazena e atualiza os dados dos json's das regioes
def atualiza_json(reg):
    nome = {1:"regiao_a.json",
            2:"regiao_b.json",
            3:"regiao_c.json"}
    
    for i, arq in nome.items():
        if i == reg:
            abrir = arq

    with open(abrir, 'r') as f:
        dados = json.load(f)
    
    numero_aleatorio = random.randint(0, 200)
    numero_aleatorio = str(numero_aleatorio)

    chave = 'dados'
    novo_valor = [
        {
            "PM": "PM2.5",
            "medida": numero_aleatorio
        }
    ]
    hora_atual = datetime.strptime(dados['hora'], '%H:%M')
    nova_hora = hora_atual + timedelta(hours=1)

    nova_hora_str = nova_hora.strftime('%H:%M')
    dados["hora"] = nova_hora_str
 

    dados[chave] = novo_valor

    with open(abrir, 'w') as f:
        json.dump(dados, f, indent=4)

    geral()

    return dados

#Função que armazena e atualiza os dados do geral.json
def geral():

    media = 0
    aux = 0

    with open('regiao_a.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    dados_poluição = dados["dados"][0]
    pm_value = float(dados_poluição["medida"])

    aux = aux + pm_value

    with open('regiao_b.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    dados_poluição = dados["dados"][0]
    pm_value = float(dados_poluição["medida"])

    aux = aux + pm_value

    with open('regiao_c.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    dados_poluição = dados["dados"][0]
    pm_value = float(dados_poluição["medida"])

    aux = aux + pm_value
    hora_atual = datetime.strptime(dados['hora'], '%H:%M')


    with open('geral.json', 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    media = aux/3
    media = str(media)

    nova_hora_str = hora_atual.strftime('%H:%M')
    dados["hora"] = nova_hora_str

    chave = 'dados'
    novo_valor = [
        {
            "PM": "PM2.5",
            "medida": media
        }
    ]

    dados[chave] = novo_valor

    with open('geral.json', 'w') as f:
        json.dump(dados, f, indent=4)

    return dados

#Função que valida a entrada do usuário
def valida_op():
    while True:
        op = input('Escolha uma opção: ')
        if op == '':
            print('\033[1;31mErro! opção escolhida é nula!\033[0m')
        elif re.match("^[1-3]*$",op):
            op = int(op)
            break
        else:
            print('\033[1;31mErro! Opção Invalida!\033[0m')

    return op

#Função que controla todo o codigo e também é responsável pela interação com o usuário
def main():

    ascii_art = """
  ______            _              _         _____            _   _            _ 
 |  ____|          | |       /\   (_)       / ____|          | | (_)          | |
 | |__ _ __ ___ ___| |__    /  \   _ _ __  | (___   ___ _ __ | |_ _ _ __   ___| |
 |  __| '__/ _ \ __| '_ \  / /\ \ | | '__|  \___ \ / _ \ '_ \| __| | '_ \ / _ \ |
 | |  | | |  __\__ \ | | |/ ____ \| | |     ____) |  __/ | | | |_| | | | |  __/ |
 |_|  |_|  \___|___/_| |_/_/    \_\_|_|    |_____/ \___|_| |_|\__|_|_| |_|\___|_|                                                                                
"""
    print('\n')
    print(ascii_art)

    while True:
        print('----------------------------------------------------------------------------------------------')
        print('1- Gerar novo relatorio de uma regiao \n2- Gerar relatorio geral \n3- Gerar relatorio da cidade')
        op = valida_op()

        if op == 1:
            atualiza_json(1)
            atualiza_json(2)
            atualiza_json(3)
            print('------------------------------------------------------')
            print('1- Zona industrial Sul \n2- Zona industrial Norte \n3- Zona residencial')
            reg = valida_op()
            dados_json = abrir_json(reg)
            print('------------------------------------------------------')
            if dados_json:
                automato_a = QualidadeDoArAutomato()
                automato_a.transicao(dados_json)
        elif op == 2:
            atualiza_json(1)
            atualiza_json(2)
            atualiza_json(3)
            dados_json = abrir_json(1)
            print('------------------------------------------------------')
            if dados_json:
                automato_a = QualidadeDoArAutomato()
                automato_a.transicao(dados_json)
            dados_json = abrir_json(2)
            print('------------------------------------------------------')
            if dados_json:
                automato_a = QualidadeDoArAutomato()
                automato_a.transicao(dados_json)
            dados_json = abrir_json(3)
            print('------------------------------------------------------')
            if dados_json:
                automato_a = QualidadeDoArAutomato()
                automato_a.transicao(dados_json)
        elif op == 3:
            dados_json = geral()
            print('------------------------------------------------------')
            if dados_json:
                automato_a = QualidadeDoArAutomato()
                automato_a.transicao(dados_json)
            
if __name__ == "__main__":
    main()

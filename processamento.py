import json
from os import chdir, makedirs,listdir, linesep ,path,getcwd
from default_paths import *
from datetime import datetime as dt
from string import capwords
from imagens import *
import qrcode as qr
def chave_pix():
    return "5802a211-c732-4d7a-a023-0b06da757174"
def pix_qrcode():
    return "00020126850014br.gov.bcb.pix01365802a211-c732-4d7a-a023-0b06da7571740223Ytalo Santos Aragao Dev5204000053039865802BR5919YTALO SANTOS ARAGAO6015NOSSA SENHORA D62240520GerencialFacilDoacao6304E949"
def gerar_qrcode(string):
    mudar_diretorio(config_path)
    qrcodepix = qr.make(string)
    qrcodepix.save("qrcode.png")
def busca_dic_keys(dic,busca):
    list_keys = []
    resultado = {}
    for key in dic:
        list_keys.append(key)
    for key_name in list_keys:
        if key_name.__contains__(busca):
            resultado.update({key_name:dic[key_name]})
    print("Lista de chaves: ",list_keys)
    print("Resultado: ",resultado)
    return resultado

#ler_Arquivo_json_para_python lê um arquivo json e retorna um dicionário python
def ler_arquivo_json_para_python(caminho):
    with open(caminho,encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados

#string_json lê arquivo para string em python e retorna a string json com identação
def string_json(caminho):
    dados = ler_arquivo_json_para_python(caminho)
    return json.dumps(dados,indent=4,ensure_ascii=False)

#string_para_arquivo recebe uma string json e um nome de arquivo e salva em arquivo json
def string_para_arquivo(string_dados,nome_arquivo):
    with open(nome_arquivo+".json","w",encoding="utf-8") as arquivo:
        arquivo.write(string_dados)
        arquivo.close()

#Gera os diretórios padrão
def gerar_default_paths():
    caminhos = [root_path, clients_path, products_path, reports_path,config_path]
    for caminho in caminhos :
            if not path.exists(caminho):
                makedirs(caminho)

#Gera os diretórios padrão e muda o diretório de trabalho para a raíz dos diretórios criados
def definir_working_directory_padrao():
    gerar_default_paths()
    chdir(root_path)

#Altera entre os diretórios padrões
def mudar_diretorio(dir):
    if (dir == root_path):
        chdir(root_path)
    elif (dir == clients_path):
        chdir(clients_path)
    elif (dir == products_path):
        chdir(products_path)
    elif (dir == reports_path):
        chdir(reports_path)
    elif (dir == config_path):
        chdir(config_path)

def salvar_cliente(string_dados,nome_arquivo):
    mudar_diretorio(clients_path)
    string_para_arquivo(string_dados,f"{nome_arquivo}_cliente")
    mudar_diretorio(root_path)

def salvar_produto(string_dados,nome_arquivo):
    mudar_diretorio(products_path)
    string_para_arquivo(string_dados,f"{nome_arquivo}_produto")
    mudar_diretorio(root_path)

def salvar_relatorio(string_dados,nome_arquivo):
    mudar_diretorio(reports_path)
    string_para_arquivo(string_dados,f"{nome_arquivo}_relatorio")
    mudar_diretorio(root_path)

def data_hora():
    dh = dt.now()
    return f"{dh.day}-{dh.month}-{dh.year}_{dh.hour}-{dh.minute}-{dh.second}"

def cadastrar_cliente(dicionario_dados):
    #Recebe um dicionário da interface gráfica ou CLI e salva em um arquivo
    #Usado para criar um cliente do zero (novo)
    dados_json = json.dumps(dicionario_dados,indent=4,ensure_ascii=False)
    salvar_cliente(dados_json,tratar_string_nome(dicionario_dados["nome"]))
#Implementar funções semelhantes para cada tipo de arquivo (relatorios, produtos)
#Comentar as funções para eu saber o que fazem antes que eu me confunda muito
def cadastrar_produto(dicionario_dados):
    dados_json = json.dumps(dicionario_dados, indent=4, ensure_ascii=False)
    salvar_produto(dados_json,tratar_string_nome(dicionario_dados["nome"]))

def gerar_relatorio_venda(relatorio_dicionario):
    return 0

def gerar_relatorio_dia(relatorio_dicionario):
    return 0

def index_listagem(caminho):
    return listdir(caminho)

def index_listbox(caminho):
    dicionario = {}
    lista = listdir(caminho)
    for i in range(len(lista)):
        if caminho == clients_path:
            dicionario[i+1] = capwords(lista[i].replace("_cliente.json","").replace("_"," "))
        elif caminho == products_path:
            dicionario[i+1] = capwords(lista[i].replace("_produto.json","").replace("_"," "))
        elif caminho == reports_path:
            dicionario[i+1] = capwords(lista[i].replace("_report.json","").replace("_"," "))
    return dicionario

def tratar_string_nome(nome):
    replacements = {
            "ã": "a", "â": "a", "á": "a", "à": "a",
            "ẽ": "e", "ê": "e", "é": "e", "è": "e",
            "ĩ": "i", "î": "i", "í": "i", "ì": "i",
            "õ": "o", "ô": "o", "ó": "o", "ò": "o",
            "ũ": "u", "û": "u", "ú": "u", "ù": "u",
            " ": "_"
        }
    name_final = nome.lower()
    for char, replacement in replacements.items():
        name_final = name_final.replace(char, replacement)
    return name_final
def gerar_lista(caminho):
    if caminho == clients_path:
        return listdir(caminho)
    elif caminho == reports_path:
        return listdir(caminho)

def numero_string(string):
    try:
        inteiro = int(string)
        return  inteiro
    except:
        try:
            if (string.__contains__(".") and string.__contains__(",")):
                decimal = float(string.replace(".","").replace(",","."))
                return decimal
            else:
                decimal = float(string.replace(",","."))
            return decimal
        except:
            return string

def vender(dicionario_venda):
    dados_relatorio_venda = {}
    nome_arquivo = data_hora()
    for produto in dicionario_venda:
        item = produto
        quantidade = dicionario_venda[item]
#venda = {"saco_de_sal_25kg":5,"produto":"n/a"}
#vender(venda)
#valor = "10000000000,654"
#print(f"Valor2: {valor} Tipo: {type(valor)}")
#print(valor,numero_string(valor))
#print(index_listagem(products_path))

#busca_dic_keys(dicionario,"soja")
#gerar_default_paths()
#dicionario = {"nome":"Ytalo Santos Aragão Silva","exemplo":"dicionário"}
#cadastrar_cliente(dicionario)
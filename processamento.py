import json
from os import chdir, makedirs,listdir, linesep ,path,getcwd
from default_paths import *
from datetime import datetime as dt
from string import capwords
from imagens import *
import qrcode as qr
from pyperclip import copy as to_clipboard
from sys import platform
from base64 import b64decode as b64dc
from io import BytesIO
from PIL import Image
from re import sub
def chave_pix():
    return "5802a211-c732-4d7a-a023-0b06da757174"
def pix_qrcode():
    return "00020126850014br.gov.bcb.pix01365802a211-c732-4d7a-a023-0b06da7571740223Ytalo Santos Aragao Dev5204000053039865802BR5919YTALO SANTOS ARAGAO6015NOSSA SENHORA D62240520GerencialFacilDoacao6304E949"
#Gera os ícones para cada uma das plaraformas
#e retorna o ícone adequado para a plataforma atual
def gerar_icones():
    mudar_diretorio(config_path)
    icones = [icon_linux,icon_windows,icon_mac,icon_bitmap]
    formatos = ["png","ico","icns","bmp"]
    imagem = Image.open(BytesIO(b64dc(program_icon())))
    for icon in icones:
        iconfile = imagem
        formato_index = icones.index(icon)
        iconfile.save(icon,format=str(formatos[formato_index]))
    if platform.lower() == "linux":
        return icon_linux
    elif platform.lower() == "windows":
        return icon_windows
    elif platform.lower() == "darwin":
        return icon_mac
    else:
        return icon_linux
#Gera o arquivo de QRCode a partir da string
def gerar_qrcode():
    string = pix_qrcode()
    mudar_diretorio(config_path)
    qrcodepix = qr.make(string)
    qrcodepix.save("qrcode.png")
#Mapeia um um diretório para um dicionário:
#<nome_cliente_ou_produto>:<nome_do_arquivo>
#Somente com as chaves que passam pelo filtro
def mapa_arquivos(filtro,caminho):
    list_dir = listdir(caminho)
    filtro = filtro.replace(" ","_")
    list_dir.sort()
    list_dir_nomes = []
    resultado = {}
    filtro_tratado = tratar_string_nome(filtro)

    for i in range(len(list_dir)):
        nome = ""
        if list_dir[i].endswith("_cliente.json"):
            nome = list_dir[i].replace("_cliente.json","").replace("_"," ").capitalize()
        elif list_dir[i].endswith("_produto.json"):
            nome = list_dir[i].replace("_produto.json","").replace("_"," ").capitalize()
        elif list_dir[i].endswith("_report.json"):
            nome = list_dir[i].replace("_report.json","").replace("_"," ").capitalize()

        list_dir_nomes.append(nome)
    for i in range(len(list_dir)):
        if list_dir_nomes[i].lower().__contains__(filtro_tratado):
            resultado[list_dir_nomes[i].replace("_"," ").capitalize()] = list_dir[i]
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

def gerar_relatorio_venda(cliente,lista_venda):
    mudar_diretorio(products_path)
    relatorio = {}
    produtos = {}
    total_venda = 0
    nome_arquivo = data_hora()+"_report"
    if cliente != "cliente_padrao":
            nome = ler_arquivo_json_para_python(cliente)["nome"]
    else:
        nome = cliente
    relatorio[nome] = {}
    for item in lista_venda:
        produto = ler_arquivo_json_para_python(item[0])["nome"]
        quantidade = item[1]
        valor_unitario = item[2]
        total = quantidade * valor_unitario
        total_venda += total
        relatorio[nome][produto] = {"quantidade":quantidade,"valor_unitario":valor_unitario,"total":total}
    relatorio[nome]["Total da venda"] = total_venda
    dados = json.dumps(relatorio,indent=4,ensure_ascii=False)
    mudar_diretorio(reports_path)
    string_para_arquivo(dados,nome_arquivo)
    mudar_diretorio(root_path)
    

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

def numero_string(string_input):
    try:
        if string_input.__contains__(".") and string_input.__contains__(","):
            try:
                valor = string_input.replace(".","").replace(",",".")
                decimal = float(valor)
                return decimal
            except:
                pass
        elif string_input.__contains__(","):
            try:
                valor = string_input.replace(",",".")
                decimal = float(valor)
                return decimal
            except:
                pass
        elif string_input.__contains__("."):
            try:
                decimal = float(string_input)
                return decimal
            except:
                pass
        else:
            try:
                return int(string_input)
            except:
                return string_input
    except:
        return string_input

def vender(dicionario_venda):
    dados_relatorio_venda = {}
    nome_arquivo = data_hora()
    for produto in dicionario_venda:
        item = produto
        quantidade = dicionario_venda[item]
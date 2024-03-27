import re
import functools
import operator
import pandas as pd
import numpy as np
from datetime import datetime

def achatar_lista(lista_aninhada):
    """
    Achata uma lista de listas em uma única lista.

    Parâmetros:
    lista_aninhada (list): Lista de listas a ser achatada.

    Retorna:
    list: Lista achatada.
    """
    return functools.reduce(operator.iconcat, lista_aninhada, [])

def remover_duplicatas(lista):
    """
    Remove elementos duplicados de uma lista usando um conjunto.

    Parâmetros:
    lista (list): Lista com elementos potencialmente duplicados.

    Retorna:
    list: Lista com duplicatas removidas.
    """
    return list(set(lista))
   
def filtrar_dados_por_intervalo_de_datas(data_frame, coluna_data, data_inicial, data_final):
    """
    Filtra um DataFrame com base em um intervalo de datas.

    Parâmetros:
    data_frame (pd.DataFrame): DataFrame a ser filtrado.
    coluna_data (str): Nome da coluna contendo as datas.
    data_inicial (str): Data inicial no formato 'YYYY-MM-DD'.
    data_final (str): Data final no formato 'YYYY-MM-DD'.

    Retorna:
    pd.DataFrame: DataFrame filtrado.
    """
    format = "%Y-%m-%d"
    datas_validas = bool(datetime.strptime(data_inicial, format)) and bool(datetime.strptime(data_final, format))
    if datas_validas:
        return data_frame[data_frame[coluna_data].between(data_inicial, data_final)]

def remover_caracteres(lista_strings, caracteres_para_remover):
    """
    Remove caracteres especificados de strings em uma lista.

    Parâmetros:
    lista_strings (list): Lista de strings.
    caracteres_para_remover (list): Lista de caracteres a serem removidos.

    Retorna:
    list: Lista de strings com caracteres especificados removidos.
    """
    # Converte a lista de caracteres para remover em uma string
    caracteres_para_remover_str = ''.join(caracteres_para_remover)
    
    # Cria uma expressão regular que corresponde a qualquer um dos caracteres para remover
    regex = '[' + re.escape(caracteres_para_remover_str) + ']'
    
    # Usa a função re.sub para substituir os caracteres especificados por uma string vazia
    lista_filtrada = [re.sub(regex, '', item) for item in lista_strings]
    
    return lista_filtrada

def remover_nao_numericos(lista_issues):
    """
    Remove caracteres não numéricos de strings em uma lista.

    Parâmetros:
    lista_issues (list): Lista de strings.

    Retorna:
    list: Lista de strings com caracteres não numéricos removidos.
    """
    lista_filtrada = []
    for item in lista_issues:
        novo_item = re.sub('[^0-9]_', '', item)
        lista_filtrada.append(novo_item)
    return lista_filtrada

def extrair_ids_issues(mensagens_commit):
    """
    Extrai IDs de issues de mensagens de commit.

    Parâmetros:
    mensagens_commit (list): Lista de mensagens de commit.

    Retorna:
    list: Lista de IDs de issues.
    """
    lista_commit_msg_aninhada = [(msg.split()) for msg in mensagens_commit]
    lista_commit_msg_aux = remover_duplicatas(achatar_lista(lista_commit_msg_aninhada))
    lista_commit_msg = [item.replace("'","") for item in lista_commit_msg_aux]
    lista_issues_numero = [issue for issue in lista_commit_msg if re.match('ISSUE_', issue)]
    lista_issues = [issue.replace('ISSUE_', '') for issue in lista_issues_numero]
    lista_issues_aux = remover_nao_numericos(lista_issues)
    return lista_issues_aux

def calcular_tempo_em_dias(detalhes_issue, chave):
    """
    Calcula o tempo gasto em uma issue em dias.

    Parâmetros:
    detalhes_issue (dict): Dicionário contendo detalhes da issue.
    chave (str): Chave para o tempo gasto.

    Retorna:
    float: Tempo gasto em dias.
    """
    segundos_por_hora = 3600.0
    horas_por_dia = 8
    return detalhes_issue[chave]/(horas_por_dia * segundos_por_hora)

def extrair_valor_por_label(labels_issue, label):
    """
    Extrai um valor associado a um label específico.

    Parâmetros:
    labels_issue (list or str): Lista de labels ou um único label.
    label (str): Label a ser buscado.

    Retorna:
    str: Valor associado ao label, se encontrado, caso contrário uma string vazia.
    """
    if type(labels_issue) is list:
        filtrado_por_label = [elemento for elemento in labels_issue if re.match(label, elemento)]
        valor = [issue.replace(label, '') for issue in filtrado_por_label]
    else:
        valor = ''
    if len(valor) > 0:
        valor = valor[0]
    return valor

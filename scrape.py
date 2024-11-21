from flask import jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage') 
# chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)


def login(u, s):
    print('Iniciando login')
    # Encontrar campos de login e senha pelo ID e preencher
    driver.find_element(By.ID, "vSIS_USUARIOID").send_keys(u)  # Substitua "login-field-id" pelo ID real
    driver.find_element(By.ID, "vSIS_USUARIOSENHA").send_keys(s)  # Substitua "password-field-id" pelo ID real

    # Enviar formulário de login
    driver.find_element(By.NAME, "BTCONFIRMA").click()  # Substitua "login-button-id" pelo ID real do botão de login
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "ygtvlabelel10Span"))
        )
        # Extrai o texto de cada elemento para uma lista
        # REMOVER APÓS OS TESTES vvvvvv
        print('Sucesso no login')
        # REMOVER APÓS OS TESTES ^^^^^^
        return True
    except:
        print("Falha no login, retornando Falso")
        return False
    
    
def scraping():
    # REMOVER APÓS OS TESTES vvvvvv
    print('Início do Scraping')
    # REMOVER APÓS OS TESTES ^^^^^^
    # Notas_parciais
    driver.implicitly_wait(2)

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.ID, "ygtvlabelel10Span"))
        )
        driver.find_element(By.ID, "ygtvlabelel10Span").click()
    except:
        print("Botão não encontrado")

    # Pegar Notas_parciais
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ReadonlyAttribute"))
        )
        nome = driver.find_element(By.ID, 'span_MPW0041vPRO_PESSOALNOME').text
        nome = nome[0:-2]
        notas_ele = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'span_vACD_ALUNOHISTORICOITEMMEDIAFINAL_00')]")
        notas = [nota.text for nota in notas_ele]
        mates_ele = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'span_vACD_DISCIPLINANOME_00')]")
        mates = []
        
        for i in range(len(mates_ele)):
            if mates_ele[i].text.startswith("Projeto Integrador"):
                notas.pop(i)
            else:
                mates.append(mates_ele[i].text)
        # REMOVER APÓS OS TESTES vvvvvv
        print("Notas parciais obtidas")
        # REMOVER APÓS OS TESTES ^^^^^^
    except:
        print("Os elementos com as notas parciais não foram encontrados.")

    driver.implicitly_wait(2)

    # Histórico completo
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.ID, "ygtvlabelel8Span"))
        )
        driver.find_element(By.ID, "ygtvlabelel8Span").click()
    except:
        print("Botão Histórico não encontrado")
    # Historico completo
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ReadonlyAttribute"))
        )
        notas_ele = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'span_vACD_ALUNOHISTORICOITEMMEDIAFINAL_00')]")
        mates_ele = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'span_vACD_DISCIPLINANOME_00')]")
        notas_h = []
        mates_h = []
        
        for i in range(len(mates_ele)):
            if mates_ele[i].text.startswith("Projeto Integrador"):
                a = 1
            else:
                mates_h.append(mates_ele[i].text)
                notas_h.append(notas_ele[i].text)
        # REMOVER APÓS OS TESTES vvvvvv
        print("Notas históricas obtidas")
        # REMOVER APÓS OS TESTES ^^^^^^
    except:
        print("Os elementos com as notas históricas não foram encontrados.")

# REMOVER APÓS OS TESTES vvvvvv
    # print(mates)
    # print(notas)
    # print('Histórico:')
    # print(mates_h)
    # print(notas_h)
# REMOVER APÓS OS TESTES ^^^^^^
    parcial = [{ "tipo": 'a', "nome": materia, "nota": nota, 'abc': 'D'} for materia, nota in zip(mates, notas)]
    historico = [{ "tipo": 'h', "nome": materia, "nota": nota, 'abc': 'D'} for materia, nota in zip(mates_h, notas_h)]

    mates_combinadas = parcial+historico
    print('\n\nResultado sendo construído')
    resultadoParcial = [
        {"id": index, **materia} for index, materia in enumerate(mates_combinadas)
    ]
    # Convertendo para JSON
    # resultado_json = json.dumps(resultadoParcial, ensure_ascii=False, indent=4)
    
    # return resultado_json
    print('Dando return')
    return jsonify({'nome': nome, 'materias': resultadoParcial})

def run_scraping(u, s):
    
    url = 'https://siga.cps.sp.gov.br/aluno/login.aspx'
   
    driver.get(url)
    print('run_scraping iniciado')

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, '/html/body/span/h1'))
        )
        print('Erro no siga.')
        print(driver.find_element(By.XPATH, '/html/body/span/h1').text)
        return 'Falha'
    except:
        print("Sem problemas com o Siga")
        if login(u, s):
            print('login ok')
            return scraping()
        else:
            return 'Falha no login'
    # if (a == "Server Error in '/aluno' Application."):
    #     print(a)
    # else:
    #     print('Sem erros no siga.')
    #     if login(u, s):
    #         return scraping()
    #     else:
    #         return 'Falha no login'
    
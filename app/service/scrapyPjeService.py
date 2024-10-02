import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


def read_excel():
    print("Verificando o diretório de trabalho atual")
    # Verifica o diretório de trabalho atual
    current_dir = os.getcwd()
    print(f"Diretório de trabalho atual: {current_dir}")

    # Verifica se o diretório 'data' existe e lista arquivos
    data_dir = './app/data'

    if os.path.exists(data_dir) and os.path.isdir(data_dir):
        print(f"Arquivos em '{data_dir}': {os.listdir(data_dir)}")
    else:
        print(f"Diretório '{data_dir}' não existe.")

    # Caminho para o arquivo Excel
    file_path = os.path.join(data_dir, 'Processos_TRF1.xlsx')

    if not os.path.exists(file_path):
        print(f"Arquivo '{file_path}' não existe.")
        return

    # Leitura do arquivo Excel
    df = pd.read_excel(file_path)
    print("Arquivo Excel lido com sucesso")

    # Selecionar a primeira coluna
    first_column = df.iloc[:, 0]

    # Iterar sobre cada valor da primeira coluna e imprimir
    for value in first_column:
        print(f"Buscando o número do processo: {value}")
        search_process_number(value)


def initiate_webdriver() -> WebDriver:
    # Obtém o caminho de download do arquivo .env
    path_download = os.getenv('path_download', os.getcwd())
    if not os.path.exists(path_download):
        print(f"O caminho de download especificado '{path_download}' não existe.")
        return None

    print(f"Iniciando o WebDriver com o diretório de download: {path_download}")

    # Configurações do WebDriver
    chrome_options = Options()
    chrome_prefs = {
        'download.default_directory': path_download,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    }
    chrome_options.add_experimental_option('prefs', chrome_prefs)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')  # Execute Chrome em modo headless, se necessário
    chrome_options.add_argument('--disable-gpu')  # Desativa a GPU, pode ser necessário no Docker
    chrome_options.add_argument('--remote-debugging-port=9222')  # Permite o Chrome DevTools
    # Inicializa o WebDriver
    driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=chrome_options)
    print("WebDriver iniciado com sucesso")
    return driver


def search_process_number(process_number):
    driver = initiate_webdriver()
    if driver is None:
        print("WebDriver não iniciado devido à configuração incorreta do caminho de download.")
        return

    try:
        print(f"Acessando a URL para o número do processo: {process_number}")
        # Acessa a URL
        driver.get("https://pje1g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam")

        # Aguarda um tempo para garantir que a página foi carregada
        time.sleep(5)  # Ajuste o tempo conforme a necessidade

        # Encontra o campo de entrada para o número do processo
        input_element = driver.find_element(By.ID,
                                            "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso")

        # Passa o número do processo para o campo de entrada
        print(f"Enviando número do processo: {process_number}")
        input_element.send_keys(process_number)

        # Encontra o botão de pesquisa e clica
        search_button = driver.find_element(By.ID, "fPP:searchProcessos")
        search_button.click()

        # Aguarda os resultados
        time.sleep(5)  # Ajuste o tempo conforme a necessidade

        try:
            # Tenta encontrar e clicar no link específico
            print("Procurando e clicando no link 'Consulta pública'")
            link_consulta_publica = driver.find_element(By.XPATH, "//a[contains(@onclick, 'Consulta pública')]")
            driver.execute_script("arguments[0].click();", link_consulta_publica)
        except Exception as e:
            # Caso ocorra uma exceção, loga a mensagem, espera 10 segundos e finaliza
            print("Link 'Consulta pública' não encontrado. Finalizando o script.")
            time.sleep(10)
            driver.quit()
            exit(1)  # Sai do script com código de erro

        # Aguarda a nova aba carregar
        time.sleep(5)  # Ajuste o tempo conforme a necessidade

        # Alterna para a nova aba
        driver.switch_to.window(driver.window_handles[-1])
        print("Alternando para a nova aba do processo encontrado")

        # Procurar o painel de documentos pelo ID
        try:
            panel = driver.find_element(By.ID, "j_id136:processoDocumentoGridTabPanel")
            print("Painel de documentos encontrado.")

            # Procurar todos os links dentro do painel que têm um `onclick` e título "Visualizar"
            links = panel.find_elements(By.XPATH, ".//a[contains(@onclick, 'A4J.AJAX.Submit') and @title='Visualizar']")
            if links:
                print(f"Encontrados {len(links)} links. Clicando nos links...")
                for link in links:
                    link_html = link.get_attribute('outerHTML')
                    print(f"Link encontrado: {link_html}")
                    driver.execute_script("arguments[0].click();", link)

                    # Alterna para a nova aba
                    driver.switch_to.window(driver.window_handles[-1])

                    # Espera 10 segundos para a nova aba ser carregada
                    time.sleep(10)

                    try:
                        # Procurar e clicar no link de download do PDF pelo ID em cada aba
                        download_link = driver.find_element(By.ID, "j_id42:downloadPDF")
                        print(f"Link de download encontrado. Clicando no link...")
                        driver.execute_script("arguments[0].click();", download_link)
                    except Exception as e:
                        print(f"Erro ao encontrar ou clicar no link de download do PDF: {e}")

                    # Espera o download ser iniciado
                    time.sleep(5)  # Ajuste conforme necessário

                    # Fecha a aba atual
                    driver.close()

                    # Alterna de volta para a aba original
                    driver.switch_to.window(driver.window_handles[0])
            else:
                print("Nenhum link encontrado no painel de documentos.")
        except Exception as panel_ex:
            print(f"Erro ao procurar o painel de documentos ou clicar nos links: {panel_ex}")

        # Extrai o HTML da página atual após clicar em "Consulta pública"
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print("Dados da página de consulta pública extraídos com sucesso")

        return soup.prettify()  # Retorne uma string do HTML formatado (ou processe conforme necessário)
    except Exception as e:
        print(f"Erro durante o download do número do processo: {e}")
    finally:
        driver.quit()
        print("WebDriver finalizado")


# Utilização da função para leitura do Excel e processamento dos números de processo
read_excel()

# Projeto de Consulta de Processos TRF1

Este projeto é uma aplicação Python que lê números de processos de um arquivo Excel e usa Selenium para automatizar a consulta de processos no site do TRF1, baixando PDFs relevantes.

## Estrutura do Projeto

```
├── app
│   ├── data
│   │   └── xlsx
│   ├── __init__.py
│   ├── main.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.cpython-311.pyc
│   │   ├── main.cpython-310.pyc
│   │   └── main.cpython-311.pyc
│   ├── routers
│   │   ├── __init__.py
│   │   ├── pjeRouter.py
│   │   └── __pycache__
│   │       ├── __init__.cpython-310.pyc
│   │       ├── __init__.cpython-311.pyc
│   │       ├── pje.cpython-311.pyc
│   │       ├── pjeRouter.cpython-310.pyc
│   │       └── pjeRouter.cpython-311.pyc
│   └── service
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-310.pyc
│       │   ├── __init__.cpython-311.pyc
│       │   ├── scrapyPjeService.cpython-310.pyc
│       │   └── scrapyPjeService.cpython-311.pyc
│       └── scrapyPjeService.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt

```

## Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Configurando a Aplicação

1. **Clone o repositório:**

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

2. **Crie um arquivo `.env` para configurar o caminho de download:**

Crie um arquivo `.env` na raiz do projeto com o conteúdo:

## Executando com Docker

1. **Build a imagem Docker:**

```bash
docker-compose build
```

2. **Execute a aplicação:**

```bash
docker-compose up
```

A aplicação estará disponível em `http://localhost:8001`.

## Dockerfile

O `Dockerfile` está configurado para:

1. Usar uma imagem base do Ubuntu 22.04.
2. Instalar as dependências necessárias, incluindo Python 3 e Google Chrome.
3. Instalar o ChromeDriver para controle do Chrome via Selenium.
4. Copiar o código do projeto para o contêiner.
5. Definir o `PYTHONPATH` para `/app`.
6. Rodar o `uvicorn` para servir a aplicação.

## docker-compose.yml

O `docker-compose.yml` está configurado para:

1. Construir a imagem Docker a partir do Dockerfile na raiz do projeto.
2. Mapear a porta `8000` do contêiner para a porta `8001` do host.
3. Montar o diretório atual no diretório `/app` do contêiner.
4. Definir a variável de ambiente `PYTHONUNBUFFERED` para `1`.

## Explicação do Código

O código principal está no arquivo `app/main.py`. Aqui está um resumo de suas funções:

- **read_excel:** Lê o arquivo Excel com números de processos e invoca a função `search_process_number` para cada número de processo.
- **initiate_webdriver:** Configura e inicializa o WebDriver do Chrome com opções específicas.
- **search_process_number:** Acessa o site do TRF1, realiza a busca pelo número do processo fornecido, navega pelos resultados, e tenta baixar os PDFs disponíveis.

## Observações

- Certifique-se de que o caminho de download especificado no arquivo `.env` exista no seu sistema.
- O tempo de espera (com `time.sleep`) pode precisar ser ajustado com base na velocidade da conexão e desempenho do site.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
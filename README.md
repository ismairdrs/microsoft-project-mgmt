# Microsoft Project Management System

## Descrição
Este é um sistema desenvolvido para a Microsoft, que visa gerenciar projetos, clientes e atividades de maneira eficiente. Ele permite a criação, listagem e gerenciamento de clientes, projetos e atividades associados.

O projeto utiliza **FastAPI** como framework principal, **PostgreSQL** como banco de dados, e foi implementado com foco em modularidade e extensibilidade. Inclui testes unitários e de integração para garantir a confiabilidade das funcionalidades.

---

## Requisitos Necessários
- **Python 3.11**
- **Docker**
- **Docker Compose**

---

## Como Rodar o Projeto

### Configuração Inicial
1. Clone o repositório:
   - `git clone git@github.com:ismairdrs/microsoft-project-mgmt.git`
   - `cd microsoft-project-mgmt`

2. Crie o ambiente virtual e instale as dependências:
   - `python3.11 -m venv venv`
   - `source venv/bin/activate`
   - `pip install -r requirements.txt`

3. Configure o banco de dados:
   Certifique-se de que o **Docker** está instalado e funcionando.

---

### Rodando o Projeto
Para iniciar o projeto localmente, use o comando:

- `make run`

Este comando inicia a aplicação FastAPI e o banco de dados PostgreSQL em contêineres Docker. Após a inicialização, você pode acessar a API em:

- URL da API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Documentação Interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Executando os Testes

#### Testes Unitários
Para rodar os testes unitários, utilize o comando:

- `make unit-test`

#### Testes de Integração
Para rodar os testes de integração, utilize o comando:

- `make integration-test`

Este comando configura um banco de dados de teste em um contêiner Docker e executa os testes de integração.

---

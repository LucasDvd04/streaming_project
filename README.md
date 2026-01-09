# 🎬 Streaming App – Django + APIs

Este projeto é uma aplicação web desenvolvida com **Django** que simula uma plataforma de streaming. Os dados exibidos são obtidos a partir de **duas APIs diferentes**, integrados e organizados em um único sistema para exibição de mídias como filmes e séries.

🔗 **Demo online:**
[https://lucasdvd04.pythonanywhere.com/](https://lucasdvd04.pythonanywhere.com/)

---

## 📌 Objetivo do Projeto

O objetivo deste projeto é demonstrar, de forma prática, a integração de múltiplas APIs em uma aplicação Django, abordando conceitos como:

* Consumo de APIs externas
* Normalização e persistência de dados
* Organização de conteúdo para exibição contínua (estilo streaming)
* Boas práticas de estruturação de projeto Django
* Deploy em ambiente de produção (PythonAnywhere)

Este projeto também faz parte do meu **portfólio como desenvolvedor Python/Django**.

---

## 🚀 Funcionalidades

* Listagem de filmes e/ou séries
* Integração com **duas APIs externas**:

  * API responsável pelos dados principais das mídias (título, imagem, ano, etc.)
  * API complementar para descrição, detalhes ou informações adicionais
* Exibição organizada do conteúdo no frontend
* Persistência dos dados em banco de dados local
* Interface simples e funcional
* Aplicação publicada em ambiente online

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Django**
* **Requests** (consumo de APIs)
* **SQLite** (ambiente de desenvolvimento)
* **HTML / CSS**
* **PythonAnywhere** (deploy)

---

## 🧩 Arquitetura e Integração das APIs

O projeto utiliza duas APIs distintas:

1. **API de Mídias**
   Responsável por fornecer a lista principal de filmes/séries, incluindo identificadores únicos.

2. **API de Detalhes**
   Utilizada para enriquecer os dados, como descrição, sinopse ou informações complementares.

Os dados são processados, tratados e armazenados no banco de dados para evitar múltiplas requisições desnecessárias e melhorar a performance da aplicação.

---

## ▶️ Como Executar o Projeto Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. Inicie o servidor

```bash
python manage.py runserver
```

A aplicação estará disponível em:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

para preencher o banco de dados é necessario abrir requisições na api dentro do projeto.

---

## 🌐 Deploy

O projeto está publicado no **PythonAnywhere**, incluindo:

* Configuração de ambiente virtual
* Migrações aplicadas em produção
* Banco de dados configurado
* Variáveis sensíveis protegidas

🔗 **Link do projeto em produção:**
[https://lucasdvd04.pythonanywhere.com/](https://lucasdvd04.pythonanywhere.com/)

---

## 📌 Possíveis Melhorias Futuras

* Sistema de autenticação de usuários
* Favoritar filmes/séries
* Categorias como *Lançamentos* e *Em Alta*
* Cache para otimização das requisições às APIs
* Interface mais avançada (UI/UX)

📢 *Este projeto é educacional e não possui fins comerciais.*

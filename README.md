# ⛩️ MyAnimeHub - Sistema de Gestão de Animes

![Status](https://img.shields.io/badge/Status-Online-success?style=flat&logo=python)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-green?style=flat&logo=flask)
![Deploy](https://img.shields.io/badge/Deploy-PythonAnywhere-blueviolet?style=flat)

> **Acesse o projeto online:** [https://luffybaiano27.pythonanywhere.com](https://luffybaiano27.pythonanywhere.com)

---

## 📖 Sobre o Projeto

O **MyAnimeHub** é uma aplicação web *Full Stack* desenvolvida como projeto acadêmico para o curso de **Análise e Desenvolvimento de Sistemas (ADS)**.

O objetivo foi criar uma solução para substituir o uso de planilhas e blocos de notas no gerenciamento de animes assistidos. O diferencial do sistema é a **automação**: ao invés de um CRUD manual tradicional, o sistema consome APIs externas para buscar capas, sinopses e dados técnicos, traduzindo o conteúdo automaticamente para o usuário.

---

## 🛠️ Tecnologias e Ferramentas

### Backend
* **Python 3.10:** Linguagem base.
* **Flask:** Microframework web para rotas e controle de requisições.
* **SQLAlchemy (ORM):** Para manipulação do banco de dados orientado a objetos.
* **Flask-Login:** Gestão de sessões e proteção de rotas.
* **Requests:** Para consumo de APIs REST.
* **Deep-Translator:** Biblioteca para tradução automática (Inglês -> Português).

### Frontend
* **HTML5 / CSS3:** Estrutura e Estilização.
* **Bootstrap 5:** Design responsivo, Grid System e componentes (Modais/Carrossel).
* **Jinja2:** Motor de templates para renderização dinâmica no servidor.
* **Particles.js:** Efeitos visuais.

### Banco de Dados
* **SQLite:** Banco de dados relacional serverless (arquivo `animes.db`).

---

## ⚙️ Arquitetura e Fluxo de Dados

O sistema opera com um fluxo de **"Busca e Enriquecimento"**:

1.  **Input:** O usuário digita o nome do anime (ex: "One Piece").
2.  **API Fetch:** O Backend consulta a **Jikan API** (MyAnimeList).
3.  **Tratamento de Dados:**
    * Verifica se o anime está em lançamento (se episódios retornarem `null` ou `1`, converte para `0`).
    * Traduz a sinopse original (EN) para Português (PT-BR).
4.  **Persistência:** Os dados tratados são salvos no banco SQLite via SQLAlchemy.
5.  **Visualização:** O Frontend renderiza os cards com links dinâmicos para streaming.

---

## 🚀 Como rodar o projeto localmente

Para testar em sua máquina, siga os passos abaixo:

### 1. Clone o repositório
```bash
git clone [https://github.com/LuffyBaiano27/MyAnimeHub.git](https://github.com/LuffyBaiano27/MyAnimeHub.git)
cd MyAnimeHub

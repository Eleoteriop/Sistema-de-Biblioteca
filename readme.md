# 📚 Sistema de Biblioteca
Um sistema completo de gerenciamento de biblioteca desenvolvido com Python e Flask, permitindo o cadastro e gerenciamento de usuários e livros, autenticação de usuários, empréstimo de livros e registro de doações.

O projeto também utiliza a **Open Library API** para buscar automaticamente imagens das capas dos livros, proporcionando uma experiência mais visual para os usuários.

🚀 Demonstração
🔗 [Acessar o projeto online](https://sistema-de-biblioteca-xbdr.onrender.com/)

## ✨ Funcionalidades
🔐 Cadastro de usuários<br>
🔑 Login e autenticação<br>
👤 Sessão de usuário<br>
📚 Cadastro e gerenciamento de livros<br>
🔎 Consulta de livros<br>
📖 Sistema de empréstimos<br>
🔄 Controle de livros emprestados<br>
🎁 Sistema de doação de livros<br>
🖼️ Busca automática das capas dos livros através da Open Library API<br>
💾 Banco de dados SQLite3<br>
🌐 Interface web utilizando Flask<br>
🚪 Logout e controle de sessão<br><br>

## 🛠️ Tecnologias utilizadas
* Python<br>
* Flask<br>
* SQLite3<br>
* HTML5<br>
* CSS3<br>
* Jinja2<br>
* Open Library API

## 🏗️ Estrutura do projeto
biblioteca/<br>
│<br>
├── __pycache__/<br>
│<br>
├── .vscode/<br>
│<br>
├── banco de dados <br>
│&emsp;&emsp;&emsp;&emsp;└──biblioteca.db<br>
│<br>
├── static/<br>
│ &emsp;&emsp;&emsp;  ├── css/<br>
│ &emsp;&emsp;&emsp;  └── imagens/<br>
│<br>
├── templates/<br>
│ &emsp;&emsp;&emsp;&emsp;  ├── cadastrar_livro.html<br>
│ &emsp;&emsp;&emsp;&emsp; ├── cadastro.html<br>
│ &emsp;&emsp;&emsp;&emsp; ├── esqueci_senha.html<br>
│ &emsp;&emsp;&emsp;&emsp; ├── home.html<br>
│ &emsp;&emsp;&emsp;&emsp; ├── livros.html<br>
│ &emsp;&emsp;&emsp;&emsp; ├── login.html<br>
│ &emsp;&emsp;&emsp;&emsp;  ├── meus_emprestimos.html<br>
│ &emsp;&emsp;&emsp;&emsp; └── Nova_senha.html<br>
│<br>
├── venv/<br>
│<br>
├── .gitignore<br>
├── app.py<br>
└── livros.py<br>

A estrutura acima é apenas um exemplo e pode ser adaptada de acordo com a organização atual do projeto.

### ⚙️ Como executar o projeto
1. Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git<br>
&emsp; Entre na pasta do projeto: cd seu-repositorio

2. Crie um ambiente virtual<br>
&emsp; **Windows:** python -m venv venv venv\Scripts\activate<br>
&emsp;  **Linux/macOS:** python3 -m venv venv source venv/bin/activate

3. Instale as dependências
pip install -r requirements.txt

4. Execute a aplicação
python app.py

Depois, acesse no navegador:

http://127.0.0.1:5000

### 🗄️ Banco de dados
O projeto utiliza SQLite3 para armazenar as informações da aplicação.

Entre os dados armazenados estão:<br>
* Usuários cadastrados<br>
* Livros<br>
* Informações relacionadas aos empréstimos<br>
* Registros necessários para o funcionamento do sistema<br>
* Por utilizar SQLite, não é necessário configurar um servidor de banco de dados separado para executar o projeto localmente.

### 📖 **Open Library API**
Para melhorar a apresentação dos livros, o sistema utiliza a Open Library API para obter informações e imagens das capas dos livros.

A integração permite que as capas dos livros sejam obtidas através de uma API externa, evitando a necessidade de armazenar manualmente todas as imagens das capas no projeto.

Essa funcionalidade demonstra a utilização de uma API externa em uma aplicação Flask.

### 🔐 Autenticação e sessões
O sistema possui um fluxo de autenticação para os usuários.

Cadastro<br>
   ↓<br>
Login<br>
   ↓<br>
Sessão do usuário<br>
   ↓<br>
Acesso às funcionalidades<br>
   ↓<br>
Logout

As sessões são utilizadas para controlar o acesso às funcionalidades que dependem de um usuário autenticado.

### 📚 Sistema de empréstimos
O sistema permite que os usuários realizem o empréstimo de livros disponíveis no acervo da biblioteca.

Fluxo básico:

Usuário<br>
   ↓<br>
Seleciona um livro<br>
   ↓<br>
Solicita o empréstimo<br>
   ↓<br>
Sistema registra o empréstimo<br>
   ↓<br>
Livro fica associado ao empréstimo

### 🎁 Sistema de doações
O projeto também conta com uma funcionalidade de doação de livros, permitindo que usuários contribuam para o crescimento do acervo da biblioteca.

O sistema permite realizar o cadastro das informações necessárias para registrar uma nova doação.

### 👤 Cadastro e login
Os usuários podem criar suas próprias contas através do sistema de cadastro.

Após o cadastro, o usuário pode realizar o login e acessar as funcionalidades disponíveis de acordo com seu estado de autenticação.

Novo usuário<br>
     ↓<br>
Cadastro<br>
     ↓<br>
Conta criada<br>
     ↓<br>
Login<br>
     ↓<br>
Usuário autenticado

### 🚀 Possíveis melhorias futuras
Algumas funcionalidades que podem ser implementadas futuramente:

 Painel administrativo<br>
 Controle de usuários administradores<br>
 Paginação dos livros<br>
 Sistema de busca e filtros avançados<br>
 Data de devolução dos empréstimos<br>
 Notificações de empréstimos próximos do vencimento<br>
 Histórico completo de empréstimos<br>
 Validação mais completa dos formulários<br>
 Deploy da aplicação<br>
 Migração para PostgreSQL<br>
 Testes automatizados<br>
 Melhorias de responsividade<br>

## 🎯 Objetivo do projeto
Este projeto foi desenvolvido com o objetivo de praticar e demonstrar conhecimentos em desenvolvimento web com Python e Flask.

Durante o desenvolvimento foram trabalhados conceitos como:

* Desenvolvimento de aplicações web<br>
* Criação de rotas com Flask<br>
* Templates com Jinja2<br>
* Autenticação de usuários<br>
* Gerenciamento de sessões<br>
* Operações CRUD<br>
* Banco de dados SQLite3<br>
* Integração com APIs externas<br>
* Consumo de dados através de requisições HTTP<br>
* Gerenciamento de livros<br>
* Sistema de empréstimos<br>
* Sistema de doações<br>

## 👨‍💻 Desenvolvedor
Desenvolvido por Patrick Eleoterio.

⭐ **Se você gostou do projeto, considere deixar uma estrela no repositório!**

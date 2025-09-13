# 📚 Sistema de Biblioteca Comunitária

Sistema web completo para gerenciamento de biblioteca comunitária desenvolvido com **Django 4.2** e **Bootstrap 5** (Sneat Admin Template).

## Link do vídeo da apresentação👇
[Vídeo no youtube]
(https://youtu.be/u38GoTJIRhI?si=GSyE3G_x2HuQfz2_)

## 🎯 Objetivo do Projeto

Sistema profissional de gerenciamento de biblioteca com funcionalidades completas:

### 📋 **Funcionalidades Principais**
- **Gestão Completa**: Livros, categorias, leitores e funcionários
- **Sistema de Empréstimos**: Controle completo de empréstimos/devoluções
- **Controle de Multas**: Cálculo automático por atraso (R$ 2,00/dia)
- **Validações Robustas**: Django Forms com validações customizadas
- **Permissões**: Sistema baseado em grupos (Funcionários/Leitores)
- **Interface Responsiva**: Design moderno e adaptável
- **Dashboard Inteligente**: Estatísticas em tempo real

### 🔧 **Características Técnicas**
- ✅ **Django Forms**: Validações automáticas e tratamento de erros
- ✅ **Sistema de Permissões**: Controle de acesso por grupos
- ✅ **ModelForms**: Integração total com modelos Django  
- ✅ **Validações Customizadas**: ISBN, CPF, limites de empréstimo
- ✅ **Bootstrap 5**: Interface moderna e responsiva
- ✅ **SQLite**: Banco de dados integrado (pronto para produção)

## Integrantes do Grupo

- **Maria de Fátima Prado Neves** 
- **Raifran Santos Guimarães** 
- **Eduarda Teixeira Santos Fraga**

## 🚀 Funcionalidades Detalhadas

### **Para Funcionários (Acesso Total)**
- **Livros**: Criar, editar, excluir e consultar
- **Categorias**: Gerenciamento completo de categorias
- **Leitores**: Cadastro e gestão de usuários leitores
- **Funcionários**: Gestão da equipe da biblioteca
- **Empréstimos**: Realizar, renovar e devolver livros
- **Relatórios**: Dashboard com estatísticas completas
- **Multas**: Controle automático de atrasos

### **Para Leitores (Acesso Limitado)**
- **Consulta de Acervo**: Visualização de livros disponíveis
- **Categorias**: Navegação por categorias
- **Meus Empréstimos**: Acompanhamento de empréstimos ativos
- **Filtros e Busca**: Pesquisa avançada no acervo

## Pré-requisitos

- **Python 3.8+**: Linguagem de programação
- **pip**: Gerenciador de pacotes Python
- **Git**: Para clonar o repositório

## Instalação Completa

### 1️⃣ **Clone o Repositório**
```bash
git clone https://github.com/mariaprado000/biblioteca-comunitaria.git
cd biblioteca-comunitaria
```

### 2️⃣ **Configure o Ambiente Virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate
```

### 3️⃣ **Instale as Dependências**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Configure o Banco de Dados**
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações  
python manage.py migrate
```

### 5️⃣ **🎯 CONFIGURAÇÃO AUTOMÁTICA COMPLETA**
```bash
# ⭐ EXECUTE ESTE COMANDO PARA CONFIGURAR TUDO:
python create_test_data.py
```

**Este script configura automaticamente:**
- ✅ **Grupos e Permissões** (Funcionários/Leitores)
- ✅ **Usuário Administrador** (admin/admin123)  
- ✅ **Funcionário de Teste** (funcionario1/func123)
- ✅ **4 Leitores de Exemplo** (senha: 123456)
- ✅ **7 Categorias de Livros**
- ✅ **10 Livros Exemplo** (com ISBNs válidos)
- ✅ **Empréstimos Ativos** (para demonstração)

### 7️⃣ **Execute o Servidor**
```bash
python manage.py runserver
```

### 8️⃣ **Acesse o Sistema**
- 🌐 **Sistema**: http://127.0.0.1:8000/
- ⚙️ **Admin Django**: http://127.0.0.1:8000/admin/
- 🔐 **Login**: http://127.0.0.1:8000/auth/login/

---

## Usuários Pré-Configurados

### 👑 **ADMINISTRADOR PRINCIPAL**
- **Username**: `admin`
- **Password**: `admin123`  
- **Acesso**: Total (Superusuário + Funcionário)

### **FUNCIONÁRIO**
- **Username**: `funcionario1`
- **Password**: `func123`
- **Acesso**: Total (CRUD completo)

### **LEITORES DE TESTE**
| Username | Password | Nome Completo |
|----------|----------|---------------|
| `joao.silva` | `123456` | João Silva |
| `maria.prado` | `123456` | Maria Prado |
| `pedro.oliveira` | `123456` | Pedro Oliveira |
| `ana.costa` | `123456` | Ana Costa |

**Acesso dos Leitores**: Visualização de livros, categorias e próprios empréstimos

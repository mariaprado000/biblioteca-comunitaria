# 📚 Sistema de Biblioteca Comunitária

Sistema web para gerenciamento de biblioteca comunitária desenvolvido com Django 4.2 e Bootstrap 5 (Sneat Admin Template).

## 🎯 Objetivo do Projeto

Sistema completo de gerenciamento de biblioteca com:
- Controle de livros por categorias
- Gestão de leitores e funcionários  
- Sistema de empréstimos e devoluções
- Controle de multas por atraso
- Sistema de permissões baseado em grupos
- Interface responsiva e moderna

## Integrantes do Grupo

- **Maria de Fátima Prado Neves** 
- **Raifran Santos Guimarães** 
- **Eduarda Teixeira Santos Fraga**

### Para Funcionários:
- ✅ Gerenciar livros (CRUD completo)
- ✅ Gerenciar leitores e funcionários
- ✅ Realizar empréstimos e devoluções
- ✅ Controle de multas
- ✅ Renovar empréstimos
- ✅ Dashboard com estatísticas

### Para Leitores:
- ✅ Consultar acervo de livros
- ✅ Ver categorias disponíveis
- ✅ Visualizar empréstimos ativos

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação e Execução

1. **Clone o repositório:**
```bash
git clone https://github.com/mariaprado000/biblioteca-comunitaria.git
cd biblioteca-comunitaria
```

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Colete arquivos estáticos:**
```bash
python manage.py collectstatic --noinput
```

6. **Crie dados de teste (opcional):**
```bash
python create_test_data.py
```

7. **Execute o servidor:**
```bash
python manage.py runserver
```

8. **Acesse o sistema:**
   - URL: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 👤 Usuários de Teste

### Funcionário:
- **Usuário**: admin
- **Senha**: admin123
- **Permissões**: Acesso completo ao sistema

### Leitor:
- **Usuário**: maria.prado  
- **Senha**: 123456
- **Permissões**: Consulta de livros e categorias

## 🗂️ Estrutura do Projeto

```
biblioteca-comunitaria/
├── app_categoria/          # Gestão de categorias
├── app_dashboard/          # Dashboard principal
├── app_emprestimo/         # Sistema de empréstimos
├── app_funcionario/        # Gestão de funcionários
├── app_leitor/             # Gestão de leitores
├── app_livro/              # Gestão de livros
├── app_user/               # Autenticação
├── biblioteca/             # Configurações do projeto
├── base_static/            # Arquivos estáticos personalizados
├── staticfiles/            # Arquivos estáticos coletados
├── templates/              # Templates base
└── manage.py
```

# 🎵 Biblioteca de Música - API REST

Uma API REST moderna para gerenciar uma biblioteca de música, construída com FastAPI e SQLAlchemy. O projeto usa organização por módulos (`app/`) com models, schemas, rotas e configuração de banco separadas.

## ✨ Características Principais

- **CRUD Completo**: Operações Create, Read, Update e Delete para Artistas, Gêneros e Álbuns
- **Relacionamentos Complexos**: Suporte a relacionamentos One-to-Many e Many-to-Many
- **Validação de Dados**: Validação automática com Pydantic 2.x em todas as requisições
- **Tratamento de Erros**: Respostas HTTP apropriadas com mensagens de erro descritivas
- **Documentação Interativa**: Swagger UI integrado para testar endpoints
- **Type Hints Avançados**: Código totalmente tipado com `Mapped` e type hints completos (SQLAlchemy 2.0)
- **SQLAlchemy 2.0 Moderno**: Uso de `mapped_column` e `Mapped` para melhor type safety
- **Gestão de Banco Robusta**: Validação de variáveis de ambiente com tratamento de erros

## 🛠️ Stack Tecnológico

Dependências principais (veja `requirements.txt`):

- **FastAPI** 0.139.2 — Framework web
- **SQLAlchemy** 2.0.51 — ORM
- **Pydantic** 2.13.4 — Validação e serialização
- **Uvicorn** 0.51.0 — Servidor ASGI
- **psycopg2-binary** — Adaptador PostgreSQL

Consulte `requirements.txt` para a lista completa de dependências e versões.

## 📋 Pré-requisitos

- Python 3.9+
- PostgreSQL 12+
- pip ou poetry

## 🚀 Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/FilipeMadeira13/biblioteca-de-musica.git
cd biblioteca_de_musica
```

### 2. Criar e ativar ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/biblioteca_musica
```

### 5. Executar a aplicação
```bash
# estando na raiz do projeto
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação da API

Acesse a documentação interativa em:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Arquitetura e Estrutura

O código está organizado dentro do diretório `app/`:

```
biblioteca_de_musica/
├── app/
│   ├── main.py                # Aplicação FastAPI e ponto de entrada
│   ├── database.py            # Configuração do SQLAlchemy / sessão
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── album.py
│   │   ├── artista.py
│   │   └── album_genero.py
│   ├── routes/                # Roteadores (endpoints) por recurso
│   │   ├── album.py
│   │   ├── artista.py
│   │   └── genero.py
│   └── schemas/               # Esquemas Pydantic por recurso
│       ├── album.py
│       ├── artista.py
│       └── genero.py
├── requirements.txt
└── README.md
```

### Modelos de Dados

Todos os modelos utilizam SQLAlchemy 2.0 com `Mapped` type hints para máxima type safety:

#### Artista
```python
class Artista(Base):
    id: Mapped[int]           # Identificador único
    nome: Mapped[str]         # Nome do artista
    pais_origem: Mapped[str]  # País de origem
    ano_formacao: Mapped[int] # Ano de formação
    albuns: Mapped[list["Album"]]  # Relacionamento um-para-muitos
```

#### Gênero
```python
class Genero(Base):
    id: Mapped[int]           # Identificador único
    nome: Mapped[str]         # Nome do gênero musical
    albuns: Mapped[list["Album"]]  # Relacionamento muitos-para-muitos
```

#### Álbum
```python
class Album(Base):
    id: Mapped[int]            # Identificador único
    titulo: Mapped[str]        # Título do álbum
    artista_id: Mapped[int]    # Chave estrangeira para artista
    artista: Mapped["Artista"] # Relacionamento muitos-para-um
    generos: Mapped[list["Genero"]]  # Relacionamento muitos-para-muitos
```

> A relação entre Álbum e Gênero é muitos-para-muitos, implementada através de uma tabela associativa (`album_genero`) que guarda os pares `album_id` / `genero_id`.

### Configuração do Banco de Dados

A configuração do SQLAlchemy está em `app/database.py`:

```python
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi definida. Verifique seu arquivo .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Recursos:**
- Validação obrigatória de `DATABASE_URL` via `.env`
- Session management com context manager para garantir limpeza de recursos
- Suporte para qualquer banco de dados SQLAlchemy (PostgreSQL, MySQL, SQLite, etc.)

## 🔌 Endpoints Disponíveis

### Artistas
```
POST   /artistas/              # Criar novo artista
GET    /artistas/              # Listar todos os artistas
GET    /artistas/{artista_id}  # Obter artista específico
PUT    /artistas/{artista_id}  # Atualizar artista
DELETE /artistas/{artista_id}  # Deletar artista
```

### Gêneros
```
POST   /generos/              # Criar novo gênero
GET    /generos/              # Listar todos os gêneros
GET    /generos/{genero_id}   # Obter gênero específico
PUT    /generos/{genero_id}   # Atualizar gênero
DELETE /generos/{genero_id}   # Deletar gênero
```

### Álbuns
```
POST   /albuns/               # Criar novo álbum
GET    /albuns/               # Listar todos os álbuns
GET    /albuns/{album_id}     # Obter álbum específico
PUT    /albuns/{album_id}     # Atualizar álbum
DELETE /albuns/{album_id}     # Deletar álbum
```

## 📝 Exemplos de Uso

### Criar um Artista
```bash
curl -X POST "http://localhost:8000/artistas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "The Beatles",
    "pais_origem": "Reino Unido",
    "ano_formacao": 1960
  }'
```

### Listar Artistas
```bash
curl -X GET "http://localhost:8000/artistas/"
```

### Obter Artista Específico
```bash
curl -X GET "http://localhost:8000/artistas/1"
```

### Atualizar Artista
```bash
curl -X PUT "http://localhost:8000/artistas/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "The Beatles Remastered",
    "pais_origem": "Reino Unido",
    "ano_formacao": 1960
  }'
```

### Deletar Artista
```bash
curl -X DELETE "http://localhost:8000/artistas/1"
```

### Criar um Gênero
```bash
curl -X POST "http://localhost:8000/generos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Rock"
  }'
```

### Criar um Álbum
O álbum precisa referenciar um artista existente (`artista_id`) e, opcionalmente, uma lista de gêneros já cadastrados (`genero_ids`):
```bash
curl -X POST "http://localhost:8000/albuns/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Abbey Road",
    "artista_id": 1,
    "genero_ids": [1, 2]
  }'
```
Se `artista_id` ou algum id em `genero_ids` não existir no banco, a API retorna `404` com uma mensagem indicando o que não foi encontrado.

## 🎯 Boas Práticas Implementadas

✅ **Clean Code**: Código bem estruturado e legível  
✅ **Type Hints Avançados**: Uso completo de `Mapped` e type hints do SQLAlchemy 2.0  
✅ **Validação de Entrada**: Pydantic 2.x garante dados válidos  
✅ **Tratamento de Erros**: Respostas HTTP apropriadas e mensagens claras  
✅ **Separação de Responsabilidades**: Models, Schemas e Routes bem definidos  
✅ **Relacionamentos Complexos**: One-to-Many (Artista → Álbum) e Many-to-Many (Álbum ↔ Gênero) com integridade referencial via `ForeignKey`  
✅ **Documentação Automática**: Swagger UI gerada automaticamente  
✅ **Dependency Injection**: Uso de `Depends` do FastAPI para gerenciar sessões  
✅ **Validação de Ambiente**: Verificação de `DATABASE_URL` com tratamento de erros  
✅ **Docstrings**: Documentação de classes e relacionamentos nos models  
✅ **TYPE_CHECKING**: Uso de imports condicionais para evitar circular imports  

## 🧪 Testando a API

Use a Swagger UI integrada (`http://localhost:8000/docs`) para testar os endpoints interativamente, ou ferramentas como Postman / Insomnia / `curl`.

Exemplo rápido (criar artista):
```bash
curl -X POST "http://localhost:8000/artistas/" \
  -H "Content-Type: application/json" \
  -d '{"nome":"The Beatles","pais_origem":"Reino Unido","ano_formacao":1960}'
```

## 🩹 Solução de Problemas

### `permissão negada para esquema public` (PostgreSQL 15+)

A partir do PostgreSQL 15, usuários comuns deixaram de ter permissão automática para criar objetos no schema `public`. Se `Base.metadata.create_all(bind=engine)` falhar com esse erro, conecte-se ao banco com um usuário administrador (ex: `postgres`) e conceda a permissão ao usuário usado na `DATABASE_URL`:

```sql
GRANT ALL ON SCHEMA public TO seu_usuario;
```

## 📈 Possíveis Extensões

- Adicionar autenticação e autorização (JWT)
- Implementar paginação nos endpoints GET
- Adicionar busca e filtros avançados
- Criar testes unitários (pytest)
- Implementar cache (Redis)
- Adicionar logging estruturado
- Implementar CI/CD (GitHub Actions)

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido por Filipe Madeira como exemplo de API REST profissional com FastAPI e SQLAlchemy.

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**

# 🎵 Biblioteca de Música - API REST

Uma API REST moderna e bem estruturada para gerenciamento de uma biblioteca de música, desenvolvida com FastAPI e SQLAlchemy. Demonstra boas práticas em design de APIs, validação de dados e modelagem de banco de dados.

## ✨ Características Principais

- **CRUD Completo**: Operações Create, Read, Update e Delete para Artistas, Gêneros e Álbuns
- **Relacionamentos Complexos**: Suporte a relacionamentos One-to-Many e Many-to-Many
- **Validação de Dados**: Validação automática com Pydantic em todas as requisições
- **Tratamento de Erros**: Respostas HTTP apropriadas com mensagens de erro descritivas
- **Documentação Interativa**: Swagger UI integrado para testar endpoints
- **Type Hints**: Código totalmente tipado para melhor qualidade e manutenibilidade

## 🛠️ Stack Tecnológico

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **FastAPI** | 0.139.2 | Framework web de alta performance |
| **SQLAlchemy** | 2.0.51 | ORM para manipulação de banco de dados |
| **PostgreSQL** | - | Banco de dados relacional |
| **Pydantic** | 2.13.4 | Validação de dados e serialização |
| **Uvicorn** | 0.51.0 | Servidor ASGI |

## 📋 Pré-requisitos

- Python 3.9+
- PostgreSQL 12+
- pip ou poetry

## 🚀 Instalação

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
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
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação da API

Acesse a documentação interativa em:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Arquitetura e Estrutura

```
biblioteca_de_musica/
├── main.py          # Aplicação principal e definição de rotas
├── models.py        # Modelos SQLAlchemy (Artista, Genero, Album)
├── schemas.py       # Esquemas Pydantic para validação
├── database.py      # Configuração e sessão do banco de dados
├── requirements.txt # Dependências do projeto
└── README.md        # Este arquivo
```

### Modelos de Dados

#### Artista
- `id` (int): Identificador único
- `nome` (str): Nome do artista
- `pais_origem` (str): País de origem
- `ano_formacao` (int): Ano de formação

#### Gênero
- `id` (int): Identificador único
- `nome` (str): Nome do gênero musical

#### Álbum
- `id` (int): Identificador único
- `titulo` (str): Título do álbum
- `artista_id` (int): Referência ao artista (usado na criação/atualização)
- `artista` (str): Nome do artista (retornado nas respostas)
- `genero_ids` (list[int]): Ids dos gêneros associados (usado na criação/atualização)
- `generos` (list): Lista de gêneros associados, com `id` e `nome` (retornado nas respostas)

> A relação entre Álbum e Gênero é muitos-para-muitos, implementada através de uma tabela associativa (`album_genero`) que guarda os pares `album_id` / `genero_id`.

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
✅ **Type Hints**: Tipagem completa para melhor manutenibilidade  
✅ **Validação de Entrada**: Pydantic garante dados válidos  
✅ **Tratamento de Erros**: Respostas HTTP apropriadas e mensagens claras  
✅ **Separação de Responsabilidades**: Models, Schemas e Routes bem definidos  
✅ **Relacionamentos Complexos**: One-to-Many (Artista → Álbum) e Many-to-Many (Álbum ↔ Gênero) com integridade referencial via `ForeignKey`  
✅ **Documentação Automática**: Swagger UI gerada automaticamente  
✅ **Dependency Injection**: Uso de `Depends` do FastAPI para gerenciar sessões  

## 🧪 Testando a API

Use a Swagger UI integrada (`http://localhost:8000/docs`) para testar todos os endpoints interativamente, ou use ferramentas como:
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- `curl` via terminal

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

Desenvolvido como exemplo de API REST profissional com FastAPI e SQLAlchemy.

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**
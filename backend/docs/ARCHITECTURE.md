# Cognet Backend Architecture

## Architecture Flow

```
HTTP Request
    ↓
API Layer (Routes, Endpoints)
    ↓
Application Layer (Use Cases, Orchestration)
    ↓
Domain Layer (Entities, Business Logic)
    ↓
Core Layer (Intelligence Engines)
    ↓
Infrastructure Layer (External Integrations)
    ↓
External APIs (OpenAI, MongoDB, etc.)
```

---

## Layer Breakdown

### 1. API Layer (`app/api/`)

**Purpose:** Entry point for all HTTP requests.

**Responsibilities:**
- Receive and validate HTTP requests
- Route requests to appropriate handlers
- Serialize/deserialize payloads
- Handle middleware concerns (auth, logging, CORS)

**Components:**
- `router.py` - Main API router that combines all endpoints
- `deps.py` - Dependency injection for shared resources
- `middleware.py` - Custom middleware for cross-cutting concerns
- `v1/` - Versioned API endpoints (chat, memory, context)

**Example Flow:**
```
POST /api/v1/chat
  ↓
ChatRouter receives request
  ↓
Validates ChatRequest schema
  ↓ Passes to Application Layer
```

---

### 2. Application Layer (`app/application/`)

**Purpose:** Orchestrates business logic and use cases.

**Responsibilities:**
- Implement business workflows
- Coordinate between domain and infrastructure
- Handle transactional concerns
- Implement authorization and access control

**Components:**
- `chat_usecase.py` - Chat interaction workflow
- `memory_usecase.py` - Memory management workflow

**Example Flow:**
```
ChatRequest received
  ↓
ChatUseCase orchestrates:
  1. Retrieve relevant context (Domain → Core → Infrastructure)
  2. Generate embedding (Domain → Core)
  3. Execute reasoning (Domain → Core)
  4. Store interaction (Domain → Infrastructure)
  ↓ Returns ChatResponse
```

---

### 3. Domain Layer (`app/domain/`)

**Purpose:** Contains business entities and domain logic.

**Responsibilities:**
- Define business entities (Memory, Context, Agent)
- Implement domain business rules
- Repository pattern for data persistence
- Service classes for domain operations

**Components:**

#### Memory Domain
- `memory/entity.py` - Memory entity definitions
- `memory/service.py` - Memory business logic
- `memory/repository.py` - Memory data access

#### Context Domain
- `context/entity.py` - Context entity definitions
- `context/service.py` - Context business logic

#### Agent Domain
- `agent/entity.py` - Agent entity definitions
- `agent/service.py` - Agent business logic

**Example Flow:**
```
MemoryService receives request to store memory
  ↓
Validates memory entity against business rules
  ↓
Calls MemoryRepository to persist
  ↓ Returns stored memory with ID
```

---

### 4. Core Layer (`app/core/`)

**Purpose:** Intelligence engine - the "secret sauce" of Cognet.

**Responsibilities:**
- Semantic embeddings and vector operations
- Intelligent retrieval and ranking
- Context building and synthesis
- Reasoning and inference

**Components:**

#### Embedding (`core/embedding/`)
- `engine.py` - Generates embeddings for content

#### Retrieval (`core/retrieval/`)
- `semantic.py` - Semantic search across memory
- `ranking.py` - Rank retrieved results by relevance

#### Context (`core/context/`)
- `builder.py` - Synthesizes relevant context for reasoning

#### Inference (`core/inference/`)
- `reasoning.py` - AI reasoning and decision logic

**Example Flow:**
```
User query: "What was I working on yesterday?"
  ↓
1. EmbeddingEngine converts query to vector
  ↓
2. SemanticRetrieval finds similar memories
  ↓
3. RankingEngine prioritizes by relevance
  ↓
4. ContextBuilder synthesizes response
  ↓
5. ReasoningEngine generates intelligent response
  ↓ Returns contextual answer
```

---

### 5. Infrastructure Layer (`app/infrastructure/`)

**Purpose:** Manages connections to external systems.

**Responsibilities:**
- Database connections and queries
- External API client integration
- Logging and monitoring
- Configuration and secrets management

**Components:**

#### Database (`infrastructure/db/mongo/`)
- `client.py` - MongoDB connection management
- `collections.py` - Collection definitions
- `base_repository.py` - Base class for all repositories

#### AI (`infrastructure/ai/`)
- `openai_client.py` - OpenAI API integration

#### Logging (`infrastructure/logging/`)
- `logger.py` - Centralized logging

**Example Flow:**
```
MemoryRepository.save(memory)
  ↓
MongoClient.insert_one(memory_doc)
  ↓
MongoDB stores document
  ↓ Returns inserted ID
```

---

### 6. External APIs

**Purpose:** Third-party services that power Cognet.

**Services:**
- **OpenAI API** - Embeddings, reasoning, language models
- **MongoDB** - Document storage and vector search
- **Logging Services** - Application observability

**Examples:**
- Embedding generation: `app.inference.embedding_engine` → OpenAI `/v1/embeddings`
- Memory storage: `app.infrastructure.db.mongo` → MongoDB insert
- Vector search: `app.core.retrieval.semantic` → MongoDB vector search

---

## Request/Response Flow Example

### User Chat Interaction

```
1. API LAYER
   POST /api/v1/chat
   Request: { "message": "What was I doing?" }
   ↓

2. APPLICATION LAYER (ChatUseCase)
   Orchestrates entire workflow:
   - Get user context
   - Process message
   - Generate response
   ↓

3. DOMAIN LAYER
   MemoryService.find_relevant(user_id, query)
   ContextService.build(user_id, relevant_memories)
   ↓

4. CORE LAYER
   EmbeddingEngine.encode(query)
     → Calls OpenAI
   SemanticRetrieval.search(embedding)
     → Searches MongoDB vectors
   ContextBuilder.synthesize(memories)
   ReasoningEngine.generate_response(context)
     → Calls OpenAI reasoning
   ↓

5. INFRASTRUCTURE LAYER
   MongoClient.find(filters, options)
   OpenAIClient.request(embeddings, reasoning)
   Logger.info(event)
   ↓

6. EXTERNAL APIS
   OpenAI API: /v1/embeddings, /v1/chat
   MongoDB: Query and vector search operations
   ↓

7. RESPONSE
   Returns synthesized response with context
   HTTP 200: { "response": "You were working on..." }
```

---

## Data Flow Pattern

### Unidirectional Dependency

Each layer only depends on layers **below** it:

```
API ↓
Application ↓
Domain ↓
Core ↓
Infrastructure ↓
External APIs
```

**Benefits:**
- Clean separation of concerns
- Easy testing (mock lower layers)
- Independent development
- Clear data flow
- No circular dependencies

---

## Key Principles

1. **API Layer** - Handles HTTP contract
2. **Application Layer** - Orchestrates workflows
3. **Domain Layer** - Business rules and logic
4. **Core Layer** - Intelligence and reasoning
5. **Infrastructure Layer** - Technical details
6. **External APIs** - Third-party integrations

Each layer has a single responsibility and communicates with the layer below.

---

## Testing Strategy

- **API Tests:** Mock Application layer
- **Application Tests:** Mock Domain/Core layer
- **Domain Tests:** Mock Infrastructure layer
- **Core Tests:** Unit tests on algorithms
- **Infrastructure Tests:** Integration tests with real/test databases

---

## Folder Mapping

```
backend/app/
├── api/              → API Layer
├── application/      → Application Layer
├── domain/           → Domain Layer
├── core/             → Core Layer (Intelligence)
├── infrastructure/   → Infrastructure Layer (External connections)
├── schemas/          → Data contracts
├── config/           → Configuration
└── utils/            → Shared utilities
```

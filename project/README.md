# Provisio Backend

FastAPI backend for group shopping organization with real-time features via Socket.IO.

## Tech Stack

- Python 3.11
- FastAPI + uvicorn
- Pydantic for data validation
- Firebase Admin SDK (Authentication + Firestore)
- Socket.IO (python-socketio) for real-time features
- pytest for testing
- Docker + docker-compose
- Black + Ruff for code formatting and linting

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment variables & Firebase initialization
│   ├── deps.py              # Authentication dependencies
│   ├── models.py            # Pydantic schemas
│   ├── realtime.py          # Socket.IO event handlers
│   ├── routers/
│   │   ├── users.py         # User endpoints
│   │   ├── groups.py        # Group management endpoints
│   │   ├── products.py      # Product CRUD endpoints
│   │   ├── catalog.py       # Product catalog/presets
│   │   └── chat.py          # Chat history endpoint
│   └── repositories/
│       └── firestore.py     # Firestore CRUD operations
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_groups.py       # Group tests
│   └── test_products.py     # Product tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Setup

### Prerequisites

- Python 3.11+
- Firebase project with Firestore enabled
- Firebase service account credentials

### Installation

1. Clone the repository

2. Copy `.env.example` to `.env` and fill in your Firebase credentials:

```bash
cp .env.example .env
```

3. Update `.env` with your Firebase credentials:

```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-client-email
FIREBASE_DB_URL=https://your-project-id.firebaseio.com
PORT=8000
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
uvicorn app.main:socket_app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. Build and run with docker-compose:

```bash
docker-compose up --build
```

## API Documentation

Once running, visit:
- API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### Base URL: `/api/v1`

### Authentication

All endpoints (except `/` and `/health`) require Firebase authentication. Include the Firebase ID token in the Authorization header:

```
Authorization: Bearer <firebase-id-token>
```

### Users

- `GET /users/me` - Get current user info

### Groups

- `POST /groups` - Create a new group
- `GET /groups` - List user's groups
- `GET /groups/{group_id}` - Get group details
- `DELETE /groups/{group_id}` - Delete group (owner only)
- `POST /groups/{group_id}/members/{member_id}` - Add member to group
- `DELETE /groups/{group_id}/members/{member_id}` - Remove member from group

### Products

- `POST /groups/{group_id}/products` - Create product
- `GET /groups/{group_id}/products` - List group products
- `GET /groups/{group_id}/products/{product_id}` - Get product details
- `PATCH /groups/{group_id}/products/{product_id}` - Update product
- `DELETE /groups/{group_id}/products/{product_id}` - Delete product

### Catalog

- `GET /catalog/products` - Get preset products list

### Chat

- `GET /groups/{group_id}/messages` - Get chat history (with limit parameter)

## WebSocket Events

### Connection

Connect to: `ws://localhost:8000/ws`

Authentication required via Socket.IO auth:

```javascript
const socket = io('http://localhost:8000/ws', {
  auth: {
    token: '<firebase-id-token>'
  }
});
```

### Events

#### Client → Server

- `join_group` - Join a group room
  ```json
  { "groupId": "group-id" }
  ```

- `leave_group` - Leave a group room
  ```json
  { "groupId": "group-id" }
  ```

- `chat_message` - Send a chat message
  ```json
  { "groupId": "group-id", "text": "Hello!" }
  ```

- `product_updated` - Notify product update
  ```json
  { "groupId": "group-id", "productId": "product-id" }
  ```

- `presence` - Update user presence
  ```json
  { "groupId": "group-id", "status": "online" }
  ```

#### Server → Client

- `joined_group` - Confirmation of joining group
- `left_group` - Confirmation of leaving group
- `user_joined` - Another user joined the group
- `user_left` - Another user left the group
- `chat_message` - New chat message in group
- `product_updated` - Product was updated
- `presence` - User presence update
- `error` - Error message

## Data Models

### User
```json
{
  "id": "string",
  "username": "string",
  "displayName": "string",
  "email": "string",
  "photoURL": "string | null",
  "createdAt": "datetime"
}
```

### Group
```json
{
  "id": "string",
  "name": "string",
  "description": "string | null",
  "ownerId": "string",
  "members": ["userId1", "userId2"],
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### Product
```json
{
  "id": "string",
  "groupId": "string",
  "name": "string",
  "assigneeUserId": "string | null",
  "status": "pending | bought",
  "quantity": "number",
  "notes": "string | null",
  "preset": "string | null",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### ChatMessage
```json
{
  "id": "string",
  "groupId": "string",
  "userId": "string",
  "text": "string",
  "createdAt": "datetime"
}
```

## Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## Code Quality

Format code with Black:

```bash
black app/ tests/
```

Lint with Ruff:

```bash
ruff check app/ tests/
```

## Development

The application uses:
- FastAPI for REST API
- Socket.IO for real-time bidirectional communication
- Firebase Admin SDK for authentication and Firestore database
- Pydantic for data validation and serialization

### Adding New Endpoints

1. Create a new router in `app/routers/`
2. Register it in `app/main.py`
3. Add tests in `tests/`

### Adding New Socket.IO Events

1. Add event handler in `app/realtime.py`
2. Ensure proper authentication and authorization checks

## License

MIT

import socketio
from firebase_admin import auth as firebase_auth
from app.repositories.firestore import repo


sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)


async def verify_token(token: str):
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None


@sio.event
async def connect(sid, environ, auth):
    print(f"Client {sid} attempting to connect")

    if not auth or 'token' not in auth:
        print(f"Client {sid} rejected: no token provided")
        return False

    user = await verify_token(auth['token'])
    if not user:
        print(f"Client {sid} rejected: invalid token")
        return False

    async with sio.session(sid) as session:
        session['user_id'] = user.get('uid')

    print(f"Client {sid} connected as user {user.get('uid')}")
    return True


@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")


@sio.event
async def join_group(sid, data):
    group_id = data.get('groupId')

    if not group_id:
        await sio.emit('error', {'message': 'groupId is required'}, room=sid)
        return

    async with sio.session(sid) as session:
        user_id = session.get('user_id')

    if not user_id:
        await sio.emit('error', {'message': 'Unauthorized'}, room=sid)
        return

    group = await repo.get_group(group_id)
    if not group:
        await sio.emit('error', {'message': 'Group not found'}, room=sid)
        return

    if user_id not in group.get('members', []):
        await sio.emit('error', {'message': 'Not a member of this group'}, room=sid)
        return

    sio.enter_room(sid, f"group:{group_id}")
    await sio.emit('joined_group', {'groupId': group_id}, room=sid)
    await sio.emit('user_joined', {'userId': user_id}, room=f"group:{group_id}", skip_sid=sid)
    print(f"User {user_id} joined group {group_id}")


@sio.event
async def leave_group(sid, data):
    group_id = data.get('groupId')

    if not group_id:
        return

    async with sio.session(sid) as session:
        user_id = session.get('user_id')

    sio.leave_room(sid, f"group:{group_id}")
    await sio.emit('left_group', {'groupId': group_id}, room=sid)
    await sio.emit('user_left', {'userId': user_id}, room=f"group:{group_id}")
    print(f"User {user_id} left group {group_id}")


@sio.event
async def chat_message(sid, data):
    group_id = data.get('groupId')
    text = data.get('text')

    if not group_id or not text:
        await sio.emit('error', {'message': 'groupId and text are required'}, room=sid)
        return

    async with sio.session(sid) as session:
        user_id = session.get('user_id')

    if not user_id:
        await sio.emit('error', {'message': 'Unauthorized'}, room=sid)
        return

    group = await repo.get_group(group_id)
    if not group or user_id not in group.get('members', []):
        await sio.emit('error', {'message': 'Not a member of this group'}, room=sid)
        return

    message_data = {
        'groupId': group_id,
        'userId': user_id,
        'text': text,
    }

    message = await repo.create_chat_message(message_data)

    await sio.emit('chat_message', {
        'id': message['id'],
        'groupId': message['groupId'],
        'userId': message['userId'],
        'text': message['text'],
        'createdAt': message['createdAt'].isoformat(),
    }, room=f"group:{group_id}")


@sio.event
async def product_updated(sid, data):
    group_id = data.get('groupId')
    product_id = data.get('productId')

    if not group_id or not product_id:
        await sio.emit('error', {'message': 'groupId and productId are required'}, room=sid)
        return

    async with sio.session(sid) as session:
        user_id = session.get('user_id')

    if not user_id:
        await sio.emit('error', {'message': 'Unauthorized'}, room=sid)
        return

    group = await repo.get_group(group_id)
    if not group or user_id not in group.get('members', []):
        await sio.emit('error', {'message': 'Not a member of this group'}, room=sid)
        return

    product = await repo.get_product(product_id)
    if not product:
        await sio.emit('error', {'message': 'Product not found'}, room=sid)
        return

    await sio.emit('product_updated', {
        'id': product['id'],
        'groupId': product['groupId'],
        'name': product['name'],
        'assigneeUserId': product.get('assigneeUserId'),
        'status': product['status'],
        'quantity': product['quantity'],
        'notes': product.get('notes'),
        'preset': product.get('preset'),
        'updatedAt': product['updatedAt'].isoformat(),
    }, room=f"group:{group_id}")


@sio.event
async def presence(sid, data):
    group_id = data.get('groupId')
    status = data.get('status')

    if not group_id or not status:
        return

    async with sio.session(sid) as session:
        user_id = session.get('user_id')

    if not user_id:
        return

    await sio.emit('presence', {
        'userId': user_id,
        'status': status,
    }, room=f"group:{group_id}", skip_sid=sid)

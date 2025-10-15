from datetime import datetime
from typing import Optional, List, Dict, Any
from firebase_admin import firestore
from app.config import get_firestore_client


class FirestoreRepository:
    def __init__(self):
        self.db = get_firestore_client()

    def _doc_to_dict(self, doc) -> Optional[Dict[str, Any]]:
        if not doc.exists:
            return None
        data = doc.to_dict()
        data['id'] = doc.id
        return data

    async def create_user(self, user_id: str, user_data: dict) -> dict:
        user_ref = self.db.collection('users').document(user_id)
        user_data['createdAt'] = datetime.utcnow()
        user_ref.set(user_data)
        return {**user_data, 'id': user_id}

    async def get_user(self, user_id: str) -> Optional[dict]:
        user_ref = self.db.collection('users').document(user_id)
        doc = user_ref.get()
        return self._doc_to_dict(doc)

    async def create_group(self, group_data: dict) -> dict:
        group_ref = self.db.collection('groups').document()
        now = datetime.utcnow()
        group_data['createdAt'] = now
        group_data['updatedAt'] = now
        group_data['members'] = group_data.get('members', [])
        group_ref.set(group_data)
        return {**group_data, 'id': group_ref.id}

    async def get_group(self, group_id: str) -> Optional[dict]:
        group_ref = self.db.collection('groups').document(group_id)
        doc = group_ref.get()
        return self._doc_to_dict(doc)

    async def update_group(self, group_id: str, update_data: dict) -> Optional[dict]:
        group_ref = self.db.collection('groups').document(group_id)
        update_data['updatedAt'] = datetime.utcnow()
        group_ref.update(update_data)
        return await self.get_group(group_id)

    async def delete_group(self, group_id: str) -> bool:
        group_ref = self.db.collection('groups').document(group_id)
        group_ref.delete()
        return True

    async def list_user_groups(self, user_id: str) -> List[dict]:
        groups_ref = self.db.collection('groups')
        query = groups_ref.where('members', 'array_contains', user_id)
        docs = query.stream()
        return [self._doc_to_dict(doc) for doc in docs]

    async def add_member_to_group(self, group_id: str, user_id: str) -> Optional[dict]:
        group_ref = self.db.collection('groups').document(group_id)
        group_ref.update({
            'members': firestore.ArrayUnion([user_id]),
            'updatedAt': datetime.utcnow()
        })
        return await self.get_group(group_id)

    async def remove_member_from_group(self, group_id: str, user_id: str) -> Optional[dict]:
        group_ref = self.db.collection('groups').document(group_id)
        group_ref.update({
            'members': firestore.ArrayRemove([user_id]),
            'updatedAt': datetime.utcnow()
        })
        return await self.get_group(group_id)

    async def create_product(self, product_data: dict) -> dict:
        product_ref = self.db.collection('products').document()
        now = datetime.utcnow()
        product_data['createdAt'] = now
        product_data['updatedAt'] = now
        product_ref.set(product_data)
        return {**product_data, 'id': product_ref.id}

    async def get_product(self, product_id: str) -> Optional[dict]:
        product_ref = self.db.collection('products').document(product_id)
        doc = product_ref.get()
        return self._doc_to_dict(doc)

    async def update_product(self, product_id: str, update_data: dict) -> Optional[dict]:
        product_ref = self.db.collection('products').document(product_id)
        update_data['updatedAt'] = datetime.utcnow()
        product_ref.update(update_data)
        return await self.get_product(product_id)

    async def delete_product(self, product_id: str) -> bool:
        product_ref = self.db.collection('products').document(product_id)
        product_ref.delete()
        return True

    async def list_group_products(self, group_id: str) -> List[dict]:
        products_ref = self.db.collection('products')
        query = products_ref.where('groupId', '==', group_id)
        docs = query.stream()
        return [self._doc_to_dict(doc) for doc in docs]

    async def create_chat_message(self, message_data: dict) -> dict:
        message_ref = self.db.collection('messages').document()
        message_data['createdAt'] = datetime.utcnow()
        message_ref.set(message_data)
        return {**message_data, 'id': message_ref.id}

    async def list_group_messages(self, group_id: str, limit: int = 100) -> List[dict]:
        messages_ref = self.db.collection('messages')
        query = messages_ref.where('groupId', '==', group_id).order_by('createdAt', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        messages = [self._doc_to_dict(doc) for doc in docs]
        return list(reversed(messages))


repo = FirestoreRepository()

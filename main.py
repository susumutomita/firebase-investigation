import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate("path/to/serviceAccount.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client()
import datetime

def save_availability_data(facility_id, availability_data):
    """
    施設の空き情報をFirestoreに保存する関数
    :param facility_id: 施設のID
    :param availability_data: 空き情報のデータ
    """
    # Firestoreのコレクションを指定
    collection_ref = db.collection('facility_availability')

    # ドキュメントのIDを施設IDに基づいて設定
    doc_ref = collection_ref.document(facility_id)

    # 保存するデータにタイムスタンプを追加
    availability_data['timestamp'] = datetime.datetime.now()

    # Firestoreにデータを保存
    doc_ref.set(availability_data)

def get_availability_data(facility_id):
    """
    Firestoreから施設の空き情報を取得する関数
    :param facility_id: 施設のID
    :return: 空き情報のデータ
    """
    # Firestoreのコレクションを指定
    collection_ref = db.collection('facility_availability')

    # ドキュメントのIDを施設IDに基づいて取得
    doc_ref = collection_ref.document(facility_id)

    # Firestoreからデータを取得
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

# テスト用のデータ
facility_id = 'example_facility'
availability_data = {
    'available_slots': 5,
    'last_checked': datetime.datetime.now()
}

# データを保存
save_availability_data(facility_id, availability_data)

# データを取得して表示
retrieved_data = get_availability_data(facility_id)
print(retrieved_data)

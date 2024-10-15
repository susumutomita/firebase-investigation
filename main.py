import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数からサーティフィケイトのパスを取得
cert_path = os.getenv("FIREBASE_CERTIFICATE_PATH")
if not cert_path:
    raise ValueError("環境変数 'FIREBASE_CERTIFICATE_PATH' が設定されていません")

# 環境変数からコレクション名を取得
collection_name = os.getenv("FIREBASE_COLLECTION_NAME")
if not collection_name:
    raise ValueError("環境変数 'FIREBASE_COLLECTION_NAME' が設定されていません")

cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred)
print("firebase_admin initialized")

# Firestoreに対してデータの取得クエリ
db = firestore.client()
docs = db.collection(collection_name).get()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")

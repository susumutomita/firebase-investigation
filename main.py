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

# Firestoreに対してデータの書き込み
db = firestore.client()
doc_ref = db.collection(collection_name).document("new_document")

# 書き込むデータ
data = {
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@example.com"
}

# データをFirestoreに書き込む
doc_ref.set(data)
print("データが書き込まれました")

# 書き込まれたデータを取得して確認
written_data = doc_ref.get().to_dict()
if written_data == data:
    print("データが正しく書き込まれました")
else:
    print("データの書き込みに失敗しました")

# 書き込まれたデータを表示
print("書き込まれたデータ:", written_data)

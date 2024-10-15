import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from flask import Flask, jsonify, request

app = Flask(__name__)

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


@app.route("/data", methods=["GET"])
def get_data():
    # Firestoreからデータを取得
    doc = doc_ref.get()
    if doc.exists:
        return jsonify(doc.to_dict()), 200
    else:
        return jsonify({"error": "データが見つかりません"}), 404


@app.route("/data", methods=["POST"])
def post_data():
    # リクエストからデータを取得
    data = request.json
    if not data:
        return jsonify({"error": "データが提供されていません"}), 400

    # データをFirestoreに書き込む
    doc_ref.set(data)
    return jsonify({"message": "データが書き込まれました"}), 201


if __name__ == "__main__":
    app.run(debug=True)

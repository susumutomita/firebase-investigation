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

# Firestoreクライアントの初期化
db = firestore.client()
collection_ref = db.collection(collection_name)


@app.route("/data", methods=["GET"])
def get_all_data():
    """Firestoreから全てのデータを取得するエンドポイント"""
    try:
        docs = collection_ref.stream()
        data = {doc.id: doc.to_dict() for doc in docs}
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data/<doc_id>", methods=["GET"])
def get_data(doc_id):
    """Firestoreから特定のドキュメントを取得するエンドポイント"""
    try:
        doc = collection_ref.document(doc_id).get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": f"ドキュメント '{doc_id}' が見つかりません"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["POST"])
def create_or_update_data():
    """Firestoreにデータを追加または更新するエンドポイント（アップサート）"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "データが提供されていません"}), 400

        doc_id = data.get("id")

        if doc_id:
            # 指定されたIDでドキュメントをセット（アップサート）
            collection_ref.document(doc_id).set(data, merge=True)
            return jsonify({"message": f"ドキュメント '{doc_id}' が追加/更新されました"}), 201
        else:
            # ドキュメントIDを自動生成して追加
            doc_ref = collection_ref.add(data)
            return jsonify({"message": "新しいドキュメントが追加されました", "id": doc_ref[1].id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data/<doc_id>", methods=["DELETE"])
def delete_data(doc_id):
    """Firestoreから特定のドキュメントを削除するエンドポイント"""
    try:
        doc = collection_ref.document(doc_id).get()
        if doc.exists:
            collection_ref.document(doc_id).delete()
            return jsonify({"message": f"ドキュメント '{doc_id}' が削除されました"}), 200
        else:
            return jsonify({"error": f"ドキュメント '{doc_id}' が見つかりません"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # すべての外部からのアクセスを許可し、指定ポートでサーバーを起動
    app.run(host="0.0.0.0", port=8000, debug=True)

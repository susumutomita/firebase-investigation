import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)

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
@swag_from({
    'responses': {
        200: {
            'description': '全てのデータを取得',
            'schema': {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object'
                }
            }
        },
        500: {
            'description': 'サーバーエラー'
        }
    }
})
def get_all_data():
    """Firestoreから全てのデータを取得するエンドポイント
    ---
    tags:
      - Data
    responses:
      200:
        description: 全てのデータを取得
      500:
        description: サーバーエラー
    """
    try:
        docs = collection_ref.stream()
        data = {doc.id: doc.to_dict() for doc in docs}
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data/<doc_id>", methods=["GET"])
@swag_from({
    'parameters': [
        {
            'name': 'doc_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': '取得するドキュメントのID'
        }
    ],
    'responses': {
        200: {
            'description': 'ドキュメントを取得',
            'schema': {
                'type': 'object'
            }
        },
        404: {
            'description': 'ドキュメントが見つからない'
        },
        500: {
            'description': 'サーバーエラー'
        }
    }
})
def get_data(doc_id):
    """Firestoreから特定のドキュメントを取得するエンドポイント
    ---
    tags:
      - Data
    parameters:
      - name: doc_id
        in: path
        type: string
        required: true
        description: 取得するドキュメントのID
    responses:
      200:
        description: ドキュメントを取得
      404:
        description: ドキュメントが見つからない
      500:
        description: サーバーエラー
    """
    try:
        doc = collection_ref.document(doc_id).get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": f"ドキュメント '{doc_id}' が見つかりません"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'ドキュメントID（省略可）'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'email': {
                        'type': 'string'
                    },
                    'age': {
                        'type': 'integer'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'データが作成/更新された',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'id': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'データが提供されていません'
        },
        500: {
            'description': 'サーバーエラー'
        }
    }
})
def create_or_update_data():
    """Firestoreにデータを追加または更新するエンドポイント（アップサート）
    ---
    tags:
      - Data
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: string
              description: ドキュメントID（省略可）
            name:
              type: string
            email:
              type: string
            age:
              type: integer
    responses:
      201:
        description: データが作成/更新された
      400:
        description: データが提供されていません
      500:
        description: サーバーエラー
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "データが提供されていません"}), 400

        doc_id = data.get("id")

        if doc_id:
            # 指定されたIDでドキュメントをセット（アップサート）
            collection_ref.document(doc_id).set(data, merge=True)
            return jsonify({
                "message": f"ドキュメント '{doc_id}' が追加/更新されました",
                "id": doc_id
            }), 201
        else:
            # ドキュメントIDを自動生成して追加
            doc_ref = collection_ref.add(data)
            return jsonify({
                "message": "新しいドキュメントが追加されました",
                "id": doc_ref[1].id
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/data/<doc_id>", methods=["DELETE"])
@swag_from({
    'parameters': [
        {
            'name': 'doc_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': '削除するドキュメントのID'
        }
    ],
    'responses': {
        200: {
            'description': 'ドキュメントが削除された'
        },
        404: {
            'description': 'ドキュメントが見つからない'
        },
        500: {
            'description': 'サーバーエラー'
        }
    }
})
def delete_data(doc_id):
    """Firestoreから特定のドキュメントを削除するエンドポイント
    ---
    tags:
      - Data
    parameters:
      - name: doc_id
        in: path
        type: string
        required: true
        description: 削除するドキュメントのID
    responses:
      200:
        description: ドキュメントが削除された
      404:
        description: ドキュメントが見つからない
      500:
        description: サーバーエラー
    """
    try:
        doc = collection_ref.document(doc_id).get()
        if doc.exists:
            collection_ref.document(doc_id).delete()
            return jsonify({"message": f"ドキュメント '{doc_id}' が削除されました"}), 200
        else:
            return jsonify({"error": f"ドキュメント '{doc_id}' が見つかりません"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    """Swagger UIのトップページ
    ---
    description: Swagger UIにリダイレクト
    responses:
      302:
        description: Swagger UIへリダイレクト
    """
    return jsonify({"message": "Swagger UIへアクセスするには /apidocs/ を使用してください."}), 200


@app.route("/data/write", methods=["POST"])
def write_data():
    """Firestoreにデータを書き込むエンドポイント
    ---
    tags:
      - Data
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            field1:
              type: string
            field2:
              type: string
    responses:
      200:
        description: データが正常に書き込まれた
      400:
        description: 無効なリクエスト
      500:
        description: サーバーエラー
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "無効なリクエスト"}), 400

        doc_ref = collection_ref.add(data)
        return jsonify({
            "message": "データが正常に書き込まれました",
            "id": doc_ref[1].id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # すべての外部からのアクセスを許可し、指定ポートでサーバーを起動
    app.run(host="0.0.0.0", port=8000, debug=True)

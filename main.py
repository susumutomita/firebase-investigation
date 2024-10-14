import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# サービスアカウントキーのパスを指定
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://your-database-name.firebaseio.com/"}
)

# データの参照
ref = db.reference("/")
data = ref.get()
logger.info(f"データの参照: {data}")

# データの書き込み
new_user_ref = ref.child("users").push(
    {"name": "John Doe", "email": "john@example.com"}
)
logger.info(f"データの書き込み: {new_user_ref.key}")

# データの更新
ref.child("users/user_id").update({"name": "Jane Doe"})
logger.info("データの更新: users/user_id の名前を Jane Doe に更新")

# データの削除
ref.child("users/user_id").delete()
logger.info("データの削除: users/user_id を削除")

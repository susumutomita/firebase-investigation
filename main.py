import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# サービスアカウントキーのパスを指定
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://your-database-name.firebaseio.com/"}
)

# データの参照
ref = db.reference("/")
data = ref.get()
print(data)

# データの書き込み
new_user_ref = ref.child("users").push(
    {"name": "John Doe", "email": "john@example.com"}
)

# データの更新
ref.child("users/user_id").update({"name": "Jane Doe"})

# データの削除
ref.child("users/user_id").delete()

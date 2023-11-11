import datetime

import Use_Database_sql

db = Use_Database_sql.Database()

def enter_room(id: str):  # 入室処理
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list_1d = []
    for i in range(len(id_list)):
        for j in range(len(id_list[i])):
            id_list_1d.append(id_list[i][j])  # id_listを1次元リストに変換
    if id not in id_list_1d:  # idがデータベースにない場合
        print("[Exit] No such ID in database.")
        return -1

    db.execute_database(
        "UPDATE student SET attendance = '出席' WHERE id = 'id003'"
    )  # 出席状況を欠席に変更
    dt = datetime.datetime.now()
    db.execute_database(
        "INSERT INTO log (id, year, month, day, hour, minute, second, attendance) VALUES ('"
        + id
        + "', '"
        + str(dt.year)
        + "', '"
        + str(dt.month)
        + "', '"
        + str(dt.day)
        + "', '"
        + str(dt.hour)
        + "', '"
        + str(dt.minute)
        + "', '"
        + str(dt.second)
        + "', '入室')"
    )  # ログに記録
    db.commit_database()  # データベースにコミットする
    print("[Enter] " + id + " Entered.", str(datetime.datetime.now()))


def get_fields_from_database(table: str):  # データベースからフィールドを取得
    ret = db.execute_database("PRAGMA table_info(" + table + ")")  # データベースからフィールドを取得
    fields = []
    for i in ret:
        fields.append(i[1])  # フィールドをリストに追加
    return fields


def add_student_to_database(data: dict):
    '''
    生徒をデータベースに新規に追加する。
    
    引数: 生徒の情報を格納した dict を渡す。この dict はデータベースのフィールドをキーに持つ必要がある。
    戻り値: 成功した場合は 0，失敗した場合は -1 を返す。
    '''
    
    fields_database = get_fields_from_database("student")  # データベースから生徒テーブルのフィールドを取得
    fields_data = list(data.keys())  # 引数のフィールドを取得
    for i in fields_database:  # 引数のフィールドがデータベースにあるか確認
        if i not in fields_data:
            print(
                "[Error] add_student_to_database: Failed to add data to database. Fields mismatch.: ",
                i,
            )
            return -1
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list_1d = []
    for i in range(len(id_list)):
        for j in range(len(id_list[i])):
            id_list_1d.append(id_list[i][j])
    if data["id"] in id_list_1d:  # idがデータベースにある場合
        print(
            "[Error] 生徒の追加に失敗しました。このカードはすでに登録されています。このカードを別の生徒に割り当てるには，まずこのカードを所有する生徒の除名を行ってください。 : ",
            data["name"],
        )
        return -1
    # データベースのフィールドの順番にdataを並び変える
    
    fdata = []
    for i in fields_database:
        fdata.append(data[i])
    

    # 引数の文字列を成形
    print(fdata)
    fields_attr = ", ".join(fields_database)  # フィールドをカンマ区切りにする
    data_attr = "', '".join(fdata)  # データをカンマ区切りにする

    if (
        db.execute_database(
            "INSERT INTO student (" + fields_attr + ") VALUES ('" + data_attr + "')"
        )
        == -1
    ):
        print("[Error] add_student_to_database: Couldn't add data to database.")
        return -1
    print("[Info] Added student to database. :", data["name"])


def add_systemlog_to_database(data: str):  # システムログをデータベースに追加
    dt = datetime.datetime.now()
    db.execute_database(
        "INSERT INTO system_log (year, month, day, hour, minute, second, operation) VALUES ('"
        + str(dt.year)
        + "', '"
        + str(dt.month)
        + "', '"
        + str(dt.day)
        + "', '"
        + str(dt.hour)
        + "', '"
        + str(dt.minute)
        + "', '"
        + str(dt.second)
        + "', '"
        + data
        + "')"
    )  # ログに記録
    db.commit_database()  # データベースにコミットする


def exit_room(id: str):  # 退室処理
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list_1d = []
    for i in range(len(id_list)):
        for j in range(len(id_list[i])):
            id_list_1d.append(id_list[i][j])  # id_listを1次元リストに変換
    if id not in id_list_1d:  # idがデータベースにない場合
        print("[Enter] No such ID in database.")
        return -1

    db.execute_database(
        "UPDATE student SET attendance = '退席' WHERE id = 'id003'"
    )  # 出席状況を欠席に変更
    dt = datetime.datetime.now()
    db.execute_database(
        "INSERT INTO log (id, year, month, day, hour, minute, second, attendance) VALUES ('"
        + id
        + "', '"
        + str(dt.year)
        + "', '"
        + str(dt.month)
        + "', '"
        + str(dt.day)
        + "', '"
        + str(dt.hour)
        + "', '"
        + str(dt.minute)
        + "', '"
        + str(dt.second)
        + "', '退出')"
    )  # ログに記録
    db.commit_database()  # データベースにコミットする
    print("[Exit] " + id + " Exited.", str(datetime.datetime.now()))
    
def commit_database():
    db.commit_database()
    
def disconnect_from_database():
    db.disconnect_from_database()
    
def rollback_database():
    db.rollback_database()
    
def connect_to_database():
    db.connect_to_database()
    
def execute_database(sql):
    return db.execute_database(sql)
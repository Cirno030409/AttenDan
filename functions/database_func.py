import datetime

import Use_Database_sql

db = Use_Database_sql.Database()


def get_fields_from_database(table: str):  # データベースからフィールドを取得
    """指定のテーブルのフィールドを取得する

    Args:
        table (str): 取得したいテーブル名

    Returns:
        fields (list): フィールドのリスト
    """
    ret = db.execute_database("PRAGMA table_info(" + table + ")")  # データベースからフィールドを取得
    fields = []
    for i in ret:
        fields.append(i[1])  # フィールドをリストに追加
    return fields

def get_dict_from_database(table: str):  # データベースから辞書を取得
    """指定したテーブルのデータベースから，フィールドをキーとした辞書を取得します。

    Args:
        table (str): テーブル名
    Returns:
        data (dict): フィールドをキーとした辞書
    """
    fields = get_fields_from_database(table)  # データベースからフィールドを取得
    data = execute_database("SELECT * FROM " + table)  # データベースからデータを取得
    
    dict_data = []
    for row in data:
        dict_row = {fields[i]: row[i] for i in range(len(fields))}
        dict_data.append(dict_row)
    return dict_data
    


def remove_student_from_database(id: str, name: str):
    """
    生徒をデータベースから除名する。対象のIDとそのIDに対応する名前が異なる場合，エラーを返し，除名しない。

    Args:
        id (str): 生徒のID
        name (str): 生徒の名前
        
    Returns:
        成功した場合は0, IDがデータベースにない場合は-1, IDに対応する名前が異なる場合は-2を返す。
    """
    
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list = [item for sublist in id_list for item in sublist]  # 2次元リストを1次元に変換

    if len(id_list) == 0 or id not in id_list:  # idがデータベースにない場合
        print("[Error] 生徒の除名に失敗しました。このカードは登録されていません。 : ", id)
        return -1
    else:
        touched_name = db.execute_database("SELECT name FROM student WHERE id = '%s'" % id)[0][0]

    if name != touched_name:  # idに対応する名前が異なる場合
        print(
            "[Error] 生徒の除名に失敗しました。除名しようとした名前と，タッチされたカードに登録されている名前が異なります。 : 除名しようとした名前: %s, カードに登録されている名前: %s" % (name,touched_name))
        return -2
    else:
        db.execute_database("DELETE FROM student WHERE id = '" + id + "'")  # 生徒データベースから除名
        db.execute_database("DELETE FROM parent WHERE id = '" + id + "'")  # 保護者データベースから除名
        db.commit_database()  # データベースにコミットする
        add_systemlog_to_database("生徒の除名: " + name)  # システムログに記録
        print("[Remove] " + name + " が除名されました。")


def add_student_to_database(data: dict):
    """
    生徒をデータベースに新規に追加する。

    Args:
        data (dict): 生徒の情報を格納した辞書。辞書のキーはフィールド名と同じにすること。
        
    Returns:
        成功した場合は0, すでに登録されている場合は-1, フィールドがデータベースにない場合は-2を返す。
    """
    fields_student = get_fields_from_database("student")  # データベースから生徒テーブルのフィールドを取得
    fields_parent = get_fields_from_database("parent")  # データベースから保護者テーブルのフィールドを取得
    fields = fields_student + fields_parent  # 二つのリストを連結
    for i in fields:  # 引数のフィールドがデータベースにあるか確認
        if i not in fields:
            print(
                "[Error] add_student_to_database: Failed to add data to database. Fields mismatch.: ",
                i,
            )
            return -2
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list = [item for sublist in id_list for item in sublist]  # 2次元リストを1次元に変換
    if len(id_list) != 0:  # データベースに生徒の情報が１つ以上ある場合
        if data["id"] in id_list:  # idがデータベースにある場合
            name = db.execute_database("SELECT name FROM student WHERE id = '" + data["id"] + "'")[0][0] # idに対応する名前を取得
            print(
                "[Error] 生徒の追加に失敗しました。このカードはすでに登録されています。このカードを別の生徒に割り当てるには，まずこのカードを所有する生徒の除名を行ってください。カードの所有者: ", name
            )
            return -1
    
    # データベースのフィールドの順番にdataを並び変える
    student_data = get_dict_from_database("student")
    parent_data = get_dict_from_database("parent")

    fdata = []
    for i in fields_student:
        fdata.append(data[i])
    # 引数の文字列を成形
    fields_attr = ", ".join(fields_student)  # フィールドをカンマ区切りにする
    data_attr = "', '".join(fdata)  # データをカンマ区切りにする

    if (
        db.execute_database(
            "INSERT INTO student (" + fields_attr + ") VALUES ('" + data_attr + "')"
        )
        == -1
    ):
        print("[Error] add_student_to_database: Couldn't add data to student table.")
        return -1
    
    fdata_parent = []
    for i in fields_parent:
        fdata_parent.append(data[i])
        
    fields_attr = ", ".join(fields_parent)  # フィールドをカンマ区切りにする
    data_attr = "', '".join(fdata)  # データをカンマ区切りにする
    
    print(fields_attr)
    print(data_attr)
    
    if (
        db.execute_database(
            "INSERT INTO parent (" + fields_attr + ") VALUES ('%s', '%s', '%s')" % (data["id"], data["parent_name"], data["mail_address"])
        , debug=True)
        == -1
    ):
        print("[Error] add_student_to_database: Couldn't add data to parent table.")
        return -1

    add_systemlog_to_database("生徒の追加: " + data["name"])  # システムログに記録
    db.commit_database()  # データベースにコミットする
    print("[Register] " + data["name"] + " が登録されました。")


def add_systemlog_to_database(data: str):  # システムログをデータベースに追加
    """
    システムログをデータベースに追加する。

    引数: ログに記録する文字列
    戻り値: なし
    """
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


def enter_room(id: str):  # 入室処理
    """
    生徒の入室処理を行う

    引数: 生徒のID
    戻り値: なし
    """
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


def exit_room(id: str):  # 退室処理
    """
    生徒の退出処理を行う。

    引数: 生徒のID
    戻り値: なし
    """
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


if __name__ == "__main__":
    add_student_to_database({"name": "test", "age": "a", "gender": "b", "parent_name": "id001", "parent_address": "id001", "id": "id001"})

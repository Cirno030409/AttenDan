import csv
import sqlite3


class Database:
    def __init__(self):
        self.dbname = "RoboDone_AttendanceSystem_Database.db"

    def connect_to_database(self):  # データベースを読み出す
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()
        print("[Database] connected.")

    def execute_database(self, sql):  # データベースにコマンドを実行し，実行結果をかえす
        print("[Database] Executing command. -->", sql)
        try:
            self.cur.execute(sql)
        except sqlite3.OperationalError as e:
            print("[Error] SQL command execution failed. :", e)
            return -1
        fetch = self.cur.fetchall()  # 実行結果を取得
        for i in range(len(fetch)):
            fetch[i] = list(fetch[i])  # fetchをリストに変換
        return fetch

    def commit_database(self):
        self.conn.commit()
        print("[Database] commited.")

    def rollback_database(self):
        self.conn.rollback()
        print("[Database] rollbacked.")

    def disconnect_from_database(self):
        self.cur.close()
        self.conn.close()
        print("[Database] disconnected.")

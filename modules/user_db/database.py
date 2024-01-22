import os
import sqlite3
current_pyfile_path = os.path.abspath(__file__)
USER_DB_PATH = os.path.join(os.path.dirname(current_pyfile_path),"any_userdb.db")
class DB:
    def __init__(self,ob_path) -> None:
        self.name = "user.db"
        self.ob_path = ob_path
        self.db_path = f"{self.ob_path}modules\\user_db\\{self.name}"
        
    def create_database(self):
        conn = sqlite3.connect(self.db_path)
        # 创建一个Cursor:
        cursor = conn.cursor()
        # 执行一条SQL语句，创建user表:
        cursor.execute('create table user (username varchar(20) primary key, password varchar(20), consumption float,recharge float)')
        # 关闭Cursor:
        cursor.close()
        # 提交事务:
        conn.commit()
        # 关闭Connection:
        conn.close()
    def check_credentials(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM user WHERE username='{username}' AND password='{password}'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return True
        else:
            return False
    def get_user_info(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT consumption, recharge FROM user WHERE username='{username}'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result
        else:
            return None
    def deduct_balance(self, username, amount):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 先获取用户当前的消费额度和充值额度
        cursor.execute(f"SELECT consumption, recharge FROM user WHERE username='{username}'")
        result = cursor.fetchone()
        if result:
            current_consumption, current_recharge = result
            # 计算新的消费额度
            new_consumption = current_consumption + amount
            # 如果新的消费额度大于充值额度，将消费额度设置为充值额度，并返回False
            if new_consumption > current_recharge:
                new_consumption = current_recharge
                success = False
            else:
                success = True
            # 更新数据库
            cursor.execute(f"UPDATE user SET consumption={new_consumption} WHERE username='{username}'")
            # 提交事务
            conn.commit()
        else:
            success = False
        cursor.close()
        conn.close()
        return success
    def insert_users(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for i in range(1, 28):  # 生成1到27的序列
            username = f"ai{i:02}"  # 格式化用户名，保证是两位数
            password = "123456"
            consumption = 0.0
            recharge = 10.0
            # 检查用户名是否存在
            cursor.execute(f"SELECT * FROM user WHERE username='{username}'")
            result = cursor.fetchone()
            # 如果用户名不存在，插入数据
            if not result:
                cursor.execute(f"INSERT INTO user (username, password, consumption, recharge) VALUES ('{username}', '{password}', {consumption}, {recharge})")
        cursor.close()
        conn.commit()  # 提交事务
        conn.close()

def get_deduction_amount(txt,model_name,mode):
    if mode == "input":
        deduction_tables = {
            "GPT3.5 Turbo":0.036,
            "GPT3.5 Turbo 16K":0.02,
            # "GPT4",
            # "GPT4 32K",
            # "GPT4 Turbo",
            # "GPT4 Vision",
            # "川虎助理",
            # "DALL-E 3",
            # "midjourney",
            # "讯飞星火大模型V3.0",
            # "讯飞星火大模型V2.0",
            # "讯飞星火大模型V1.5",
            # "chatglm-6b",
            # "chatglm-6b-int4",
            # "chatglm-6b-int4-ge",
            # "chatglm2-6b",
            # "chatglm2-6b-int4",
            # "chatglm3-6b",
            # "chatglm3-6b-32k",

        }
    if mode == "output":
        deduction_tables = {
        "GPT3.5 Turbo":0.036,
        "GPT3.5 Turbo 16K":0.02,
        # "GPT4",
        # "GPT4 32K",
        # "GPT4 Turbo",
        # "GPT4 Vision",
        # "川虎助理",
        # "DALL-E 3",
        # "midjourney",
        # "讯飞星火大模型V3.0",
        # "讯飞星火大模型V2.0",
        # "讯飞星火大模型V1.5",
        # "chatglm-6b",
        # "chatglm-6b-int4",
        # "chatglm-6b-int4-ge",
        # "chatglm2-6b",
        # "chatglm2-6b-int4",
        # "chatglm3-6b",
        # "chatglm3-6b-32k",
        }
    return len(txt)/500 *deduction_tables.get(model_name,0.3)

class User_Db:
    def __init__(self) -> None:
        self.db_path = USER_DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
    def create_database(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            consumption REAL,
            recharge REAL,
            reset_times INTEGER,
            use_costs REAL,
            limit_costs REAL,
            last_reset_time TEXT,
            enable_models TEXT,
            admin_name TEXT
        );
        """
        self.cur.execute(create_table_query)
        self.conn.commit()
    def insert_users(self,data_to_insert):
        insert_data_query = """
        INSERT INTO users (username, password, consumption, recharge, reset_times, use_costs, limit_costs, last_reset_time, enable_models, admin_name)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cur.executemany(insert_data_query, data_to_insert)
        self.conn.commit()
    def update_last_reset_time(self,data):
        all ='''
            UPDATE users
            SET
                # username = ?,
                # password = ?,
                # consumption = ?,
                # recharge = ?,
                # reset_times = ?,
                use_costs = ?,
                # limit_costs = ?,
                last_reset_time = ?,

            WHERE username = ?
            """
        '''
        update_data_query = """
            UPDATE users
            SET
                use_costs = ?,
                last_reset_time = ?
            WHERE username = ?
        """
        self.cur.executemany(update_data_query, data)
        self.conn.commit()
    def check_credentials(self, username, password):
        self.cur.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False
    def deduct_balance(self,username,amount):
        self.cur.execute(f"SELECT consumption, recharge,use_costs,limit_costs FROM users WHERE username='{username}'")
        result = self.cur.fetchone()
        if result:
            current_consumption, current_recharge,use_costs,limit_costs = result
            # 计算新的消费额度
            new_consumption = current_consumption + amount
            # 如果新的消费额度大于充值额度，将消费额度设置为充值额度，并返回False
            if new_consumption > current_recharge:
                new_consumption = current_recharge
                result = False
            else:
                result = True
            if use_costs is None:
                use_costs = 0
            new_use_costs = use_costs + amount
            if new_use_costs > limit_costs:
                new_use_costs = limit_costs
                result = False
            else:
                result = True
            # 更新数据库
            self.cur.execute(f"UPDATE users SET consumption={new_consumption},use_costs={new_use_costs} WHERE username='{username}'")
            # 提交事务
            self.conn.commit()
        else:
            result = False
        
    def get_user_info(self, username):

        self.cur.execute(f"SELECT consumption, recharge,reset_times,use_costs,limit_costs,last_reset_time,enable_models FROM users WHERE username='{username}'")
        result = self.cur.fetchone()

        if result:
            return result
        else:
            return None
    def __del__(self):
        self.conn.close()



if __name__ == "__main__":
    # db = DB()
    # db.create_database()
    udb = User_Db()
    udb.create_database()
    users_0 = [
        ['root', 'dlm00_416416', 5, 350, None, None, None, None, 'all', None],
        ['ai01', '123456', 2, 5, 60,0, 0.01, 1705289852, 'GPT3.5 Turbo 16K,', 'root'],
        ['erro', '123456', 2, 5, 60, 0, 0.01, 1705289852, 'all', 'root'],
    ]
    udb.insert_users(users_0)

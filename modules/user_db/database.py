import sqlite3
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

if __name__ == "__main__":
    db = DB()
    db.create_database()


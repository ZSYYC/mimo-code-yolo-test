import pymysql
from pymysql import OperationalError
import time

class DatabaseClient:
    def __init__(self, config, max_retries=3, retry_delay=2):
        self.config = config
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """建立数据库连接"""
        for attempt in range(self.max_retries):
            try:
                self.connection = pymysql.connect(**self.config)
                self.cursor = self.connection.cursor()
                print("✅ 成功连接数据库")
                break
            except OperationalError as e:
                print(f"❌ 数据库连接失败，第 {attempt + 1} 次尝试：{e}")
                time.sleep(self.retry_delay)
        else:
            raise ConnectionError("数据库连接失败超过最大重试次数")

    def query_by_name(self, img_name):
        """根据图片名模糊查询设备名、图片名"""
        try:
            sql = """
            SELECT device_name, photo_name, photo_time FROM ser_traplight_photo WHERE photo_path LIKE %s
            UNION ALL
            SELECT device_name, photo_name, photo_time FROM ser_traplight_xct_photo WHERE photo_path LIKE %s
            """
            params = ('%' + img_name + '%',) * 2  # 三个 %s 对应三个参数
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            if results:
                print(f"📦 查询到 {len(results)} 条结果：")
            return results
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return []

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔌 数据库连接已关闭")
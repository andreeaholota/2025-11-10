from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.*
            FROM stores s 
            ORDER BY s.store_name
        """

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllOrder(store_id):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ 
            SELECT o.*
            FROM orders o
            WHERE o.store_id = %s
        """

        cursor.execute(query, (store_id,))
        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOrdersByDate(store_id, K):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ 
            SELECT v1.orderId AS v1, v2.orderId AS v2, (v1.quantity + v2.quantity)/DATEDIFF(v1.orderDate, v2.orderDate) AS weight
            FROM ( SELECT o.order_id AS orderId, o.order_date AS orderDate, SUM(oi.quantity) AS quantity
                 FROM orders o, order_items oi
                 WHERE o.store_id = %s
                 AND o.order_id = oi.order_id
                 GROUP BY o.order_id, o.order_date) v1, 
                ( SELECT o.order_id AS orderId, o.order_date AS orderDate, SUM(oi.quantity) AS quantity
                 FROM orders o, order_items oi
                 WHERE o.store_id = %s
                 AND o.order_id = oi.order_id
                 GROUP BY o.order_id, o.order_date) v2
            WHERE DATEDIFF(v1.orderDate, v2.orderDate) BETWEEN 1 AND %s
        """

        cursor.execute(query, (store_id, store_id, K, ))
        for row in cursor:
            results.append((row["v1"], row["v2"], row["weight"]))

        cursor.close()
        conn.close()
        return results
from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories(idMapCategories):

        conn = DBConnect.get_connection()


        cursor = conn.cursor(dictionary=True)
        query = """select distinct category_id, category_name  
                    from categories c """

        cursor.execute(query)

        for row in cursor:

            idMapCategories[row["category_id"]] = row["category_name"]



        cursor.close()
        conn.close()
        return idMapCategories

    @staticmethod
    def getRightProducts(category):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from products p
                    where category_id = %s"""

        cursor.execute(query, (category,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getWeightedEdges(category, start, end):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select oi.product_id, count(*) as peso
                    from order_items oi , orders o , products p 
                    where oi.order_id = o.order_id 
                    and p.product_id = oi.product_id 
                    and p.category_id = %s
                    and date(o.order_date) between %s and %s
                    group by product_id"""

        cursor.execute(query, (category, start, end,))

        for row in cursor:
            results.append((row["product_id"], row["peso"]))

        cursor.close()
        conn.close()
        return results

from db_connection import get_db_connection

def fetch_menu(category=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT mi.item_id, mi.item_name, c.category_name,
               m.menu_name, mi.size, mi.price
        FROM menu_items mi
        JOIN category c ON mi.cat_id = c.cat_id
        JOIN menu m ON mi.menu_id = m.menu_id
        WHERE 1=1
    """
    params = []

    if category:
        query += " AND c.category_name = %s"
        params.append(category)

    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

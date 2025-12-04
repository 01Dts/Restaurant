from JWTBased.db_connection import get_db_connection


def fetch_orders(order_status=None, start_date=None, end_date=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT DISTINCT o.order_id, o.order_date, o.order_status
        FROM orders o WHERE 1=1
    """

    params = []

    if order_status:
        query += " AND o.order_status = %s"
        params.append(order_status)

    if start_date:
        query += " AND o.order_date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND o.order_date <= %s"
        params.append(end_date)

    cursor.execute(query, params)
    orders = cursor.fetchall()

    final_output = []

    for order in orders:
        oid = order["order_id"]

        # Fetch items
        cursor.execute("""
            SELECT o.id, o.item_id, mi.item_name, c.category_name,
                   o.size, o.price, o.qty, o.total
            FROM orders o
            JOIN menu_items mi ON o.item_id = mi.item_id
            JOIN category c ON mi.cat_id = c.cat_id
            WHERE o.order_id = %s
            ORDER BY o.id
        """, (oid,))
        items = cursor.fetchall()

        # Fetch payments
        cursor.execute("""
            SELECT payment_id, payment_date, amount_due, tips, discount,
                   total_paid, payment_type, payment_status
            FROM payments WHERE order_id = %s ORDER BY payment_id
        """, (oid,))
        payments = cursor.fetchall()

        order_total = sum(float(i["total"]) for i in items)
        amount_due = sum(float(p["amount_due"]) for p in payments) if payments else 0
        total_paid = sum(float(p["total_paid"]) for p in payments) if payments else 0

        final_output.append({
            "order_id": oid,
            "order_date": order["order_date"].strftime("%Y-%m-%d"),
            "order_status": order["order_status"],
            "items": items,
            "payments": payments,
            "order_total": round(order_total, 2),
            "amount_due": amount_due,
            "total_paid": total_paid,
            "balance": round(amount_due - total_paid, 2)
        })

    conn.close()
    return final_output

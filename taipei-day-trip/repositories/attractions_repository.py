def fetch_attractions_by_page(db, page: int, keyword: str = None):
    OFFSET = 12*(page)
    sql_query = """
    SELECT attractions.id, attractions.name, attractions.category, attractions.description, attractions.address, attractions.transport, attractions.mrt, attractions.lat, attractions.lng,
    JSON_ARRAYAGG(img_urls.url) AS images
    FROM attractions
    INNER JOIN img_urls ON attractions.id = img_urls.attraction_id

    """
    conditions = []
    params = []
    if keyword:
        conditions.append(
            "WHERE attractions.mrt = %s OR attractions.name LIKE %s")
        params.extend([keyword, f"%{keyword}%"])
    if conditions:
        sql_query += " AND ".join(conditions)
    sql_query += " GROUP BY attractions.id LIMIT 13 OFFSET %s"
    params.extend([OFFSET])

    db.execute(sql_query, tuple(params))
    attraction_data = db.fetchall()
    return attraction_data


def fetch_attraction_by_id(db, attraction_id):
    sql_query = """
        SELECT attractions.id, attractions.name, attractions.category, attractions.description, attractions.address, attractions.transport, attractions.mrt, attractions.lat, attractions.lng,
        JSON_ARRAYAGG(img_urls.url) AS images
        FROM attractions
        INNER JOIN img_urls ON attractions.id = img_urls.attraction_id
        WHERE attractions.id = %s
        GROUP BY attractions.id
        """
    db.execute(sql_query, (attraction_id,))
    attraction = db.fetchone()
    return attraction


def get_attraction_info(db, id):
    db.execute(" SELECT a.id, name, address, url AS image FROM attractions a JOIN img_urls i ON a.id = i.attraction_id WHERE a.id = %s LIMIT 1;", (
               id,))
    attraction = db.fetchone()
    return attraction

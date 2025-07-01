def fetch_mrt_stations(db):
    db.execute(
        "SELECT mrt, COUNT(mrt) AS count FROM attractions WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY count DESC")
    mrts = db.fetchall()
    return mrts

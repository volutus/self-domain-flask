from pysrc import db
import base64

def fetch_reviews():

    sql = '''
    select no.name, no.barcode, no.image_uri, no.image_data, no.container_type,
    nm.name as maker, nr.review_date, nr.score, nr.price, nr.review 
    from noodle_review nr
    join noodles no on nr.noodle_id = no.id 
    join noodle_maker nm on no.maker_id = nm.id 
    order by score desc, price;
    '''

    with db.fetch_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql)
        columns = [column[0] for column in cur.description]
        reviews = []
        for row in cur.fetchall():
            reviews.append(dict(zip(columns, row)))
        
        # Probably don't need this now
        for r in reviews:
            if r["image_data"] is not None:
                r["image_b64"] = base64.b64encode(r["image_data"]).decode("utf-8")

    return reviews
    
    

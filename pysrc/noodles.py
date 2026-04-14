from pysrc import db

def fetch_reviews():

    sql = '''
    select no.name, no.barcode, no.image_uri, no.container_type,
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

    return reviews
    
    

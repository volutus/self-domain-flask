import os
import psycopg2

def fetch_dict():
    # init DB (pull me into a utility if this comes up often)
    # db_host = os.environ['DB_HOST']
    db_host = 'self-domain-docker-db-1'
    db_user = os.environ['DB_USERNAME']
    db_pass = os.environ['DB_PASSWORD']
    conn = psycopg2.connect(host=db_host, database="postgres", user=db_user, password=db_pass)

    sql = '''
    select no.name, nm.name as maker, nr.review_date, nr.score, nr.review 
    from noodle_review nr
    join noodles no on nr.noodle_id = no.id 
    join noodle_maker nm on no.maker_id = nm.id;
    '''
    
    cur = conn.cursor()
    cur.execute(sql)
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    
    return reviews
    
    

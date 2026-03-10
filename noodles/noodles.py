import os
import psycopg2

def fetch_dict(hex_string):
    # init DB (pull me into a utility if this comes up often)
    conn = psycopg2.connect(host="localhost", database="postgres",
                            user=os.environ['DB_USERNAME'], pass=os.environ['DB_PASSWORD'])
    
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
    
    

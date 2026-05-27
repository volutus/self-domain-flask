import pysrc.db as db
import requests
from PIL import Image
import io
import base64

class DashboardLink(object):
    def __init__(self, row):
        self.table = row['table_name']
        self.title = row['title']
        self.link = row['link']
        self.svg = row['svg']
        self.count = row['record_count']

    @staticmethod
    def fetch_all():
        dashboard_links = list()
        sql = """
        select np.*, pg.n_live_tup as record_count from nms_page np 
        join pg_stat_user_tables pg on np.table_name = pg.relname 
        order by np.rank;
        """
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            for row in cur.fetchall():
                dashboard_links.append(DashboardLink(row))
        return dashboard_links

class NoodleMaker(object):
    def __init__(self, row):
        self.id = row.get('id')
        self.name = row['name']
    
    @staticmethod
    def fetch_all():
        records = list()
        sql = "select * from noodle_maker"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            for row in cur.fetchall():
                records.append(NoodleMaker(row))
        return records
    
    @staticmethod
    def fetch_id(id):
        maker = None
        sql = "SELECT * from noodle_maker where id = %s"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            params = (id,)
            cur.execute(sql, params)

            row = cur.fetchone()
            if row is not None and len(row) > 0:
                maker = NoodleMaker(row)
        return maker
    
    @staticmethod
    def to_select_options(makers):
        options = list()        # pretty sure this could be a list comprehension
        for maker in makers:
            options.append(SelectOption(maker.id, maker.name))
        return options
    
    def uri(self):
        return f"/nms/edit-noodle-maker?id={self.id}"
    
    def edit(self, mode):
        match mode:
            case 'update':
                return self.update()
            case 'create':
                return self.create()
            case 'delete':
                return self.delete()
        return f"No update integrated for {mode}"
            
    
    def update(self):
        sql = "UPDATE noodle_maker SET name=%s where id=%s"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            params = (self.name, self.id)
            cur.execute(sql, params)
        return f"Update completed for maker #{self.id}" 
    def create(self):
        sql = "INSERT INTO noodle_maker (name) values (%s) RETURNING id"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            params = (self.name,)
            cur.execute(sql, params)
            row = cur.fetchone()
            self.id = row['id']
        return f"Created new maker with ID #{self.id}" 
    def delete(self):
        sql = "DELETE FROM noodle_maker WHERE id=%s"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            params = (self.id,)
            cur.execute(sql, params)
        return f"Processed delete for maker #{self.id}" 

class NoodleReview(object):
    def __init__(self, row):
        self.id = row.get('id')
        self.name = row['name']
        self.maker_id = row['maker_id']
        self.barcode = row['barcode']
        self.container_type = row['container_type']
        self.image_uri = row['image_uri']
        self.image_data = row.get('image_data')
        self.review_date = row['review_date']
        self.score = row['score']
        self.price = row['price']
        self.review = row['review']
        
    @staticmethod
    def fetch_all():
        sql = """
        select no.*, nr.review_date, nr.score, nr.price, nr.review
        from noodle_review nr
        join noodles no on nr.noodle_id = no.id 
        order by nr.review_date desc;
        """
        records = list()
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            for row in cur.fetchall():
                records.append(NoodleReview(row))
        return records
    
    @staticmethod
    def fetch_id(id):
        obj = None
        sql = """
        select no.*, nr.review_date, nr.score, nr.price, nr.review
        from noodle_review nr
        join noodles no on nr.noodle_id = no.id 
        where no.id = %s
        """
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            params = (id,)
            cur.execute(sql, params)

            row = cur.fetchone()
            if row is not None and len(row) > 0:
                obj = NoodleReview(row)
        return obj
        
    
    def uri(self):
        return f"/nms/edit-noodle-review?id={self.id}"
    
    def edit(self, mode):
        match mode:
            case 'update':
                return self.update()
            case 'create':
                return self.create()
            case 'delete':
                return self.delete()
        return f"No update integrated for {mode}"
            
    
    def update(self):
        self.rip_image()
        update_noodle = "UPDATE noodles SET name=%s, maker_id=%s, barcode=%s, container_type=%s, image_uri=%s, image_data=%s where id=%s"
        update_review = "UPDATE noodle_review SET review_date=%s, score=%s, price=%s, review=%s WHERE noodle_id=%s"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            
            noodle_params = (self.name, self.maker_id, self.barcode, self.container_type, self.image_uri, self.image_data, self.id)
            cur.execute(update_noodle, noodle_params)
            
            review_params = (self.review_date, self.score, self.price, self.review, self.id)
            cur.execute(update_review, review_params)
            
        return f"Update completed for noodle #{self.id} and associated review." 
    
    def create(self):
        self.rip_image()
        noodle = "INSERT INTO noodles (name, maker_id, barcode, container_type, image_uri, image_data) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
        review = "INSERT INTO noodle_review (review_date, score, price, review, noodle_id) VALUES (%s, %s, %s, %s, %s)"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            
            noodle_params = (self.name, self.maker_id, self.barcode, self.container_type, self.image_uri, self.image_data)
            cur.execute(noodle, noodle_params)
            
            row = cur.fetchone()
            self.id = row['id']
            
            review_params = (self.review_date, self.score, self.price, self.review, self.id)
            cur.execute(review, review_params)
            
        return f"Create completed for noodle #{self.id} and associated review." 
    
    def delete(self):
        review = "DELETE FROM noodle_review WHERE noodle_id = %s"
        noodle = "DELETE FROM noodles WHERE id = %s"
        with db.fetch_connection() as conn:
            cur = conn.cursor()
            
            # we need to delete the review first or it'll throw a SQL error due to the existing foreign key
            param = (self.id,)
            cur.execute(review, param)      
            cur.execute(noodle, param)
            
        return f"Delete processed for noodle #{self.id} and associated review." 
    
    def rip_image(self):
        if self.image_uri is None or self.image_uri.startswith("/"):
            return

        response = requests.get(self.image_uri)  
        original = Image.open(io.BytesIO(response.content))
        original.thumbnail((400, 400))
        
        filename = f"/static/noodles/{self.id}.avif" 
        original.save(filename, format='AVIF')     
        self.image_uri = filename
        
        # Also save the data into the DB so we can replicate from nothing if needed
        new_image = io.BytesIO()
        original.save(new_image, format='AVIF')     
        self.image_data = new_image.getvalue()


        

class SelectOption(object):
    def __init__(self, value, text):
        self.value = value
        self.text = text
    
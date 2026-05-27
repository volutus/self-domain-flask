from pysrc import db

def fetch_all():

    sql = '''
    select * from sauce order by id;
    '''
    
    records = list()
    with db.fetch_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            records.append(Sauce(row))


    content = dict()
    content["records"] = records
    
    fields = list()
    if len(records) > 0:
        record = records[0]
        fields = list(vars(record).keys())
    [f.replace("_", " ").title() for f in fields]       #  Replace underscore with spaces and title case
    content["fields"] = fields

    return content
    
    
class Sauce(object):
    def __init__(self, row):
        self.id = row.get('id')
        self.name = row['name']
        self.saucier = row['saucier']
        self.owner = row['owner']
        self.in_stock = row['in_stock']
        self.heat_index = row['heat_index']
        self.linger_index = row['linger_index']
        self.flavor_index = row['flavor_index']
        self.scoville = row['scoville']
        self.heat_notes = row['heat_notes']
        self.flavor_notes = row['flavor_notes']
        self.description = row['description']

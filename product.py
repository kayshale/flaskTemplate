import pymysql
from baseObject import baseObject

class productList(baseObject):

    def __init__(self):
        self.data = [] # where the dataset is stored as a list of dictionaries
        self.tempdata = {}
        self.tn = 'ortizk_product'
        self.fnl = ['sku','name','price'] #fnl = field name list
        self.conn = None
        self.errorList = []
        self.pk = 'pid'

    def setupObject(self,tn):
        self.data = []
        self.tempdata = {}
        self.tn = 'ortizk_product'
        self.fnl = ['sku','name','price']
        self.pk = 'pid'
        self.conn = None
        self.errorList = []
        self.getFields()

    def connect(self):
        import config
        self.conn = pymysql.connect(host=config.DB['host'], port=config.DB['port'], user=config.DB['user'], passwd=config.DB['passwd'], db=config.DB['db'], autocommit=True)

    def getFields(self):
        sql = 'DESCRIBE `' + self.tn + '`;'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.fnl = []
        for row in cur:
            self.fnl.append(row['Field'])
            if row['Extra'] == 'auto_increment' and row['Key'] == 'PRI':
                self.pk = row['Field']
        #print(self.fnl)

    def add(self):
        self.data.append(self.tempdata)

    def set(self,fn,val):
        if fn in self.fnl:
            self.tempdata[fn] = val
        else:
            print('Invalid field: ' + str(fn))

    def update(self,n,fn,val):
        if len(self.data) >= (n + 1) and fn in self.fnl:
            self.data[n][fn] = val
        else:
            print('could not set value at row ' + str(n) + ' col ' + str(fn) )

    def insert(self,n=0):
        cols = ''
        vals = ''
        tokens = []
        for fieldname in self.fnl:
            if fieldname in self.data[n].keys():
                tokens.append(self.data[n][fieldname])
                vals += '%s,'
                cols += '`'+fieldname+'`,'
        vals = vals[:-1]
        cols = cols[:-1]
        sql = 'INSERT INTO `' + self.tn +'` (' +cols + ') VALUES (' + vals+');'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tokens)
        cur.execute(sql,tokens)
        self.data[n][self.pk] = cur.lastrowid

    def delete(self,n=0):
        item = self.data.pop(n)
        self.deleteById(item[self.pk])

    def verifyNew(self,n=0):
        if len(self.data[n]['sku']) == 0:
            self.errorList.append("Product sku cannot be blank.")
        #Add if statements for validation of other fields
        if len(self.data[n]['name']) == 0:
            self.errorList.append("Product name cannot be blank.")

        if self.data[n]['price'] < 0:
            self.errorList.append("Product price must be greater than zero.")

        elif len(cost.rsplit('.')[-1]) != 2:
           print('Too many digits after')

        if len(self.errorList) > 0:
            return False
        else:
            return True

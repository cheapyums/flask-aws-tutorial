# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

# ACC NOTE:  I had to create the database in mysql first
# mysql -h cydb.csyohiqdr8hj.us-west-1.rds.amazonaws.com -P 3306 -u admin -p

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:cydbadmin@cydb.csyohiqdr8hj.us-west-1.rds.amazonaws.com:3306/cydb'

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'dsaf0897sfdg45sfdgfdsaqzdf98sdf0a'

#SQLALCHEMY_ENGINE_OPTIONS = {"isolation_level":'READ_COMMITTED'}

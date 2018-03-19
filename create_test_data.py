import sqlite3
from sqlite3 import Error
from PIL import Image

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_blog_post_top(conn, sqlStatements):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    cur = conn.cursor()
    for sql in sqlStatements:
        if isinstance(sql, tuple):
            try:
                cur.execute("INSERT INTO blog_profile (profile_image, zip, latitude, longitude, is_storm_spotter, user_id_id) VALUES(?,?,?,?,?,?)", sql)
            except:
                pass

            try:
                cur.execute("INSERT INTO blog_image (image, blog_post_id_id) VALUES(?,?)", sql)
            except:
                pass
        else:
            cur.execute(sql)
    conn.commit()
    return cur.lastrowid

###################
### Sql Inserts ###
###################

longString1 = ''' 'Check out this total crazy torando I saw while driving around in my Jetta.  mauris neque quam, fermentum ut nisl vitae, convallis maximus nisl. Sed mattis nunc id lorem euismod placerat. Vivamus porttitor magna enim, ac accumsan tortor cursus at. Phasellus sed ultricies mi non congue ullam corper. Praesent tincidunt sedtellus ut rutrum. Sed vitae justo condimentum, porta lectus vitae, ultricies congue gravida diam non fringilla.' '''
longString2 = ''' 'Heavy flooding in the marina trench area.  ac accumsan tortor cursus at.  Watch for large carpe bass swimming upstream Phasellus sed ultricies mi non congue ullam corpe mauris neque quam, fermentum ut nisl vitae, convallis maximus nisl. Sed mattis nunc id lorem euismod placerat. Vivamus porttitor magna enim, r. Praesent tincidunt sedtellus ut rutrum. Sed vitae justo condimentum, porta lectus vitae, ultricies congue gravida diam non fringilla.' '''
longString3 = ''' 'Thunderstorms have been happening all the time in Oklahoma, here is a perfect example near Routersville At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil.' '''
commentString1 = ''' 'Wow crazy tornado - great pics!' '''
commentString2 = ''' 'What camera are you using - any lens tips?' '''
commentString3 = ''' 'Looks wet out there' '''
commentString4 = ''' 'Wow cool photo - this is in NE?' '''
commentString5 = ''' 'GREAT JOB!' '''

### Encode images for insertion
images = []

imagePaths = ['testData/instructor.jpg',
              'testData/tornado1.jpg',
              'testData/tornado2.jpg',
              'testData/tornado3.jpg',
              'testData/flood1.jpg',
              'testData/flood2.jpg',
              'testData/thunderstorm1.jpg',
              'testData/thunderstorm2.jpg',
              'testData/thunderstorm3.jpg',
              'testData/thunderstorm4.jpg',
              ]

for path in imagePaths:
    imgobj = Image.open(path)
    # Only shrink profile images
    if 'instructor' in path:
        imgobj.thumbnail((120, 120))
    # Shrink blog post images to another size? Something else???
    else:
        imgobj.thumbnail((480, 640))
    imgobj = imgobj.tobytes()
    images.append(imgobj)

sqlStatements = []
### Creating Blog Posts
sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + longString1 + ''', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);
''')

sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + longString2 + ''', CURRENT_TIMESTAMP, NULL, 1);
''')

sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + longString3 + ''', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);
''')

sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + commentString1 + ''', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);
''')

sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + commentString2 + ''', CURRENT_TIMESTAMP, NULL, 1);
''')

sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + commentString3 + ''', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);
''')

sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + commentString4 + ''', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);
''')

sqlStatements.append('''
INSERT INTO blog_blog_post 
(author, text, created_date, published_date, user_id_id)
VALUES ('Username', ''' + commentString5 + ''', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);
''')

# Creating Top Posts
sqlStatements.append('''
INSERT INTO blog_top_post
(blog_post_ptr_id, title)
VALUES (1, 'Tornado');
''')

sqlStatements.append('''
INSERT INTO blog_top_post
(blog_post_ptr_id, title)
VALUES (2, 'Flood');
''')

sqlStatements.append('''
INSERT INTO blog_top_post
(blog_post_ptr_id, title)
VALUES (3, 'Thunderstorm');
''')

# Creating response posts
sqlStatements.append('''
INSERT INTO blog_response_post
(blog_post_ptr_id, top_post_id_id)
VALUES (4, 1);
''')

sqlStatements.append('''
INSERT INTO blog_response_post
(blog_post_ptr_id, top_post_id_id)
VALUES (5, 1);
''')

sqlStatements.append('''
INSERT INTO blog_response_post
(blog_post_ptr_id, top_post_id_id)
VALUES (6, 2);
''')

sqlStatements.append('''
INSERT INTO blog_response_post
(blog_post_ptr_id, top_post_id_id)
VALUES (7, 3);
''')

sqlStatements.append('''
INSERT INTO blog_response_post
(blog_post_ptr_id, top_post_id_id)
VALUES (8, 3);
''')

# Create a profile for instructor
sqlStatements.append((images[0], 68114, 41.2565, 95.9345, True, 1))

# Create tags for test blogs
sqlStatements.append('''
INSERT INTO blog_tags
(tag, blog_post_id_id)
VALUES ('Tornado', 1);
''')

sqlStatements.append('''
INSERT INTO blog_tags
(tag, blog_post_id_id)
VALUES ('Twister', 1);
''')

sqlStatements.append('''
INSERT INTO blog_tags
(tag, blog_post_id_id)
VALUES ('Storm', 1);
''')

sqlStatements.append('''
INSERT INTO blog_tags
(tag, blog_post_id_id)
VALUES ('Flood', 2);
''')

sqlStatements.append('''
INSERT INTO blog_tags
(tag, blog_post_id_id)
VALUES ('Wet', 2);
''')

sqlStatements.append('''
INSERT INTO blog_tags
(tag, blog_post_id_id)
VALUES ('Water', 2);
''')

# Add images to blogs
# Tornado photos
sqlStatements.append((images[1], 1))
sqlStatements.append((images[2], 1))
sqlStatements.append((images[3], 1))
# Flood photos
sqlStatements.append((images[4], 2))
sqlStatements.append((images[5], 2))
# Thunderstorm photos
sqlStatements.append((images[6], 3))
sqlStatements.append((images[7], 3))
sqlStatements.append((images[8], 3))
sqlStatements.append((images[9], 3))

# Create alerts
sqlStatements.append('''
INSERT INTO blog_alerts
(alert_name)
VALUES ('Tornado Nebraska');
''')

sqlStatements.append('''
INSERT INTO blog_alerts
(alert_name)
VALUES ('Tornado Kansas');
''')

sqlStatements.append('''
INSERT INTO blog_alerts
(alert_name)
VALUES ('Tornado Oklahoma');
''')

sqlStatements.append('''
INSERT INTO blog_alerts
(alert_name)
VALUES ('Tornado North and South Dakota');
''')

sqlStatements.append('''
INSERT INTO blog_alerts
(alert_name)
VALUES ('Earthquake Nationwide');
''')

sqlStatements.append('''
INSERT INTO blog_alerts
(alert_name)
VALUES ('Heavyrain West Coast');
''')

sqlStatements.append('''
INSERT INTO blog_user_alerts
(alert_id_id, user_id_id)
VALUES (1, 1);
''')

sqlStatements.append('''
INSERT INTO blog_user_alerts
(alert_id_id, user_id_id)
VALUES (5, 1);
''')

##############
### Run It ###
##############
DB = 'db.sqlite3'

conn = create_connection(DB)
print(create_blog_post_top(conn, sqlStatements))

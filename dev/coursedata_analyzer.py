import psycopg2

__author__ = 'ng3br'

PG_USER = "postgres"
PG_USER_PASS = "admin"
PG_HOST_INFO = ""

def instructor_numbers(dept_id):
    dict = {}
    conn = psycopg2.connect("dbname=course1 user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    print("** Connected to database.")

    cur = conn.cursor()
    query = "SELECT * from coursedata WHERE deptid = '%s'"%(dept_id)
    cur.execute(query)
    list = cur.fetchall()
    for course in list:
        instructor = course[6]
        enrollment = int(course[5])
        if instructor not in dict:
            dict[instructor] = enrollment
        else:
            dict[instructor] += enrollment

    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    print("** Closed connection and database.  Bye!.")

    print(dict)
    return dict

if __name__ == '__main__':
    instructor_numbers('APMA')
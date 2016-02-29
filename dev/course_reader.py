import csv
import psycopg2

__author__ = 'ng3br'

PG_USER = "postgres"
PG_USER_PASS = "admin"
PG_HOST_INFO = ""

def load_course_database(db_name, csv_filename):
    conn = psycopg2.connect("dbname=" + db_name + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    print("** Connected to database.")

    cur = conn.cursor()
    with open(csv_filename, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            query = "INSERT INTO coursedata (deptid, coursenum, semester, meetingtype, seatstaken, seatsoffered, instructor)" \
                                           " VALUES (%s, %s, %s, %s, %s, %s, %s)"
            print(query)
            cur.execute(query, tuple(row))


        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()
        print("** Closed connection and database.  Bye!.")


def read_course_database(db_name):
    conn = psycopg2.connect("dbname=" + db_name + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    print("** Connected to database.")


    cur = conn.cursor()
    query = "SELECT * from coursedata WHERE deptid='APMA'"
    cur.execute(query)
    print(cur.fetchall())

    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    print("** Closed connection and database.  Bye!.")

#load_course_database('course1', 'seas-courses-5years.csv')
read_course_database('course1')
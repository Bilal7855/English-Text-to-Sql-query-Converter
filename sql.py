import sqlite3


def create_student_table():
    connection = sqlite3.connect("STUDENT.db")
    cursor = connection.cursor()

    # Create table only if it doesn't exist
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS STUDENT (
            NAME VARCHAR(25) PRIMARY KEY,
            CLASS VARCHAR(25),
            SECTION VARCHAR(25),
            MARKS INT
        );''')
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        return False

    # Insert sample data
    cursor.execute('''INSERT INTO STUDENT VALUES('BILAL','DATA SCIENCE','A',90)''')
    cursor.execute('''INSERT INTO STUDENT VALUES('noman','Ai engineer','b',100)''')
    cursor.execute('''INSERT INTO STUDENT VALUES('jamshaid','react develper','b',80)''')
    cursor.execute('''INSERT INTO STUDENT VALUES('salman','freelancer','A',90)''')
    cursor.execute('''INSERT INTO STUDENT VALUES('waqas','front end develper','c',90)''')

    connection.commit()
    connection.close()

    print("Sample student data inserted successfully!")


if __name__ == "__main__":
    create_student_table()

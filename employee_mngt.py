# employee_mngt.py

import psycopg2
from psycopg2 import sql


def connect():
    conn = psycopg2.connect(dbname = "employee_mngt",user = "postgres",password = "makeover22",host = "localhost")
    return conn

def create_dept(name, location):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO departments (name, location) VALUES (%S, %s) RETURNING department_id;",(name, location))
    department_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return department_id
	
def create_employee(name, email, phone, hire_date, department_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (name, email, phone, hire_date, department_id) VALUES (%s, %s, %s, %s, %s) RETURNING employee_id;", (name, email, phone, hire_date, department_id))
    employee_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return employee_id

def read_employees():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def update_employee(employee_id, name=None, email=None, phone=None, hire_date=None, department_id=None):
    conn = connect()
    cur = conn.cursor()
    query = "UPDATE employees SET "
    params = []
    if name:
        query += "name = %s, "
        params.append(name)
    if email:
        query += "email = %s, "
        params.append(email)
    if phone:
        query += "phone = %s, "
        params.append(phone)
    if hire_date:
        query += "hire_date = %s, "
        params.append(hire_date)
    if department_id:
        query += "department_id = %s, "
        params.append(department_id)
    query = query.rstrip(", ")
    query += " WHERE employee_id = %s RETURNING employee_id;"
    params.append(employee_id)
    cur.execute(query, params)
    updated_employee_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return updated_employee_id

def delete_employee(employee_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id = %s RETURNING employee_id;", (employee_id,))
    deleted_employee_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return deleted_employee_id

if __name__ == "__main__":
    # Example usage
    dept_id = create_department("Engineering", "New York")
    print(f"Created department with ID: {dept_id}")

    emp_id = create_employee("John Doe", "john.doe@example.com", "555-555-5555", "2023-06-01", dept_id)
    print(f"Created employee with ID: {emp_id}")

    print("Employees before update:")
    read_employees()

    updated_emp_id = update_employee(emp_id, name="John D.", phone="555-555-5556")
    print(f"Updated employee with ID: {updated_emp_id}")

    print("Employees after update:")
    read_employees()

    deleted_emp_id = delete_employee(emp_id)
    print(f"Deleted employee with ID: {deleted_emp_id}")

    print("Employees after delete:")
    read_employees()

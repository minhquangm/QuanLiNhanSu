from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Kết nối đến database
def connect_db():
    return sqlite3.connect("employees.db")

# Khởi tạo database
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Trang danh sách nhân sự
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees ORDER BY id DESC")
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

# Thêm/Sửa nhân sự
@app.route('/add_edit', methods=['GET', 'POST'])
def add_edit():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        salary = request.form['salary']
        status = request.form['status']

        conn = connect_db()
        cursor = conn.cursor()

        if employee_id:  # Cập nhật nhân sự
            cursor.execute("""
                UPDATE employees SET name=?, position=?, department=?, salary=?, status=? WHERE id=?
            """, (name, position, department, salary, status, employee_id))
        else:  # Thêm nhân sự mới
            cursor.execute("""
                INSERT INTO employees (name, position, department, salary, status)
                VALUES (?, ?, ?, ?, ?)
            """, (name, position, department, salary, status))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    employee_id = request.args.get('id')
    employee = None
    if employee_id:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
        employee = cursor.fetchone()
        conn.close()
    
    return render_template('add_edit.html', employee=employee)

# Xóa nhân sự
@app.route('/delete/<int:employee_id>')
def delete(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Tìm kiếm nhân sự
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE name LIKE ? OR position LIKE ? OR department LIKE ?", 
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    init_db()  # Tạo database nếu chưa có
    app.run(debug=True)

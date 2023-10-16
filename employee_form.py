import http.server
import socketserver
import MySQLdb as mysql
import os
import cgi

# Database connection parameters
customhost = "db-1.cjtjjruls9d6.us-east-2.rds.amazonaws.com"
customuser = "richa"
custompass = "richa462"
customdb = "db-1"

# Create a database connection
db = mysql.connect(
    host=customhost,
    user=customuser,
    passwd=custompass,
    db=customdb
)

# Function to handle form submission
def process_employee_form(data, img_data):
    cursor = db.cursor()
    insert_query = "INSERT INTO employee (empid, fname, lname, pri_skill, location, image) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (data['employee_id'], data['first_name'], data['last_name'], data['primary_skill'], data['location'], img_data))
    db.commit()
    cursor.close()

class EmployeeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("employee_form.html", "r") as file:
                self.wfile.write(file.read().encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("404 Not Found".encode())

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        data = {}
        img_data = None

        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                img_data = field_item.file.read()
            else:
                data[field] = field_item.value

        process_employee_form(data, img_data)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("Employee data has been successfully updated!".encode())

if __name__ == '__main__':
    PORT = 8000
    handler = EmployeeHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

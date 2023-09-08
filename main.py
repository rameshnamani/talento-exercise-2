from flask import Flask, request, jsonify, Response
from xml.etree.ElementTree import Element, ElementTree, tostring
from operator import itemgetter

app = Flask(__name__)

# Sample employee data
employees = [
    {'name': 'Joe', 'last_name': 'Smith', 'age': 25},
    {'name': 'Allen', 'last_name': 'Jones', 'age': 21},
    {'name': 'Sam', 'last_name': 'Andrews', 'age': 35}
]

# Endpoint to add an entry to the list
@app.route('/add', methods=['POST'])
def add_employee():
    new_employee = request.get_json()
    print(type(new_employee))
    if new_employee:
        employees.extend(new_employee)
        return jsonify({'message': 'Employee added successfully!'}), 201
    else:
        return jsonify({'error': 'Invalid employee data.'}), 400

# Endpoint to return the list in JSON format
@app.route('/json', methods=['GET'])
def get_employees_json():
    sorted_employees = sorted(employees, key=itemgetter('age'))
    return jsonify(sorted_employees)

# Endpoint to return the list in XML format
@app.route('/xml', methods=['GET'])
def get_employees_xml():
    sorted_employees = sorted(employees, key=itemgetter('age'))
    xml_root = Element('employees')
    for employee in sorted_employees:
        employee_elem = Element('employee')
        for key, value in employee.items():
            sub_elem = Element(key)
            sub_elem.text = str(value)
            employee_elem.append(sub_elem)
        xml_root.append(employee_elem)
    xml_string = tostring(xml_root).decode()
    return Response(xml_string, content_type='application/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
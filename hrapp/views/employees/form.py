import sqlite3
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models.department import Department
from hrapp.models import model_factory
from ..connection import Connection
from hrapp.views.employees.employee_details import get_employee

def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.department_name
        from hrapp_department d
        """)

        return db_cursor.fetchall()

@login_required
def employee_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'employees/form.html'
        context = {
            'all_departments': departments
        }

        return render(request, template, context)

@login_required
def employee_edit_form(request, employee_id):

    if request.method == 'GET':
        employee = get_employee(employee_id)
        departments = get_departments()

        template = 'employees/form.html'
        context = {
            'employee': employee,
            'all_departments': departments
        }

        return render(request, template, context)
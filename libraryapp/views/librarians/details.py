import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from libraryapp.models import Librarian
from libraryapp.models import model_factory
from ..connection import Connection


def get_librarian(librarian_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Librarian)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select l.id, 
            l.location_id, 
            l.user_id, 
            u.id, 
            u.email, 
            u.first_name, 
            u.last_name,
            u.username
        from libraryapp_librarian l
        join auth_user u on u.id = l.user_id
        where l.id = ?;
        """, (librarian_id,))

        return db_cursor.fetchone()

@login_required
def librarian_details(request, librarian_id):
    if request.method == 'GET':
        librarian = get_librarian(librarian_id)

        template = 'librarians/details.html'
        context = {
            'librarian': librarian
        }

        return render(request, template, context)
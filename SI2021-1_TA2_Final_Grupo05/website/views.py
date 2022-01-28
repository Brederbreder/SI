from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 101:
            flash('Seu resumo deve ter pelo menos 100 caracteres.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Resumo adicionado.', category='success')

    return render_template("home.html", user=current_user)

@views.route('/general', methods=['GET'])
def general():
    all_notes = Note.query.order_by(Note.id.desc()).all()
    all_user = User.query.order_by(User.id).all()

    return render_template("general.html", user=current_user, value=all_notes, users=all_user)

@views.route('/account', methods=['GET'])
def account():
    return render_template("account.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            flash('Resumo excluído.', category='neutral')
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
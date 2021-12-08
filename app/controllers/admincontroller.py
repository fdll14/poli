import os
from flask import (Flask, render_template, url_for, request, abort, redirect, make_response, session, flash, abort, jsonify)
from app import app
from uuid import uuid4
from werkzeug.utils import secure_filename
from app.models.user import User
from app.models.testimoni import Testimoni


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def make_unique(string):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{string}"

# ADMIN
@app.route('/admin', methods = ['GET'])
def admin():
    if not session.get('id'):
        return redirect(url_for('login'))
    else:
        return render_template('admin/index.html')

# TESTIMONI
@app.route('/admin/testimoni/<idx>', methods = ['GET', 'POST'])
def admin_testimoni(idx='all'):
    if request.method == "POST":
        file = request.files['foto']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = make_unique(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        testimoni = Testimoni()
        inputan = request.form
        testimoni.store(inputan['nama'],inputan['lulusan'], inputan['pesan'], filename)
        flash('Berhasil tambah data')
        return redirect(url_for('admin_testimoni', idx='all'))
    elif request.method == "GET" :
        if idx == 'all':
            testimoni = Testimoni()
            data = {
                'testimoni':testimoni.get()
            }
            return render_template('admin/testimoni.html', data=data)
        else:
            testimoni = Testimoni()
            data = testimoni.getOne(idx)
            return jsonify(result=data)
            
@app.route('/admin/testimoni/delete/<idx>', methods = ['GET'])
def admin_testimoni_delete(idx=None):
    testimoni = Testimoni()
    filename = testimoni.getCurrentFile(idx)
    os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename[0]))
    data = testimoni.destroy(idx)
    flash('Berhasil hapus data')
    return redirect(url_for('admin_testimoni', idx='all'))
@app.route('/admin/testimoni/update', methods = ['POST'])
def admin_testimoni_update():
    testimoni = Testimoni()
    inputan = request.form
    
    if not request.files['foto'] :
        filename = 'sama'
    else :
        file = request.files['foto']
        res = testimoni.getCurrentFile(inputan['id'])
        filename = res[0]
        os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = make_unique(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        else :
            return redirect(url_for('admin_testimoni', idx='all'))

    testimoni.update(inputan['id'], inputan['nama'], inputan['lulusan'], inputan['pesan'], filename)
    flash('Berhasil update data')
    return redirect(url_for('admin_testimoni', idx='all'))

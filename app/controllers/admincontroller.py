import os
from flask import (Flask, render_template, url_for, request, abort, redirect, make_response, session, flash, abort, jsonify)
from app import app
from uuid import uuid4
from werkzeug.utils import secure_filename
from app.models.user import User
from app.models.testimoni import Testimoni
from app.models.answererror import Answererror
from app.models.dataset import Dataset


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


#answer error
@app.route('/admin/answer-error/<idx>', methods = ['GET', 'POST'])
def answer_error(idx='all'):
    if request.method == "POST":
        answererror = Answererror()
        inputan = request.form
        answererror.store(inputan['pertanyaan'], inputan['status'])
        flash('Berhasil tambah data')
        return redirect(url_for('answer_error', idx='all'))
    elif request.method == "GET" :
        if idx == 'all':
            answererror = Answererror()
            data = answererror.get()
            return render_template('admin/answer_error.html', data=data)
        else:
            answererror = Answererror()
            data = answererror.getOne(idx)
            return jsonify(result=data)
            
@app.route('/admin/answer-error/delete/<idx>', methods = ['GET'])
def answer_error_delete(idx=None):
    answererror = Answererror()
    data = answererror.destroy(idx)
    flash('Berhasil hapus data')
    return redirect(url_for('answer_error', idx='all'))
@app.route('/admin/answer-error/update', methods = ['POST'])
def answer_error_update():
    answererror = Answererror()
    inputan = request.form
    answererror.update(inputan['id'], inputan['pertanyaan'], inputan['status'])
    flash('Berhasil update data')
    return redirect(url_for('answer_error', idx='all'))

#dataset
@app.route('/admin/dataset/<idx>', methods = ['GET', 'POST'])
def dataset(idx='all'):
    if request.method == "POST":
        dataset = Dataset()
        inputan = request.form
        dataset.store(inputan['pertanyaan'], inputan['jawaban'])
        flash('Berhasil tambah data')
        return redirect(url_for('dataset', idx='all'))
    elif request.method == "GET" :
        if idx == 'all':
            dataset = Dataset()
            data = dataset.get()
            return render_template('admin/dataset.html', data=data)
        else:
            dataset = Dataset()
            data = dataset.getOne(idx)
            return jsonify(result=data)
            
@app.route('/admin/dataset/delete/<idx>', methods = ['GET'])
def dataset_delete(idx=None):
    dataset = Dataset()
    data = dataset.destroy(idx)
    flash('Berhasil hapus data')
    return redirect(url_for('dataset', idx='all'))
@app.route('/admin/answer-error/update', methods = ['POST'])
def dataset_update():
    dataset = Dataset()
    inputan = request.form
    dataset.update(inputan['id'], inputan['pertanyaan'], inputan['jawaban'])
    flash('Berhasil update data')
    return redirect(url_for('dataset', idx='all'))

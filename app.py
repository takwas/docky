import os

from flask import Flask, request, render_template, jsonify, redirect, url_for


path = os.path
current_dir = path.abspath(os.curdir)

config = {
    'SECRET_KEY': 'some_secret_key',
    'SQLALCHEMY_DATABASE_URI':
        'sqlite:///{path_to_file}/docs.sqlite'.format(path_to_file=current_dir),

    # https://stackoverflow.com/a/33790196
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}

app = Flask(__name__)
app.config.update(config)

from models import db, Doc, History, User, ACTIVE_STATUS, DISABLED_STATUS
db.init_app(app)


@app.before_request
def before_every_request():
    pass


@app.after_request
def after_every_request(response):
    return response


@app.route('/')
def index():
    docs = Doc.query.filter_by(status=ACTIVE_STATUS).all()
    return render_template('index.html', doc_list=docs)


@app.route('/docs/<doc_uid>', methods=['GET'])
def view_doc(doc_uid):
    doc = Doc.query.filter_by(uid=doc_uid,
                              status=ACTIVE_STATUS).first()

    if doc is None:
        return 'Not found', 404

    doc_content = doc.content or ''
    return render_template('editing.html',
                           old_content=doc_content,
                           doc_uid=doc_uid)


@app.route('/docs', methods=['POST'])
def create_new_doc():
    # doc = Doc(content=request_data[''])
    doc = Doc()
    db.session.add(doc)
    db.session.commit()

    response_data = {
        'success': True,
        'message': 'Doc created',
        'docUID': doc.uid
    }
    return jsonify(response_data), 201


@app.route('/docs/<doc_uid>', methods=['POST'])
def update_doc(doc_uid):
    request_data = request.json

    doc = Doc.query.filter_by(uid=doc_uid,
                              status=ACTIVE_STATUS).first()

    if doc is None:
        return 'Not found', 404

    doc.content = request_data['content']
    db.session.commit()

    response_data = {
        'success': True,
        'message': 'Content updated',
        'content': doc.content or ''
    }
    return jsonify(response_data), 200


@app.route('/docs/deletions/<doc_uid>', methods=['GET'])
def remove_doc(doc_uid):
    doc = Doc.query.filter_by(uid=doc_uid,
                              status=ACTIVE_STATUS).first()

    if doc is None:
        return 'Not found', 404

    doc.status = DISABLED_STATUS
    db.session.commit()

    print 'Deleted!'

    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

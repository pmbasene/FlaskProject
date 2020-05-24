

from flask import Blueprint

summers = Blueprint('summers', __name__)



# for integrating text editor
@summers.route('/summernote', methods=['POST', 'GET'])
def summernote():
    if request.method == 'POST':
        editor = Editor(html=request.form.get('editordata'))
        # print(request.form.get('editordata'))
        db.session.add(editor)
        db.session.commit()
        # return 'Posted Data'
        return redirect(url_for('display'))
    return render_template('docEssai/summernote.html')


@summers.route('/display')   # linked to summernote route , able to display post
def display():
    posts = Editor.query.all()
    print(posts)
    # return 'data received'
    return render_template('docEssai/display.html', posts=posts)


# @summers.route('/display/<int:id>')
# def display(id):
#     posts = Editor.query.get(id)
#     print(posts)
#     # return 'data received'
#     return render_template('docEssai/display.html', posts=posts)

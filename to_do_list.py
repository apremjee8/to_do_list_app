from flask import (Flask, render_template, g,
                   redirect, request, url_for, flash)

import forms
import models

app = Flask(__name__)
app.secret_key = 'asdflkasdlgjlasjdgladgnlawnlkfwen'

final_ws = 'Oscar'


######### INDIVIDUAL FUNCTIONS #########

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

def set_workspace(path):
    global final_ws 
    final_ws = path
    return final_ws


######### VIEWING ROUTES #########

@app.route('/', methods=['GET', 'POST'])
def index(entry_id=None):
    global final_ws
    workspace = final_ws
    name = workspace

    view_entries = models.Entry.select().where(models.Entry.state =='inbox', models.Entry.workspace == workspace)
    ws = models.Workspace.select()
    form = forms.EntryForm(request.form)

    if form.validate_on_submit():
        flash('Entry added!', 'success')
        models.Entry.create(
            entry=form.entry.data, workspace=workspace
        )
        return redirect(url_for('index'))
    return render_template('view_entries.html', view_entries=view_entries, ws=ws, workspace=workspace, name=name, form=form)


@app.route('/<workspace>', methods=['GET', 'POST'])
def inbox(workspace):
    view_entries = models.Entry.select().where(models.Entry.state =='inbox', models.Entry.workspace == workspace)
    ws = models.Workspace.select()
    form = forms.EntryForm(request.form)
    path = workspace
    name = path

    set_workspace(path) #take the workspace portion of URL and make it a global variable

    if form.validate_on_submit():
        flash('Entry added!', 'success')
        models.Entry.create(
            entry=form.entry.data, workspace=name
        )
        return redirect(url_for('index'))
    return render_template('view_entries.html', view_entries=view_entries, ws=ws, name=name, workspace=workspace, form=form)

@app.route('/completed_entries', methods=['GET', 'POST'])
def completed_entries():
    global final_ws
    workspace = final_ws
    
    view_entries = models.Entry.select().where(models.Entry.state =='done', models.Entry.workspace == workspace)
    ws = models.Workspace.select()
    form = forms.EntryForm()

    if form.validate_on_submit():
        flash('Entry added!', 'success')
        models.Entry.create(
            entry=form.entry.data, workspace=workspace
        )
        return redirect(url_for('index'))
    return render_template('completed_entries.html', view_entries=view_entries, ws=ws, workspace=workspace, form=form)

@app.route('/today', methods=['GET', 'POST'])
def today():
    global final_ws
    workspace = final_ws

    view_entries = models.Entry.select().where(models.Entry.state =='today', models.Entry.workspace == workspace)
    ws = models.Workspace.select()
    form = forms.EntryForm()

    if form.validate_on_submit():
        flash('Entry added!', 'success')
        models.Entry.create(
            entry=form.entry.data, workspace=workspace
        )
        return redirect(url_for('index', workspace=workspace))
    return render_template('today.html', view_entries=view_entries, ws=ws, workspace=workspace, form=form)


@app.route('/waiting', methods=['GET', 'POST'])
def waiting():
    global final_ws
    workspace = final_ws
    
    view_entries = models.Entry.select().where(models.Entry.state =='waiting', models.Entry.workspace == workspace)
    ws = models.Workspace.select()
    form = forms.EntryForm()

    if form.validate_on_submit():
        flash('Entry added!', 'success')
        models.Entry.create(
            entry=form.entry.data, workspace=workspace
        )
        return redirect(url_for('index'))
    return render_template('waiting.html', view_entries=view_entries, ws=ws, workspace=workspace, form=form)    


######### CREATION / ENTRY MOVEMENT #########

@app.route('/create_workspace', methods=['GET', 'POST'])
def create_workspace():
    ws = models.Workspace.select()
    wform = forms.WorkspaceForm()
    if wform.validate_on_submit():
        flash('Workspace created!', 'success')
        models.Workspace.create(
            workspace=wform.workspace.data
        )
        return redirect(url_for('index'))
    return render_template('create_workspace.html', ws=ws, wform=wform)


@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    global final_ws
    workspace = final_ws

    ws = models.Workspace.select()
    form = forms.EntryForm()
    if form.validate_on_submit():
        flash('Entry added!', 'success')
        models.Entry.create(entry=form.entry.data, workspace=workspace)
        return redirect(url_for('index'))
    return render_template('add_entry.html', ws=ws, workspace=workspace, form=form)


@app.route('/update_entry/<int:entry_id>', methods=['GET', 'POST'])
def update_entry(entry_id):
    update_entry = models.Entry.select().where(models.Entry.id == entry_id)
    ws = models.Workspace.select()
    form = forms.UpdateForm()
    if form.validate_on_submit():
        flash('Entry updated!', 'success')
        q = models.Entry.update(entry=form.entry.data).where(models.Entry.id == entry_id)
        q.execute()
        return redirect(url_for('index'))
    return render_template('update_entry.html', update_entry=update_entry, ws=ws, form=form)


@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    delete_entry = models.Entry.select().where(models.Entry.id == entry_id).first()
    delete_entry.delete_instance()
    return redirect(redirect_url())


@app.route('/done_entry/<int:entry_id>', methods=['POST'])
def done_entry(entry_id):
    q = models.Entry.update(state='done').where(models.Entry.id == entry_id)
    q.execute()
    return redirect(redirect_url())


@app.route('/today_entry/<int:entry_id>', methods=['POST'])
def today_entry(entry_id):
    q = models.Entry.update(state='today').where(models.Entry.id == entry_id)
    q.execute()
    return redirect(redirect_url())


@app.route('/waiting_entry/<int:entry_id>', methods=['POST'])
def waiting_entry(entry_id):
    q = models.Entry.update(state='waiting').where(models.Entry.id == entry_id)
    q.execute()
    return redirect(redirect_url())

@app.route('/inbox_entry/<int:entry_id>', methods=['POST'])
def inbox_entry(entry_id):
    q = models.Entry.update(state='inbox').where(models.Entry.id == entry_id)
    q.execute()
    return redirect(redirect_url())


######### APP FUNCTIONS #########

@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = models.db
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after the request"""
    g.db.close()
    return response


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
    if models.Workspace.select():
        pass
    else:
        models.Workspace.create(workspace='Personal')
        models.Workspace.create(workspace='Oscar')

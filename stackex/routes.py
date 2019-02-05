from flask import render_template, redirect, url_for, request, flash
from stackex import app, db
from stackex.models import User_request, Request_result
from stackex.forms import NewRequestForm
from stackex.funcs import stack_request

def req(url):
    request = requests.get(url)
    return request.content


@app.route('/')
def home():
    results = User_request.query.all()
    return render_template('home.html', results=results)


@app.route('/new_request', methods=['GET', 'POST'])
def stack_ex():
    form = NewRequestForm()
    if form.validate_on_submit():
        stack_request(form.search.data)
        return redirect(url_for('search_results', req=form.search.data))
    return render_template('new_request.html', title="New Request", form=form)


@app.route('/search_results/<req>')
def search_results(req):
    r = req
    page = request.args.get('page', 1, type=int)
    #new_results = results_2
    find_request = User_request.query.filter_by(req_name=r).first().id
    new_results = Request_result.query.filter_by(request_id=find_request).\
        paginate(page=page, per_page=10)
    # new_results = new_results[:25]
    return render_template('search_results.html',
                           results=new_results, request=r)

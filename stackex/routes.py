from flask import render_template, redirect, url_for, request
from stackex import app
from stackex.models import User_request, Request_result
from stackex.forms import NewRequestForm
from stackex.funcs import stack_request


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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    find_request = User_request.query.filter_by(req_name=req).first()
    if find_request:
        find_request = find_request.id
    else:
        return render_template(
            'search_results.html', results=[], request=req
        )

    new_results = Request_result.query.filter_by(request_id=find_request)\
        .order_by(Request_result.last_activity_date.desc())\
        .paginate(page=page, per_page=per_page)
    return render_template('search_results.html',
                           results=new_results, request=req)


@app.route('/delete_item/<id>')
def delete(id):
    User_request.find_by_id(id).delete()
    return redirect(url_for('home'))


@app.route('/update/<id>')
def update(id):
    request = User_request.find_by_id(id).req_name
    fromdate = User_request.find_by_id(id).date
    stack_request(req=request, fromdate=fromdate)
    return redirect(url_for('home'))

from flask import render_template, redirect, url_for, request, flash
from stackex import app, db
from stackex.models import User_request, Request_result
from stackex.forms import NewRequestForm
from stackex.funcs import stack_request

results = [
    {
        "date": "12.10.2005",
        "name": "python",
        "description": "Here we talking about python"
    },
    {
        "date": "27.02.2012",
        "name": "javascript",
        "description": "Isn't it the best?"
    },
    {
        "date": "13.07.2010",
        "name": "best language",
        "description": "Of course you know the answer to that question"
    }
]

results_2 = [
    {
        "last_activity_date": "13.03.17",
        "title": "What is the best IDE",
        "link": "www.dummy.com/1"
    },
    {
        "last_activity_date": "25.06.14",
        "title": "Python vs Java",
        "link": "www.dummy.com/2"
    },
    {
        "last_activity_date": "01.08.07",
        "title": "Latest javascript framework",
        "link": "www.dummy.com/3"
    },
]


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


@app.route('/search_results')
def search_results():
    r = request.args.get("req")
    #new_results = results_2
    find_request = User_request.query.filter_by(req_name=r).first().id
    new_results = Request_result.query.filter_by(request_id=find_request)
    new_results = new_results[:25]
    return render_template('search_results.html',
                           results=new_results, request=r)

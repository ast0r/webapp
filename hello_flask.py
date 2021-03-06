import vowels2
from flask import Flask, render_template, request, session

from DBcm import UseDatabase

from checker import check_logged_in
app = Flask(__name__)


app.secret_key = '!@#$%^&*()QWERTYUIOP{'


app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': '2222',
                          'database': 'vsearchlogdb'}


def log_request(req: 'flask_request', res: str) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
                    (phrase,letters,ip,browser_string,results)
                    values
                    (%s, %s, %s, %s, %s)"""

        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(vowels2.search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Entry page')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """SELECT ts, phrase, letters, ip, browser_string, results FROM log;"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Time', 'Phrase', 'Letters', 'Remoute_addr', 'User_agent', 'Resualt')

    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_title=titles,
                           the_data=contents, )


@app.route('/login')
def do_login() -> 'str':
    session['logged_in'] = 'True'
    return 'You are now logged in: ' + session['logged_in']


@app.route('/logout')
def do_logout() -> 'html':
    session.pop('logged_in')
    return render_template('error_login.html',
                           the_title='You are now logged out')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, escape
import vowels2, mysql.connector

app = Flask(__name__)

def log_request(req: 'flask_request', res: str) -> None:
    dbconfig = {'host': '127.0.0.1',
                'user': 'vsearch',
                'password': '2222',
                'database': 'vsearchlogdb'}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """INSERT INTO log 
            (phrase,letters,ip,browser_string,results)
            VALUES 
            (%s, %s, %s, %s, %s);"""
    cursor.execute(_SQL,(req.form['phrase'],
                         req.form['letters'],
                         req.remote_addr,
                         req.user_agent.browser,
                         res,))
    conn.commit()
    cursor.close()
    conn.close()

    #with open('vsearch.log','a') as log:
     #   print(req.form, req.remote_addr,req.user_agent,res, file = log, sep='|')

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(vowels2.search4letters(phrase,letters))
    log_request(request,results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html' ,
                           the_title='Welcom to search4 on the web')

@app.route('/viewlog')
def view_the_log() -> 'html':
    content = []
    with open('vsearch.log') as log:
        for line in log:
            content.append([])
            for item in line.split('|'):
                content[-1].append(escape(item))
    titles = ('Form Data','Remoute_addr','User_agent','Resualt')
    return render_template('viewlog.html' ,
                           the_title='View Log',
                           the_row_title = titles,
                           the_data = content,)

if __name__ == '__main__':
    app.run(debug = True)
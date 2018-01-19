from flask import Flask, render_template, request
import vowels2

app = Flask(__name__)

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(vowels2.search4letters(phrase,letters))
    log_request(request,results, phrase)
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
     with open('vsearch.log') as log:
         contents = log.read()
     return render_template('viewlog.html' ,
                            the_log_msg=contents)

def log_request(req: 'flask_request',phr , res: str) -> None:
    with open('vsearch.log','a') as log:
        print(req, res, phr, file = log)

if __name__ == '__main__':
    app.run(debug = True)
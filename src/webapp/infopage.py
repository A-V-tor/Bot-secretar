from flask import (
    current_app as app,
    render_template,
)


@app.route('/infopage', methods=['GET'])
def index_main():
    return render_template('infopage.html')

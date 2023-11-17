from flask import Flask, render_template, request, url_for, jsonify

import psycopg2
import keyring

app = Flask(__name__, static_url_path= '/static')

# Configure database connection details
db_host = "127.0.0.1"
db_name = "school_portal"
db_user = "postgres"
db_password = keyring.get_password('school_portal', 'postgres')

# Define the route for the homepage
@app.route('/')
def homepage():

    return render_template('index.html')


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():

    if request.method == 'POST':

        title= request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        disposition = request.form['disposition']
        image_data = request.files['image_data'].read()

        # Connect to the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        # Insert form data into the database
        cur.execute(
            "INSERT INTO staff (title, first_name, last_name, disposition, image_data) VALUES (%s, %s, %s, %s, %s)",
            (title, first_name, last_name, disposition, psycopg2.Binary(image_data))
        )

        # Commit the database insertions
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        return 'User created successfully!'

    return render_template('staff_portal.html')

if __name__ == '__main__':
    app.run(debug=True)

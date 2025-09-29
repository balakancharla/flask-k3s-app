from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Simple in-memory user (for demo purposes)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# HTML Template (you can replace with a file later)
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial; background: #f2f2f2; text-align: center; padding-top: 50px; }
        form { background: white; padding: 20px; display: inline-block; border-radius: 5px; }
        input { margin: 5px; padding: 10px; width: 200px; }
        button { padding: 10px 20px; }
    </style>
</head>
<body>
    <h2>Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required /><br>
        <input type="password" name="password" placeholder="Password" required /><br>
        <button type="submit">Login</button>
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

welcome_page = """
<h1>Welcome, {{ username }}!</h1>
<p>You have successfully logged in.</p>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return render_template_string(welcome_page, username=username)
        else:
            error = "Invalid credentials"
    return render_template_string(login_page, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


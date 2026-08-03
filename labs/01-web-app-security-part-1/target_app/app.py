from flask import Flask, request, render_template_string

app = Flask(__name__)

# Deliberately insecure login form.
# Flaws are intentional — this is the scanner's target.
login_template = """
<!doctype html>
<html>
  <head><title>Login</title></head>
  <body>
    <h2>Login</h2>
    <form method="POST" action="/login">
      <input type="text" name="username" placeholder="Username" required /><br/>
      <input type="password" name="password" placeholder="Password" required /><br/>
      <!-- FLAW: no CSRF token -->
      <input type="submit" value="Login" />
    </form>
  </body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(login_template)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # FLAW: no rate limiting, no lockout, no attempt logging
        return "Login attempt received (not secure)", 200
    return render_template_string(login_template)


if __name__ == "__main__":
    # FLAW: plain HTTP — credentials travel in cleartext
    app.run(port=5000)
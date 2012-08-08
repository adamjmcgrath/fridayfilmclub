<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Friday Film Club{% endblock %}</title>
    <link rel="stylesheet/less" href="/stylesheets/main.less">
    <script src="/less/dist/less-1.3.0.min.js"></script>
  </head>
  <body id="{% block page_id %}{% endblock %}">
    <div class="navbar">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="i-bar"></span>
            <span class="i-bar"></span>
            <span class="i-bar"></span>
          </a>
          <a class="brand" href="#">{% block logo %}Friday Film Club{% endblock %}</a>
          <div id="sign-in">
            <img src="//lh4.googleusercontent.com/-l6LPIjkmjwA/AAAAAAAAAAI/AAAAAAAAAAA/ZAxpZ-lfnUw/s27-c/photo.jpg" height="30">
            <a class="btn btn-primary" href="#">Log In</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="row">
        {% block main %}{% endblock %}
        {% block sidebar %}{% endblock %}
      </div>
      <hr>
      <div id="footer">
        <p>&copy; Company 2012</p>
      </div>
    </div>
    {% block body_base %}{% endblock %}
  </body>
</html>

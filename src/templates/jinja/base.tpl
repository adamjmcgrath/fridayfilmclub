<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Friday Film Club{% endblock %}</title>
    {% include "templates/jinja/inc/css.tpl" %}
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
          <a class="brand cookie" href="#">{% block logo %}Friday Film Club{% endblock %}</a>
          <div id="sign-in">
            {% if logged_in %}
              <span>
                <b>{{user.name}}</b><br>
                <a href="/profile">profile</a> - <a href="/logout">logout</a>
              </span>
              <img src="{{user.avatar_url}}" width="30" height="30">
            {% endif %}
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

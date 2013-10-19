<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Friday Film Club{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% include "templates/jinja/inc/css.tpl" %}
  </head>
  <body id="{% block page_id %}{% endblock %}">
    <div class="navbar" id="title-bar">
        <div class="container">
          <a class="navbar-brand custom-font" href="{{ uri_for('home') }}">{% block logo %}Friday Film Club{% endblock %}</a>
          <div id="sign-in">
            {% if logged_in %}
              <span>
                <b>{{user.name}}</b><br>
                <a href="{{ uri_for('settings') }}">settings</a> - <a href="{{ uri_for('logout') }}">logout</a>
              </span>
              <img src="{{user.avatar_url}}" width="30" height="30">
            {% else %}
              <a href="{{ uri_for('login') }}" class="btn btn-primary">Login</a>
            {% endif %}
          </div>
        </div>
    </div>

    <div class="navbar navbar-default" id="nav">
      <ul class="nav navbar-nav">
        <li{% if page_id == 'how-page' %} class="active"{% endif %}><a href="/how">How to play</a></li>
        <li{% if page_id == 'archive-page' %} class="active"{% endif %}><a href="/archive">Old questions</a></li>
        <li{% if page_id == 'leaderboard-page' %} class="active"{% endif %}><a href="/leaderboard">Leaderboard</a></li>
      </ul>
    </div>

    <div class="container">
      {% block content %}
        <div class="row">
          {% block main %}{% endblock %}
          {% block sidebar %}{% endblock %}
        </div>
      {% endblock %}
      <hr>
      <div id="footer">
        <p>&copy; Friday Film Club</p>
      </div>
    </div>
    {% block body_base %}{% endblock %}
  </body>
</html>

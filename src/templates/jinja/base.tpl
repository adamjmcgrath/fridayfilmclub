<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Friday Film Club{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% include "templates/jinja/inc/css.tpl" %}
  </head>
  <body id="{% block page_id %}{% endblock %}">
    {% block nav_bar %}

      <div class="social-bar">
        <div class="facebook"><a href="https://www.facebook.com/fridayfilmclub" target="_blank" rel="noopener">Facebook</a></div>
        <div class="twitter"><a href="https://twitter.com/FilmMasterJack" target="_blank" rel="noopener">Twitter</a></div>
        <div class="email"><a href="mailto:fmj@fridayfilmclub.com">fmj@fridayfilmclub.com</a></div>
      </div>

      <div class="navbar" id="title-bar">
        <div class="container">
          <a class="navbar-brand custom-font-header" href="{{ uri_for('home') }}">
            Friday Film Club
          </a>
          <ul class="nav navbar-nav">
              <li{% if page_id == 'how-page' %} class="active"{% endif %}>
                <a href="{{ uri_for('how-it-works') }}">How to play</a>
              </li>
              <li{% if page_id == 'archive-page' %} class="active"{% endif %}>
                <a href="{{ uri_for('archive') }}">Archive</a>
              </li>
              <li{% if page_id == 'leaderboard-page' %} class="active"{% endif %}>
                <a href="{{ uri_for('leader-board') }}">Leaderboard</a>
              </li>
              {% if logged_in %}
              <li class="dropdown">
                <a href="#" id="leagues-dropdown" class="dropdown-toggle" data-toggle="dropdown">
                  Leagues <span class="caret"></span>
                </a>
                <ul class="dropdown-menu" id="leagues-dropdown-menu" role="menu">
                  {% for league in user.get_leagues() %}
                  <li>
                    <a href="{{ uri_for('league', league_id=league.name_slug) }}">
                      <span class="glyphicon glyphicon-list-alt"></span> {{ league.name }}
                    </a>
                  </li>
                  {% else %}
                  <li role="presentation" class="dropdown-header">You have no leagues</li>
                  {% endfor %}
                  <li class="divider"></li>
                  <li>
                    <a href="{{ uri_for('add-league') }}">
                      <span class="glyphicon glyphicon-plus"></span>
                      Create a league
                    </a>
                  </li>
                </ul>
              </li>
              <li id="user-link">
                <a href="{{ uri_for('settings') }}"><img src="{{user.pic_url()}}" width="30" height="30" class="user-pic"> {{user.name}}</a>
              </li>
              {% else %}
              <li>
                <a href="{{ uri_for('login') }}" class="btn btn-primary">Login</a>
              </li>
              {% endif %}
            </ul>
        </div>
      </div>

    {% endblock %}

    <div class="container">
      {% block content %}
        <div class="row">
          {% block main %}{% endblock %}
          {% block sidebar %}{% endblock %}
        </div>
      {% endblock %}
    </div>
      {% block footer %}
        <div id="footer">
          <p>&copy; Friday Film Club</p>
        </div>
      {% endblock %}
    {% block body_base %}{% endblock %}
    <script>
      (function() {
        var dropDown = document.getElementById('leagues-dropdown');
        var dropDownMenu = document.getElementById('leagues-dropdown-menu');
        if (!dropDown) { return false; }
        var handleClick = function(e) {
          var classList = dropDown.classList;
          if (classList.contains('open')) {
            classList.remove('open');
            dropDownMenu.style.display = 'none';
          } else if (e.target == dropDown) {
            classList.add('open');
            dropDownMenu.style.display = 'block';
          }
        };
        document.body.addEventListener('click', handleClick, true);
      })();

      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
      ga('create', 'UA-46472389-1', 'fridayfilmclub.com');
      ga('send', 'pageview');

    </script>
  </body>
</html>

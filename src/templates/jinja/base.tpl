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
      <div class="navbar" id="title-bar">
          <div class="container">
            <a class="navbar-brand custom-font-header" href="{{ uri_for('home') }}">Friday Film Club</a>
            <div id="sign-in" class="hidden-xs">
              {% if logged_in %}
                <span>
                  <b>{{user.name}}</b><br>
                  <a href="{{ uri_for('settings') }}">settings</a> - <a href="{{ uri_for('logout') }}">logout</a>
                </span>
                <img src="{{user.pic_url()}}" width="30" height="30">
              {% else %}
                <a href="{{ uri_for('login') }}" class="btn btn-primary">Login</a>
              {% endif %}
            </div>
          </div>
      </div>

      <div class="navbar navbar-default visible-xs">
        <a class="navbar-brand custom-font-header" href="{{ uri_for('home') }}">FFC</a>
        <div id="sign-in">
          {% if logged_in %}
            <span>
              <b>{{user.name}}</b><br>
              <a href="{{ uri_for('settings') }}">settings</a> - <a href="{{ uri_for('logout') }}">logout</a>
            </span>
            <img src="{{user.pic_url()}}" width="30" height="30">
          {% else %}
            <a href="{{ uri_for('login') }}" class="btn btn-primary">Login</a>
          {% endif %}
        </div>
      </div>

      <div class="navbar navbar-default" id="nav">
        <ul class="nav navbar-nav">
          <li{% if page_id == 'how-page' %} class="active"{% endif %}><a href="/how">How<span class="hide-xs"> to play</span></a></li>
          <li class="hidden-xs {% if page_id == 'archive-page' %} active{% endif %}"><a href="/archive">Old questions</a></li>
          <li{% if page_id == 'leaderboard-page' %} class="active"{% endif %}><a href="/leaderboard">Leaderboard</a></li>
        </ul>
        {% if logged_in %}
        <a href="{{ uri_for('settings') }}#invite" class="btn btn-xs btn-danger" id="invite-nav-button">Invite your friends</a>
        {% endif %}
      </div>
    {% endblock %}

    <div class="container">
      {% block content %}
        <div class="row">
          {% block main %}{% endblock %}
          {% block sidebar %}{% endblock %}
        </div>
      {% endblock %}
      {% block footer %}
        <hr>
        <div id="footer">
          <p>&copy; Friday Film Club <a href="https://twitter.com/FilmMasterJack" target="_blank" class="pull-right" id="follow-twitter">Follow us on Twitter</a></p>
        </div>
      {% endblock %}
    </div>
    {% block body_base %}{% endblock %}
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
      ga('create', 'UA-46472389-1', 'fridayfilmclub.com');
      ga('send', 'pageview');

      (function() {
        var inviteBtn = document.getElementById('invite-nav-button'),
            twitterBtn = document.getElementById('follow-twitter');

        if (inviteBtn) {
          inviteBtn.onclick = function() {
            window['ga']('send', 'event', 'invite', 'click', 'invite-your-friends');
          }
        }
        if (twitterBtn) {
          twitterBtn.onclick = function() {
            window['ga']('send', 'event', 'button', 'click', 'follow-us-on-twitter');
          }
        }
      })();
    </script>
  </body>
</html>

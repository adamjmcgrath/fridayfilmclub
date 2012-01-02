<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Friday Film Club</title>
    <link rel="stylesheet" href="/static/css/default.css">
  </head>
  <body id="{% block page_id %}home-page{% endblock %}"
        class="{% block page_class %}quiz{% endblock %}">
    <div class="wrapper">
      <div id="header">
        {% block header %}
        <h1>Friday Film Club</h1>
        <h2>Think you know film? You don't know Jack.</h2>
        {% endblock %}
      </div>
      <div id="main">
        {% block main %}{% endblock %}
      </div>
      <div id="footer">
        <p>© Friday Film Club</p>
      </div>
      {% block body_base %}{% endblock %}
    </div>
  </body>
</html>

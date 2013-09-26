{% extends "templates/jinja/base.tpl" %}

{% block page_class %}admin{% endblock page_class %}

{% block header %}
<h1>Friday Film Club</h1>
<h2><b>Admin Console</b></h2>
{% endblock %}

{% block main %}
<p class="back"><a href="{{ uri_for('admin-homepage') }}">« Back to Admin</a></p>
{% endblock %}
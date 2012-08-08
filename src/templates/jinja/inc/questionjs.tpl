{% if debug %}
  <script src="/closure-library/closure/goog/base.js"></script>
  <script src="/static/js/deps.js"></script>
  <script>
    goog.require('goog.ui.Component');
    goog.require('ffc.Question');
  </script>
{% else %}
  <script src="/static/js/quiz.js"></script>
{% endif %}

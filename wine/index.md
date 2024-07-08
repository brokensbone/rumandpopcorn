---
title: Wine
---

{{ page.dir | inspect }}
{% for sub_page in site.pages %}
    {% if sub_page.dir contains page.dir %}
        {{ sub_page.url }}
    {% endif %}
{% endfor %}
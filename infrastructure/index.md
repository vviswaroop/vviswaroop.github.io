---
layout: default
title: Infrastructure
permalink: /infrastructure/
---

<h2>Infrastructure</h2>
<p>Posts on platform engineering, CI/CD, and cloud infrastructure.</p>

<ul class="post-list">
  {% for post in site.posts %}
    {% if post.categories contains 'infrastructure' %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <span class="meta">— {{ post.date | date: "%b %d, %Y" }}</span></li>
    {% endif %}
  {% endfor %}
</ul>

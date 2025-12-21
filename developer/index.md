---
layout: default
title: Developer
permalink: /developer/
---

<h2>Developer</h2>
<p>Posts about engineering practices, tooling, and developer experience.</p>

<ul class="post-list">
  {% for post in site.posts %}
    {% if post.tags contains 'developer' %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <span class="meta">— {{ post.date | date: "%b %d, %Y" }}</span></li>
    {% endif %}
  {% endfor %}
</ul>

---
layout: default
title: "Tag: announcement"
permalink: /tag/announcement/
---

<h2>Tag: announcement</h2>

<ul class="post-list">
  {% for post in site.posts %}
    {% if post.tags contains 'announcement' %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <span class="meta">— {{ post.date | date: "%b %d, %Y" }}</span></li>
    {% endif %}
  {% endfor %}
</ul>

---
layout: default
title: Product
permalink: /product/
---

<h2>Product</h2>
<p>Posts about product thinking, design, and ownership.</p>

<ul class="post-list">
  {% for post in site.posts %}
    {% if post.tags contains 'product' %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <span class="meta">— {{ post.date | date: "%b %d, %Y" }}</span></li>
    {% endif %}
  {% endfor %}
</ul>

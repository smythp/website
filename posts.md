---
layout: default
title: All Posts
permalink: /posts/
---

<section>

  <h1 class="display-3">All posts</h1>

  {% assign posts_sorted = site.posts | sort: "date" | reverse %}
  {% assign posts_count = posts_sorted.size %}
  {% assign posts_mod = posts_count | modulo: 2 %}

  <div class="container-fluid">
    {% if posts_mod == 1 %}
    <div class="row row-cols-3 gx-5 gy-5">
    {% else %}
    <div class="row row-cols-2 gx-5 gy-5">
    {% endif %}
      {% for post in posts_sorted %}
      <div class="col">

	<div class="card cover-img">
	  <a href="{{ post.url }}">
	    {% if post.image.feature %}
	    <img src="/assets/images/{{ post.image.feature }}" class="card-img-top" alt="{{ post.title }}">
	    {% else %}
	    <img src="/assets/images/abstract.jpg" class="card-img-top" alt="{{ post.title }}">
	    {% endif %}
	  </a>

	  <div class="card-body">
	    <h2 class="card-title">
	      <a href="{{ post.url }}" class="stretched-link text-decoration-none text-reset">{{ post.title }}</a>
	    </h2>
	    <p>
	      {% if post.summary %}
	      {{ post.summary }}
	      {% else %}
	      {{ post.excerpt | strip_html | truncate: 140 }}
	      {% endif %}
	    </p>

	  </div>
	</div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

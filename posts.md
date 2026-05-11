---
layout: default
title: All Posts
permalink: /posts/
---

<section>

  <h1 class="display-3 mb-5">All posts</h1>

  {% assign posts_sorted = site.posts | sort: "date" | reverse %}

  <div class="container-fluid">
    <div class="card-grid">
      {% for post in posts_sorted %}
	<div class="card cover-img">
	  {% if post.image.feature %}
	  <img src="/assets/images/{{ post.image.feature }}" class="card-img-top" alt="">
	  {% else %}
	  <img src="/assets/images/abstract.jpg" class="card-img-top" alt="">
	  {% endif %}

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
      {% endfor %}
    </div>
  </div>
</section>

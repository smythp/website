---
layout: default
title: Talks
permalink: /talks/
---

<section>

  <h1 class="display-3 mb-5">Talks</h1>

  {% assign talks = site.posts | where: "type", "talk" %}
  {% assign workshops = site.posts | where: "type", "workshop" %}
  {% assign webinars = site.posts | where: "type", "webinar" %}
  {% assign talks_all = talks | concat: workshops | concat: webinars | sort: "date" | reverse %}

  <div class="container-fluid">
    <div class="card-grid">
      {% for post in talks_all %}
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
	    {% if post.subtitle %}
	    <p class="text-secondary">{{ post.subtitle }}</p>
	    {% elsif post.summary %}
	    <p>{{ post.summary }}</p>
	    {% else %}
	    <p>{{ post.excerpt | strip_html | truncate: 140 }}</p>
	    {% endif %}
	  </div>
	</div>
      {% endfor %}
    </div>

    <div class="mt-5">
      <a href="/posts/" class="btn btn-outline-primary btn-lg w-100 py-3 fs-4">All posts &rarr;</a>
    </div>
  </div>
</section>

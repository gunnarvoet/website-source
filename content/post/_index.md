---
title: Posts

# View.
#   1 = List
#   2 = Compact
#   3 = Card
view: 2

# Optional header image (relative to `static/img/` folder).
header:
  caption: ""
  image: ""

# Photographs live in the post bundles, and Hugo publishes every bundle
# resource by default, originals included. That put both a 6000px original
# and its resized copy on the server for each figure. With this set, only
# the resources a template actually asks for are published, which is the
# `Fit "2000x2000"` derivative the figure shortcode makes.
cascade:
  build:
    publishResources: false
---

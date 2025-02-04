---
title: How this all works
subtitle: Containers for days
image: /assets/image/photo/2023/circuits.png
layout: post
--- 

I've not done a how-it-all-works post on here before. Truth be told, quite often I'd probably have struggled to tell you how it worked. Some nice ideas, often half-implemented, a distraction or two, and somehow there it was. Until it wasn't... I'd regularly forget to sort out SSL certs, because I'd never got round to automating it. And writing a new post was surprisingly hard. Where did I have to put the files? What makes it build? And suddenly I've lost the will to work on it and gone off to do something else.

But no more! No. For I have re-organised, redesigned and reimplemented this site from top to bottom. So here's a whistlestop tour through the web-stack. 

> _September 2023 update: Yikes! This post is already outdated. I've started moving to automatically triggered AWS builds which seems like an exciting step!_

## Site code
The content of the site is essentially a bunch of text files. They're plain text, with formatting done in Markdown. This makes them _very simple_ to write. To make them look a little better than plain text though, and sort out all the pesky HTML we lean on Jekyll. There are heaps of static site generators out there. I first discovered Jekyll years ago so have largely stuck with it because its what I know.

When moving the site around I did toy with jumping to Hugo - it looks like a more modern sibling to Jekyll with a lot less code in ruby - but in the end I couldn't really justify the work to learn a new framework. Most of the tangible benefits seemed to be in the build times. I do believe it _is_ faster. But my site builds in Jekyll in ... _checks console_ ... 0.53 seconds. Build time is just not a problem I need to fix right now.

Having run Jekyll, all of my text files are transformed into lovely HTML. I check my new post looks like it should and then its time to push the files up to the webserver. And here's where the next big changes come in...

## Containerise everything!

![containers](containers.png)

My webserver is a cheapish VPS. It's not particularly well resourced but its sufficient for this site. Previously all the config for serving up my site was sat around on the VPS in a bunch of different files. This caused a few problems:
- Testing anything was basically impossible, there was no dev server at all.
- Migrating between VPS setups was an absolute pain. You could all but guarantee nothing would work.

So once we had the problems, how to solve them? Containers. I've now migrated the entire setup (this and a couple of other sites) into a handful of Docker containers, all held together by Docker Compose. It's neat. It's so neat I wish I'd done it years ago.

### SSL Termination
One of the first good steps I took was to split out SSL termination. This means I've got one container, the one that's exposed to the outside world and its whole job is to serve up SSL certificates for all three sites, and then just pass on requests to the relevant site's container. Currently, this is running NGINX but I've got half an eye on replacing it with HAProxy.

The real joy of splitting out the SSL functionality is that I can run the actual sites themselves entirely without certificates. This makes testing changes much easier. I don't need separate dev or localhost configs to run dev versions of these sites now - I simply start the container up anywhere and it _just works_ exactly the same as the real site.

### The rest
The other containers are largely very simple. The one that serves up this site is another very simple NGINX image with the HTML files from earlier injected as a volume. Sorted.

### Version controlled config
And it's all under git. Finally, I can test changes on a dev setup, commit them to the repo and then just run a pill, build and relaunch command to deploy my site changes. And be confident that they work.

## A cloudy future?

![clouds](cloudy.png)

Earlier on I mentioned the difficulty of migrating this setup. I'm now relatively confident that this is a solved problem - the whole site is now just a bunch of config and static files, all version controlled and easy to check out. This should make moving to any other VPS an absolute breeze. The exciting alternative though is to explore some of the 'serverless' options out there - AWS, Azure, Google Cloud, etc. I'm not very experience with any of them but given that the basic modus operandi is spinning up Docker containers with the server-layer abstracted away, I'd say the site was primed ready to make the switch. Exciting times.

----


And lastly, here's a bonus picture of "the internet illustrated in the style of The Matrix", for no better reason than I really like it. You're welcome.

![the internet in the style of the matrix](matrix-internet.png)

_All images generated with Midjourney_
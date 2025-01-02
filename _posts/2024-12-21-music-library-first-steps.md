---
title: "How to build the new music library"
subtitle: MP3s, FLACs, Records
layout: post
tags: music library
--- 

Having decided that it's the right time to rebuild my music library (see [the previous post]({% post_url 2024-12-17-music-library-the-problem %})), I'm now starting to scratch my head over how to do it. 

There are a few areas I clearly need to get my head around and consider the option available to me. These include:
- **Software**: how am I going to organise my library? What will I use to manage tagging files? How will I add files?
- **Data**: how visible will my library data be? How easily can I query it, explore it, check it? This is going to get important when it comes to considering quality control, missing releases, spotting duplicates and so on. 
- **Process**: how am I actually going to work through the process of building this library? Where do I start? What do I prioritise?
- **Goals**: What do I actually want to be able to do, other than listen to the music (obviously!). Am I looking to build themed (sub)collections? To explore genres over time? To listen to specific record labels? 

Some of these are easier to answer than others. 

## Goals
I'm trying not to overcomplicate this, but I think there are quite a lot of exciting opportunities here. I want to be able to:
- Listen to a specific album (obviously)
- Listen to a specific artist
- Listen to a specific genre
- Listen to a specific label

I'd like to be able to build and amend ad-hoc collections with ease ("music for driving", "cooking music", "ambient-ish-stuff-to-listen-to-while-reading").

I'd like to be able to visualise all of the above. I love a graph.

A lesser goal - perhaps more of a nice-to-have - would be to have linking between artists, records, labels, genres. Something where you can get to similar things and explore your collection. I have no idea how feasible this is, and it's by no means essential.

## Data
I want full access to my data. I'm taking it for granted that whatever software I end up using is going to add _some_ sort of data layer on top of file metadata tags - otherwise any query would have to read the whole library! This data *must* be easily accessible. I don't mind if its a simple database written to disk or a JSON API that I can query, I just need to be able to get hold of the data independently of the library software. 

The simpler, the better.

## Software
I think I'm confident in my choices here. I'm sticking with [Beets](https://beets.io/).

Beets has served me well for many, many years. It's a solid bit of open source software built by music nerds for music nerds. It slurps in new files, tags them according to rules and organises them on disk. It's backed by a Sqlite database file, which makes querying the data yourself _really easy_ (apart from Sqlite being a pig about concurrent access...).

## Process
I think I need to get the basic technical elements set up first. Something along the lines of:
- Decide where the files live
- Create a new beets library
- Build a sufficiently comprehensive beets config (consider tagging, file paths, album art, etc)
- Consider how I access the library (web ui, db export, MPD, etc)
- Import an initial batch of albums to see the process in action

After that, I think the fun really starts. It doesn't actually matter how I approach it, I just need to keep adding to the library. I plan to do weeks where I explore a specific genre, the back catalog of a specific artist, revisit records I've not listened to in a while, explore something brand new. It's all welcome.

Key decisions that need making:
- What are the tagging rules?
- What's the filepath structure?
- What do I do with album art? 

Other things to explore:
- Are there nice beets plugins for browsing a library?
- Has anyone worked on mapping MusicBrainz IDs to Spotify URNs?
- Should I commit the configs to a GitHub repo somewhere to go alongside these posts?

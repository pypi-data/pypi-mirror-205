fookebox is a jukebox-style web-frontend to MPD.

It can be used as a keyboard-less jukebox, as a powerful MPD control frontend
or as anything in between.

![Screenshot](https://code.ott.net/fookebox/screenshot.png)

With fookebox you can

 * Browse your music library by artist or genre
 * Add songs to the queue (obviously)
 * Automatically play random music from your collection
 * Limit the queue size
 * Add whole albums to the queue
 * Remove songs from the queue
 * Search for artists or genres
 * Control MPD

## Getting started

```
$ pip install fookefox
$ fookebox
```

Your jukebox should now be ready on [http://localhost:8888/](http://localhost:8888/)

## Configuration

You can run fookebox with a custom configuration:

```
$ fookebox --config my-config.ini
```

The sample config file in `examples/fookebox.ini` explains all available options
and their default values.

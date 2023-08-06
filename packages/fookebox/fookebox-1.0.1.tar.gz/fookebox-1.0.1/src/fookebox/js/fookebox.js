"use strict";

/*
 * fookebox, https://code.ott.net/fookebox/
 * Copyright (c) 2007-2023 Stefan Ott. all rights reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, version 3.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

/* global _ */

function PlayAlbumButton(album)
{
	var div = document.createElement("div");
	div.classList.add("pull-right");

	var button = document.createElement("button");
	button.classList.add("btn");
	button.classList.add("btn-default");
	button.classList.add("btn-md");
	div.append(button);

	var span = document.createElement("span");
	span.classList.add("glyphicon");
	span.classList.add("glyphicon-play");
	button.append(span);

	var text = " " + _("Play album");
	button.append(text);

	div.onclick = function() {
		album.play();
	};

	return div;
}

function AlbumHeader(album, enablePlayAlbum)
{
	var div = document.createElement("div");
	div.classList.add("panel-heading");
	div.classList.add("album-heading");

	var h4 = document.createElement("h4");
	h4.classList.add("panel-title");
	div.append(h4);

	if (enablePlayAlbum)
	{
		h4.append(new PlayAlbumButton(album));
	}

	var name = document.createElement("div");
	name.classList.add("albumTitle");
	name.innerText = album.name;
	h4.append(name);

	var artist = document.createElement("div");
	artist.classList.add("albumArtist");
	artist.innerText = album.artist;
	h4.append(artist);

	var cover = new AlbumCover(album);
	cover.load(div);

	return div;
}

function TrackList(tracks, jukebox)
{
	var body = document.createElement("div");
	body.classList.add("panel-body");

	var list = document.createElement("ul");
	list.classList.add("list-unstyled");
	body.append(list);

	for (var i=0; i < tracks.length; i++)
	{
		var track = tracks[i];
		list.append(new Track(track, jukebox));
	}

	return body;
}

function Track(t, jukebox)
{
	var li = document.createElement("li");

	var link = document.createElement("a");
	link.href = "#";
	link.innerHTML = `${t.track} &ndash; ${t.artist} &ndash; ${t.title}`;
	li.append(link);

	link.onclick = function(event)
	{
		event.preventDefault();
		jukebox.play([t]);
	};

	return li;
}

function AlbumCover(album)
{
	this.album = album;
}

/* RFC3986-compliant version of encodeURIComponent
 *
 * With the normal encodeURIComponent function, parentheses are not encoded.
 * This would lead to URLs that *can* be downloaded with $.ajax but that won't
 * work in CSS rules.
 *
 * Taken from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent
 */
function encodeRFC3986URIComponent(str) {
  return encodeURIComponent(str)
    .replace(
      /[!'()*]/g,
      (c) => `%${c.charCodeAt(0).toString(16).toUpperCase()}`
    );
}

AlbumCover.prototype.load = function(target)
{
	const file = encodeRFC3986URIComponent(this.album.tracks[0].file);
	const url = `cover/${file}`;

	const req = $.ajax(url);

	req.done(function()
	{
		target.style.backgroundImage = `url(${url})`;
	});
	req.fail(function()
	{
		target.classList.add("no-cover");
	});
};

function WindowHandler(jukebox)
{
	this.jukebox = jukebox;
	this.skipval = null;

	$(window).on("hashchange", $.proxy(this.loadhash, this));
	this.loadhash(this);
}

WindowHandler.prototype.loadhash = function()
{
	var hash = window.location.hash;

	if (!hash)
	{
		this.jukebox.showSearch();
		return;
	}

	if (hash == this.skipval)
	{
		this.skipval = null;
		return;
	}
	this.skipval = null;

	var m = hash.match(/([a-z]+)=(.*)$/);

	if (!m || (m.length != 3))
		return;

	var key = m[1];
	var val = decodeURIComponent(m[2]);

	this.jukebox.showItems(key, val);

	if (key == 'artist')
		$('#showArtists').tab('show');
	else if (key == 'genre')
		$('#showGenres').tab('show');
};

WindowHandler.prototype.skip = function(val)
{
	this.skipval = val;
};

function QueueView()
{
	var getMaxLength = function()
	{
		return $('#queue').find('li').length;
	};

	var getCurrentLength = function()
	{
		return $('#queue').find('li:not(.disabled)').length;
	};

	Object.defineProperty(this, 'maxLength',
	{
		get: getMaxLength
	});

	Object.defineProperty(this, 'currentLength',
	{
		get: getCurrentLength
	});
}

QueueView.prototype.updateLabel = function(flash)
{
	var len = this.currentLength;
	var qlen = this.maxLength;
	var label = $('#queueStatus');

	if (len == qlen)
	{
		label.text(_('full'));
		label.removeClass('label-success');
		label.addClass('label-warning');
		label.removeClass('label-info');
	}
	else if (len == 0)
	{
		label.text(_('empty'));
		label.addClass('label-success');
		label.removeClass('label-warning');
		label.removeClass('label-info');
	}
	else
	{
		label.text(len + '/' + qlen);
		label.removeClass('label-success');
		label.removeClass('label-warning');
		label.addClass('label-info');
	}

	if (flash)
	{
		this.pulsate();
	}
};

QueueView.prototype.pulsate = function()
{
	var label = $('#queueStatus');
	label.hide();
	label.show('highlight');
};

QueueView.prototype.delete = function(i)
{
	return function()
	{
		$.ajax("queue/" + (i + 1), {
			"type": "DELETE",
		});

		return false;
	}.bind(this);
};

QueueView.prototype.load = function(data)
{
	if (!("queue" in data))
	{
		return;
	}

	var len = data.queue.length;
	var prevlen = this.currentLength;
	var els = $("#queue li");

	for (var i=0; i < this.maxLength; i++)
	{
		var el = $(els[i]);
		var link = el.find("a");

		link.off("click");

		if (i >= len)
		{
			el.addClass("disabled");
			link.find(".artist").text("");
			link.find(".title").text("");
			link.click(function() {
				return false;
			});
			continue;
		}

		var track = data.queue[i];
		link.find(".artist").text(track.artist);
		link.find(".title").text(track.title);
		el.removeClass("disabled");

		if (el.find("span.controls").length > 0)
		{
			link.click(this.delete(i));
		}
		else
		{
			link.click(function() {
				return false;
			});
		}
	}

	this.updateLabel(len != prevlen);
};

function AlbumList()
{
	this.albums = new Object();
}

AlbumList.prototype.contains = function(album)
{
	return (album.hash() in this.albums);
};

AlbumList.prototype.add = function(album)
{
	this.albums[album.hash()] = album;
};

AlbumList.prototype.get = function(album)
{
	return this.albums[album.hash()];
};

AlbumList.prototype.sortAll = function()
{
	for (var key in this.albums)
	{
		var album = this.albums[key];
		album.sort(function(a, b)
		{
			return Number(a.track) - Number(b.track);
		});
	}
};

AlbumList.prototype.render = function()
{
	var queueAlbums = false;
	var albums = new Array();
	var body = $("body");

	if (body.attr("queue-albums"))
	{
		queueAlbums = true;
	}

	for (var key in this.albums)
	{
		albums.push(this.albums[key]);
	}

	albums.sort(function(a, b)
	{
		return a.name > b.name;
	});

	$(albums).each(function(i, album)
	{
		album.render(queueAlbums);
	});
};

function Album(jukebox, path, name)
{
	this.jukebox = jukebox;
	this.path = path;
	this.name = name;
	this.artist = '';
	this.tracks = new Array();
}

Album.prototype.hash = function()
{
	return btoa(escape('' + this.name + this.path));
};

Album.prototype.add = function(track)
{
	this.tracks.push(track);

	if (this.artist == '')
	{
		this.artist = track.artist;
	}
	else if ((this.artist.indexOf(track.artist) < 0) &&
		(track.artist.indexOf(this.artist) < 0))
	{
		this.artist = _('Various artists');
	}
};

Album.prototype.sort = function(f)
{
	this.tracks.sort(f);
};

Album.prototype.play = function()
{
	this.jukebox.play(this.tracks);
};

Album.prototype.render = function(enablePlayAlbum)
{
	$('#result').append(new AlbumHeader(this, enablePlayAlbum));
	$('#result').append(new TrackList(this.tracks, this.jukebox));
};

function SearchResult(jukebox, tracks)
{
	this.tracks = tracks;
	this.jukebox = jukebox;
	this.albums = new AlbumList();

	function tracknum(input)
	{
		if ((input == '') || !input)
			return '00';
		else if (input.indexOf('/') >= 0)
			return tracknum(input.replace(/\/.*/, ''));
		else if (input.length < 2)
			return '0' + input;
		else
			return input;
	}

	function mkstring(input, type)
	{
		if (typeof input == "string")
		{
			return input;
		}
		else if (typeof input == "object")
		{
			if (input.length > 0)
				return input[0];
		}

		return _('Unnamed ' + type);
	}

	$(this.tracks).each(function(i, track)
	{
		track.track = tracknum(track.track);
		track.album = mkstring(track.album, 'album');
	});

	this.parseAlbums();
}

SearchResult.prototype.parseAlbums = function()
{
	$(this.tracks).each($.proxy(function(i, track)
	{
		var album;
		var file = track.file;
		var dir = file.substring(0, file.lastIndexOf("/") + 1);
		var fn = file.substring(file.lastIndexOf("/") + 1);

		if (!track.artist)
			track.artist = _('Unknown artist');
		if (!track.title)
			track.title = _('Unnamed track') + ' [' + fn + ']';

		album = new Album(this.jukebox, dir, track.album);

		if (!this.albums.contains(album))
		{
			this.albums.add(album);
		}

		album = this.albums.get(album);
		album.add(track);
	}, this));

	this.albums.sortAll();
};

SearchResult.prototype.show = function()
{
	$('#result').empty();
	this.albums.render();
};

function FookeboxSocket()
{
	const hostname = window.location.hostname;
	const port = window.location.port;
	this._url = `ws://${hostname}:${port}/socket`;
}

FookeboxSocket.prototype.listen = function(client)
{
	this._sock = new WebSocket(this._url);
	this._sock.addEventListener('close', () => {
		setTimeout(this.listen.bind(this), 1000, client);
		console.log('Connection lost, reconnecting');
	});
	this._sock.addEventListener('message', (event) => {
		var data = JSON.parse(event.data);
		client.notify(data);
	});
};

function Jukebox()
{
	this.queue = new QueueView();
	this._state = 'stop';
}

Jukebox.prototype.showSearch = function()
{
	$('.navbar-toggle').removeClass('hidden-xs');
	$('.sidebar').removeClass('hidden-xs');
	$('.main').addClass('hidden-xs');
};

Jukebox.prototype.showResult = function()
{
	$('.navbar-toggle').addClass('hidden-xs');
	$('.sidebar').addClass('hidden-xs');
	$('.main').removeClass('hidden-xs');
	window.scrollTo(0,0);
	$('.main').scrollTop(0);
};

Jukebox.prototype.sync = function()
{
	const sock = new FookeboxSocket();
	sock.listen(this);
};

Jukebox.prototype.notify = function(data)
{
	const status = data.status;
	if (status) {
		if (status.state) {
			this._state = status.state;
		}
	}

	let playlist = data.playlistinfo;

	if (playlist) {
		const queue = playlist.splice(1);
		this.updatePlayer(playlist.pop());
		this.queue.load({'queue': queue});
	}
};

Jukebox.prototype.updatePlayer = function(data)
{
	if (data) {
		if ('artist' in data) {
			$('.currentArtist').text(data.artist);
		} else if (this._state == 'play') {
			$('.currentArtist').text(_('Unknown artist'));
		} else {
			$('.currentArtist').empty();
		}

		if ('title' in data) {
			$('.currentTitle').text(data.title);
		} else if (this._state == 'play') {
			$('.currentTitle').text(_('Unnamed track'));
		} else {
			$('.currentTitle').empty();
		}
	} else {
		$('.currentArtist').empty();
		$('.currentTitle').empty();
	}
};

Jukebox.prototype.showItems = function(type, name)
{
	const name_encoded = encodeRFC3986URIComponent(name);
	const req = $.getJSON(type + "/" + name_encoded);

	const well = $('<div class="well"></div>');
	well.text(_("Loading, please wait..."));
	const panel = $('<div class="panel panel-default"><div class="panel-body"></div></div>');
	panel.append(well);

	panel.fadeIn(400);
	$('#result').empty();
	$('#result').append(panel);

	this.showResult();

	req.done($.proxy(function(data)
	{
		const result = new SearchResult(this, data.tracks);
		result.show();
	}, this));

	req.fail(function()
	{
		console.error("failed");
	});
};

Jukebox.prototype.play = function(tracks)
{
	var files = tracks.map(function(obj) {
		return obj.file;
	});

	var req = $.ajax("queue",
	{
		"data": JSON.stringify({"files": files}),
		"type": "POST",
		"processData": false,
		"contentType": "application/json"
	});

	req.error($.proxy(function(data)
	{
		switch(data.status)
		{
			case 409:
				this.queue.pulsate();
				break;
			default:
				console.error(data);
		}
	}, this));
};

Jukebox.prototype.showGenre = function(name)
{
	this.showItems('genre', name);
};

Jukebox.prototype.showArtist = function(name)
{
	this.showItems('artist', name);
};

Jukebox.prototype.control = function(action)
{
	var data = { 'action': action };

	$.ajax({
		url: 'control',
		type: 'POST',
		data: JSON.stringify(data),
		contentType: 'application/json; charset=utf-8'
	});
};

$(document).ready(function()
{
	function filter(list)
	{
		return function(event)
		{
			var el = $(event.currentTarget);
			var val = el.val().toLowerCase();

			list.each(function(i, item)
			{
				var link = $(item).find('a');
				var text = link.text().toLowerCase();

				if (text.indexOf(val) > -1)
					link.show();
				else
					link.hide();
			});
		};
	}

	function noop(event)
	{
		event.preventDefault();
	}

	function show(hashPrefix, showFunc)
	{
		return function(event)
		{
			event.preventDefault();

			const target = $(event.target);
			const val = target.data('value');
			const hash = hashPrefix + encodeRFC3986URIComponent(val);
			wh.skip(hash);
			window.location.hash = hash;

			showFunc(val);
		};
	}

	var jukebox = new Jukebox();
	jukebox.sync();

	var wh = new WindowHandler(jukebox);

	$('#artistSearch').keyup(filter($('li.artist')));
	$('#genreSearch').keyup(filter($('li.genre')));
	$('#artistSearchForm').submit(noop);
	$('#genreSearchForm').submit(noop);
	$('li.artist a').click(show('#artist=', $.proxy(jukebox.showArtist, jukebox)));
	$('li.genre a').click(show('#genre=', $.proxy(jukebox.showGenre, jukebox)));

	function addControl(key)
	{
		$('#control-' + key).click(function()
		{
			jukebox.control(key);
			return false;
		});
	}

	if ($('#controls'))
	{
		addControl('prev');
		addControl('pause');
		addControl('play');
		addControl('next');
		addControl('voldown');
		addControl('volup');
		addControl('rebuild');
	}
});

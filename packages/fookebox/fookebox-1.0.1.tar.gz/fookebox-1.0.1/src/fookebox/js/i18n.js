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

/* global i18n */

window._ = function(s)
{
	if (typeof(i18n) != 'undefined' && i18n[s])
	{
		return i18n[s];
	}
	return s;
};

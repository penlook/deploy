#!/bin/bash
#
# Penlook Project
#
# Copyright (c) 2015 Penlook Development Team
#
# --------------------------------------------------------------------
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------
#
# Author:
#     Loi Nguyen       <loint@penlook.com>

from os import path

class Logger:

	def __init__(self):
		def __init__(self):
		log_dir = "/var/log/penlook"
		os.mkdir(log_dir, 0755)
		self.path = log_dir + "/log"
		self.file = open(self.path, 'a')

	def reset_log(self):
		pass

	def log(self, message):
		self.file.write(message + "\n")

	def close(self):
		self.file.close()

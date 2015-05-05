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

from config import *
from ec2 import *
from logger import *
import sys
import os
import thread

class Deploy:

	running = 0

	def __init__(self):
		self.config = Config()

	def list_instances(self):
		self.ec2 = EC2(self.config)
		return self.ec2.list_instances_in_balancer()

	# Deploy to single instance
	def deploy_to_instance(self, instance):
		print " --> Server : ", instance.ip_address
		client = self.ec2.ssh_to_instance(instance)
		status, stdout, stderr = client.run('ls -la')

		message = "------- MESSAGE " + instance.ip_address + "-------"
		self.logger.log(message)
		self.logger.log(stdout)

		if status == 0:
			print 'Success : ', instance.ip_address
		else:
			print 'Error : ', instance.ip_address

		self.running -= 1

	# Deploy to multiple server
	def deploy_to_cluster(self):
		self.instances = self.list_instances()
		self.logger = Logger()

		for instance in self.instances:
			if instance.state == "running":
				# Instance Object
				# https://github.com/turnkeylinux/python-boto/blob/master/boto/ec2/instance.py#L71
				self.running += 1
				#self.deploy_to_instance(instance)
				thread.start_new_thread(self.deploy_to_instance, (instance,))

		# Waiting for all deployment had finished
		while self.running > 0:
			# Pass keyword means "do nothing"
			pass

		self.logger.close()


deploy = Deploy()
deploy.deploy_to_cluster()

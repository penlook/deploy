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

import boto, boto.ec2.elb
from boto.manage.cmdshell import sshclient_from_instance
import os

class EC2:

	def __init__(self, config):
		self.config = config

	# Established new connection to Amazon Web Service
	def get_ec2_connection(self):
		connection = None
		try:
			connection = boto.ec2.connect_to_region(
				self.config.region_name,
				aws_access_key_id = self.config.access_key,
				aws_secret_access_key = self.config.secret_key)
		except:
			raise
		if connection is None:
			print "EC2 Connection fail !"
			exit(1)
		return connection

	# Get load balancer connection
	def get_load_balancer_connection(self):
		return boto.ec2.elb.connect_to_region(
			self.config.region_name,
			aws_access_key_id = self.config.access_key,
			aws_secret_access_key = self.config.secret_key)

	# Get load balancer by name
	def get_load_balancer_by_name(self, load_balancer_name = None):
		if load_balancer_name is None:
			load_balancer_name = self.config.load_balancer
		elb_connection = self.get_load_balancer_connection()
		return elb_connection.get_all_load_balancers(load_balancer_names = [load_balancer_name])[0]

	# List all instance in region
	def list_instances(self):
		ec2_connection = self.get_ec2_connection()
		reservations = ec2_connection.get_all_instances()
		instance_objects = [i for r in reservations for i in r.instances]
		instances = {}
		for instance in instance_objects:
			instances[str(instance.id)] = instance
		return instances

	# List all instance was added in load balancer
	def list_instances_in_balancer(self, load_balancer_name = None):
		instances = self.list_instances()
		instances_in_balancer = []
		load_balancer = self.get_load_balancer_by_name(load_balancer_name)
		for instance_ in load_balancer.instances:
			instance = instances[instance_.id]
			instances_in_balancer.append(instance)
		return instances_in_balancer

	# Transfer command and execute by instance (remote access)
	def ssh_to_instance(self, instance):
		ssh_client = None
		try:
			ssh_client = sshclient_from_instance(instance, self.config.pem_file, user_name = "root")
		except:
			raise
		if ssh_client is None:
			print "Can not access IP : ", instance.ip_address
			os.exit(1)
		return ssh_client


from setuptools import setup

setup(
	name='cloudkit-worker',
	version='1.0',
	packages=[
		'cloudworker'
	],
	install_requires=[
		'websocket-client'
	]
)
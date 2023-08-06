import websocket
import time
import threading
import ctypes
import json
import base64
from types import GeneratorType
from urllib.parse import urlencode


status = dict()
do_task_func = None
handle_message_func = None
ws = None



def handle_message(payload):
	handle_message_func(**payload)


def process_task(payload):
	try:
		for key, blob in payload['files'].items():
			payload['files'][key] = base64.b64decode(blob)

		result = do_task_func(**payload)

		if isinstance(result, GeneratorType):
			for piece in result:
				dispatch_result(piece)
		else:
			dispatch_result(result)

		send_to_master({ 'event': 'done' })

	except Exception as e:
		send_to_master({
			'event': 'error',
			'message': str(e)
		})
		time.sleep(0.1)
		raise e


def dispatch_result(result):
	if result is None:
		result = {}

	if 'files' in result:
		for key, blob in result['files'].items():
			result['files'][key] = base64.b64encode(blob).decode()

	send_to_master({
		'event': 'result',
		**result
	})


def on_message(ws, message):
	payload = json.loads(message)
	command = payload['command']
	
	if command == 'task':
		global current_thread
		current_thread = threading.Thread(target=process_task, args=(payload,))
		current_thread.start()

	elif command == 'abort':
		if not current_thread:
			return

		if not kill_thread(current_thread):
			print('unable to kill thread')
			return

		print('aborted current task')

		current_thread = None
		send_to_master({ 'event': 'abort' })

	else:
		handler_thread = threading.Thread(target=handle_message, args=(payload,))
		handler_thread.start()


def on_error(ws, error):
	if isinstance(error, KeyboardInterrupt):
		print('socket closed and exiting gracefully')
		exit(0)
	else:
		print('socket error:', error)


def kill_thread(thread):
	if hasattr(thread, '_thread_id'):
		thread_id = thread._thread_id
	else:
		for id, t in threading._active.items():
			if t is thread:
				thread_id = id
				break

	result_code = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))

	if result_code > 1:
		ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
		return False

	return True


def update_worker_status(updates):
	global status

	status = {
		**status,
		**updates
	}

	send_to_master({
		'event': 'status',
		**updates
	})


def connect_to_master(master_url, handle_message, do_task, meta):
	global ws, do_task_func, handle_message_func

	handle_message_func = handle_message
	do_task_func = do_task

	def on_open(ws):
		print('connection accepted')
		send_to_master({
			'event': 'init',
			'status': status
		})	

	def on_close(ws, code, message):
		print('lost connection to master')

	ws = websocket.WebSocketApp(
		'%s&%s' % (
			master_url,
			urlencode(meta)
		),
		on_open=on_open,
		on_message=on_message,
		on_error=on_error,
		on_close=on_close,
	)

	print('connecting to master')
	ws.run_forever()


def send_to_master(message):
	ws.send(json.dumps(message))
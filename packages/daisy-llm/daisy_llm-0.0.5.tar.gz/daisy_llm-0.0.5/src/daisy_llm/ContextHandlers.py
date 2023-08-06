import logging
import datetime
import json
import sqlite3
import time
import threading
from sqlite3 import Error
import sqlite3
from .Chat import Chat
import re
from ruamel.yaml import YAML
from .Text import print_text
yaml = YAML()

class ConnectionPool:
	def __init__(self, db_path, max_connections=5):
		self.db_path = db_path
		self.max_connections = max_connections
		self.connections = {}
		self.lock = threading.Lock()



	def get_connection(self):
		thread_id = threading.get_ident()
		self.lock.acquire()
		try:
			if thread_id in self.connections:
				return self.connections[thread_id]
			elif len(self.connections) < self.max_connections:
				conn = sqlite3.connect(self.db_path)
				self.connections[thread_id] = conn
				return conn
			else:
				raise Exception("Connection pool exhausted")
		finally:
			self.lock.release()

	def put_connection(self, conn):
		thread_id = threading.get_ident()
		self.lock.acquire()
		try:
			if thread_id in self.connections:
				self.connections[thread_id] = None
			else:
				conn.close()
		finally:
			self.lock.release()


class ContextHandlers:
	description = "A class for handling and managing messages in the chatGPT context object"

	def __init__(self, db_path):
		self.chat = Chat()

		#Get and set conversation_id from configs.yaml
		self.conversation_id = None
		with open("configs.yaml", "r") as f:
			configs = yaml.load(f)
		if 'conversation_id' in configs:
			self.conversation_id = configs.get("conversation_id")
			logging.info("Using conversation id from configs: " + str(self.conversation_id))


		self.db_path = db_path
		self.messages = []
		self.start_prompts = []
		self.connection_pool = ConnectionPool(db_path)


	def load_context(self):
		self.messages = []
		self.create_conversations_table_if_not_exists()
		with self.connection_pool.get_connection() as conn:

			cursor = conn.cursor()

			# If conversation_id is not set, create a new conversation ID
			if not self.conversation_id:
				self.conversation_id = str(int(time.time()))

				print_text("Creating new conversation: ", "yellow")
				print_text(str(self.conversation_id), None, "\n")

			logging.info("Conversation id: " + str(self.conversation_id))

			# Get the messages from the conversation ID
			cursor.execute('''
				SELECT * FROM messages WHERE id = ?
			''', (self.conversation_id,))
			rows = cursor.fetchall()
			if rows:
				for row in rows:
					message = json.loads(row[1])
					self.messages.append(message)
				print_text("Loaded "+ str(len(rows)) + " messages from conversation id: " + str(self.conversation_id), "yellow", "\n")

	def create_conversations_table_if_not_exists(self):
		with self.connection_pool.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS messages (
					id TEXT NOT NULL,
					message TEXT NOT NULL
				);
			''')
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS conversations (
					id TEXT PRIMARY KEY,
					name TEXT NOT NULL,
					summary TEXT NOT NULL
				);
			''')

	def save_context(self):
		logging.info("Saving context: " + str(self.conversation_id))
		with self.connection_pool.get_connection() as conn:
			conn.execute('''
				PRAGMA foreign_keys=OFF;
			''')
			conn.execute('''
				BEGIN TRANSACTION;
			''')

			# Insert conversation information if it doesn't already exist
			rows = conn.execute('''
				SELECT COUNT(*) FROM conversations WHERE id = ?;
			''', (self.conversation_id,)).fetchone()[0]
			if rows == 0:
				conn.execute('''
					INSERT INTO conversations (id, name, summary)
					VALUES (?, ?, ?);
				''', (self.conversation_id, "No name", "No summary"))

			# Save messages
			conn.execute('''
				DELETE FROM messages WHERE id = ?;
			''', (self.conversation_id,))
			for message in self.messages:
				json_message = json.dumps(message)
				conn.execute('''
					INSERT INTO messages (id, message) VALUES (?, ?);
				''', (self.conversation_id, json_message,))
			conn.execute('''
				COMMIT;
			''')
			row_count = conn.execute('''
				SELECT COUNT(*) FROM messages WHERE id = ?;
			''', (self.conversation_id,)).fetchone()[0]
			logging.info(f"Inserted {row_count} rows for conversation {self.conversation_id}.")

	def get_context(self):
		context = []
		#Append start prompts to messages
		for start_prompt in self.start_prompts:
			context.append(start_prompt)

		for message in self.messages:
			context.append(message)
		return context

	def get_context_without_timestamp(self):
		messages_without_timestamp = []

		for message in self.get_context():
			message_without_timestamp = message.copy()
			del message_without_timestamp['timestamp']
			messages_without_timestamp.append(message_without_timestamp)
		return messages_without_timestamp

	def get_conversation_name_summary(self, limit=None):
		with self.connection_pool.get_connection() as conn:
			cursor = conn.cursor()
			query = '''SELECT id, name, summary FROM conversations ORDER BY id DESC'''
			if limit:
				query += f' LIMIT {limit}'
			cursor.execute(query)
			rows = cursor.fetchall()
			if rows:
				return [(id, name, summary) for id, name, summary in rows]
			else:
				return None

	def single_message_context(self, role, message, incl_timestamp=True):
		if incl_timestamp:
			now = datetime.datetime.now()
			timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
			return {'role': role, 'timestamp': timestamp, 'content': str(message)}
		else:
			return {'role': role, 'content': str(message)}

	def add_start_prompt(self, role="system", message=""):
		start_prompt = self.single_message_context(role, message)
		self.start_prompts.append(start_prompt)

	def add_message_object(self, role, message):
		logging.debug("Adding " + role + " message to context")
		now = datetime.datetime.now()
		timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
		new_message = {'role': role, 'timestamp': timestamp, 'content': str(message)}
		self.messages.append(new_message)
		self.save_context()
		logging.debug(self.messages)

	def add_message_object_at_start(self, role, message):
		logging.debug("Appending " + role + " message at start of context")
		now = datetime.datetime.now()
		timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
		new_message = {'role': role, 'timestamp': timestamp, 'content': str(message)}
		self.messages.insert(0, new_message)
		self.save_context()
		logging.debug(self.messages)

	def remove_last_message_object(self):
		if self.messages:
			self.messages.pop()
			self.save_context()

	def get_last_message_object(self, user_type=None):
		if user_type:
			for message in reversed(self.messages):
				if message['role'] == user_type:
					return message
		else:
			if self.messages:
				return self.messages[-1]
		return False

	def replace_last_message_object(self, message, user_type=None):
		if user_type:
			for i in reversed(range(len(self.messages))):
				if self.messages[i]['role'] == user_type:
					self.messages[i]['content'] = message
					self.save_context()
					return
		elif message and self.messages:
			self.messages[-1]['content'] = message
			self.save_context()

	def delete_message_at_index(self, index):
		try:
			index = int(index)
			if index < len(self.messages) and index >= 0:
				self.messages.pop(index)
				self.save_context()
				return True
		except ValueError:
			pass
		return False

	def update_message_at_index(self, message, index):
		try:
			index = int(index)
			if index < len(self.messages) and index >= 0:
				self.messages[index]['content'] = message
				now = datetime.datetime.now()
				self.messages[index]['timestamp'] = now.strftime('%Y-%m-%d %H:%M:%S')
				self.save_context()
		except ValueError:
			pass
		return False

	def update_conversation_name_summary(self, conversation_id=None, update_all=False):
		conversation_ids = []

		if conversation_id:
			conversation_ids.append(conversation_id)
		elif update_all:
			conversation_ids = self.get_conversation_ids()
		else:
			conversation_ids.append(self.conversation_id)
			# Get conversations with missing name or summary
			conversations = self.get_conversation_name_summary(limit=None)
			for conv_id, name, summary in conversations:
				if name == "No name" or summary == "No summary":
					if conv_id not in conversation_ids:
						conversation_ids.append(conv_id)

		for conv_id in conversation_ids:
			messages = self.get_conversation_context_by_id(conv_id, include_timestamp=False)
			#If there are no messages in the context, delete it
			
			if not messages:
				self.delete_conversation_by_id(conv_id)

			# Get the name of the current conversation from the LLM
			time.sleep(1)
			logging.info("Updating conversation name and summary for: " + conv_id)

			while True:
				prompt = """
				Please respond with a name, and summary for this conversation.
				1. The name should be a single word or short phrase, no more than 5 words."
				2. The summary should be a fairly verbose summary of the conversation, as short as possible while still containing all of the important topics, names, places, and sentiment of conversation.
				3. The output must follow the following JSON format: {"name": name, "summary": summary}
				4. If the conversation is empty, please respond with "Empty"
				"""
				if messages:
					messages.append(self.single_message_context('system', prompt, False))

					print_text("Conversation info (" + str(conv_id) + "): ", "yellow")
					response = self.chat.request(
						messages=messages,
						silent=False,
						response_label=False
					)
				else:
					response = '{"name": "Empty Conversation", "summary": "None"}'


				# Extract the JSON response from the string
				response_match = re.search(r"{.*}", response)
				if response_match:
					response_json = response_match.group(0)
					break
				else:
					logging.error("Invalid response format while setting conversation name and summary. Trying again...")

			# Convert the JSON response to an object
			try:
				response_obj = json.loads(response_json)
			except Exception as e:
				logging.error("Invalid JSON response while setting conversation name and summary: " + str(e))
				return

			# Update the name and summary of the current conversation in the database
			with self.connection_pool.get_connection() as conn:
				cursor = conn.cursor()
				cursor.execute(
					'''UPDATE conversations SET name = ?, summary = ? WHERE id = ?''',
					(response_obj["name"], response_obj["summary"], conv_id)
				)
				conn.commit()

			logging.info("Name and summary updated for conversation " + conv_id + ": " + response_obj["name"])

	def get_conversation_ids(self):
		with self.connection_pool.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute('''SELECT id FROM conversations;''')
			rows = cursor.fetchall()
			return [row[0] for row in rows]

	def new_conversation(self):
		# Generate a new conversation ID
		conversation_id = str(int(time.time()))
		logging.info("Creating a new conversation: " + conversation_id)

		# Set the new conversation ID in configs.yaml
		with open("configs.yaml", "r") as f:
			configs = yaml.load(f)
		configs['conversation_id'] = conversation_id
		with open("configs.yaml", "w") as f:
			yaml.dump(configs, f)

		# Update the conversation ID and load the context
		self.conversation_id = conversation_id
		self.load_context()

	def get_conversation_name_by_id(self, conversation_id):
		with self.connection_pool.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute(
				'''SELECT name FROM conversations WHERE id = ?''',
				(conversation_id,)
			)
			row = cursor.fetchone()
			if row:
				return row[0]
			else:
				return None
			
	def get_conversation_context_by_id(self, conversation_id, include_timestamp=True):
		# Check if the conversation ID exists in the database
		with self.connection_pool.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute('''
				SELECT id FROM conversations WHERE id = ?;
			''', (conversation_id,))
			row = cursor.fetchone()

		if row:
			# Get the messages from the specified conversation ID
			with self.connection_pool.get_connection() as conn:
				cursor = conn.cursor()
				cursor.execute('''
					SELECT message FROM messages WHERE id = ?;
				''', (conversation_id,))
				rows = cursor.fetchall()

			context = []
			if rows:
				for row in rows:
					message = json.loads(row[0])
					if not include_timestamp:
						message.pop('timestamp', None)
					context.append(message)

			return context
		else:
			return None

	def set_conversation_by_id(self, conversation_id):
		if str(conversation_id).isdigit():
			conversation_id = int(conversation_id)
		else:
			return False
			
		logging.info("Setting conversation ID: " + str(conversation_id))
		
		# Check if the conversation ID exists in the database
		with self.connection_pool.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute('''
				SELECT id FROM conversations WHERE id = ?;
			''', (conversation_id,))
			row = cursor.fetchone()
		
		if row:
			# Set the conversation ID in configs.yaml
			with open("configs.yaml", "r") as f:
				configs = yaml.load(f)
			configs['conversation_id'] = conversation_id
			with open("configs.yaml", "w") as f:
				yaml.dump(configs, f)
			
			# Update the conversation ID and load the context
			self.conversation_id = conversation_id
			self.load_context()
			return True
		else:
			return False
		
	def delete_conversation_by_id(self, conversation_id):
		logging.info("Deleting conversation ID: " + conversation_id)
		
		# Check if the conversation ID exists in the database
		with self.connection_pool.get_connection() as conn:
			cursor = conn.cursor()
			cursor.execute('''
				SELECT id FROM conversations WHERE id = ?;
			''', (conversation_id,))
			row = cursor.fetchone()
		
		if row:
			# Delete the conversation from the database
			with self.connection_pool.get_connection() as conn:
				cursor = conn.cursor()
				cursor.execute('''
					DELETE FROM conversations WHERE id = ?;
					DELETE FROM messages WHERE id = ?;
				''', (conversation_id, conversation_id,))
				conn.commit()
			
			# Clear the conversation ID in configs.yaml if it matches the deleted conversation
			with open("configs.yaml", "r") as f:
				configs = yaml.load(f)
			if configs.get('conversation_id') == conversation_id:
				configs['conversation_id'] = None
				with open("configs.yaml", "w") as f:
					yaml.dump(configs, f)
			
			# Reset the conversation ID and reload the context
			self.conversation_id = None
			self.load_context()
			return True
		else:
			return False

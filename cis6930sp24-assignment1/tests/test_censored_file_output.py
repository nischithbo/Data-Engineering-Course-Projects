from censoror import create_censored_file
import os


def test_censored_file_output():
	file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'resources', "test")
	folder_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'resources')
	content = f'On███████████████,██████████at█████████████████████████████████████, can be reached at (555) 123-4567.'
	create_censored_file(content, file_path, folder_path)
	assert os.path.exists(os.path.join(folder_path, "test.censored"))
	with open(os.path.join(folder_path, "test.censored"), 'r', encoding='utf-8') as file:
		contents = file.read()
		assert contents == content



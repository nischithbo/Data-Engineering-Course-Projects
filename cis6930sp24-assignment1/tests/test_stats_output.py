from censoror import write_stats
import os


def test_stat_file_output():
	file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'resources', "stats")
	stats = f"""{'*' * 25} Stats for file : {os.path.basename(file_path)} {"*" * 25}\n""" + \
		f"""censored name count: {5}\n""" \
		f"""Censored address count : {10}\n""" \
		f"""Censored date count: {20}\n""" \
		f"""Censored phone numbers: {20}\n"""
	write_stats(stats, file_path)
	assert os.path.exists(file_path)
	with open(file_path, 'r', encoding='utf-8') as file:
		contents = file.read()
		assert contents == stats

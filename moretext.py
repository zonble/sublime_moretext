import sublime, sublime_plugin
import threading

class MoreTextAPICall(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.result = None

	def run(self):
		import json, urllib2
		moreJSURL = 'http://more.handlino.com//sentences.json'
		try:
			r = urllib2.urlopen(moreJSURL, timeout=5).read()
			j = json.loads(r)
			self.result = j['sentences'][0]
		except Exception, e:
			sublime.error_message(str(e))
			self.result = None

class MoreTextCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		thread = MoreTextAPICall()
		sublime.status_message("Loading data from more.handlino.com...")
		thread.start()
		thread.join()
		sublime.status_message("")
		if thread.result:
			region = self.view.sel()[0]
			self.view.replace(edit, region, thread.result)

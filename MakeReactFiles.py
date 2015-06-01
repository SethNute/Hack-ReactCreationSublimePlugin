import sublime
import sublime_plugin
import re
import os
from config import *

class MakeReactFilesBase(sublime_plugin.WindowCommand):
	def runCommand(self):
		self.window.show_input_panel(self.MODULE_NAME_QUESTION_TEXT, "", self.setModuleNameAndPromptForPath, None, None)

	#Have to promt for path here because you can't use show_input_panel() twice in a row
	def setModuleNameAndPromptForPath(self, user_input_name):
		self.MODULE_NAME = user_input_name
		self.window.show_input_panel(self.PATH_QUESTION_TEXT, "", self.pathInputCallback, None, None)

	def pathInputCallback(self, user_path_to_file):
		closure_file_path = BASE_CLOSURE_PATH + user_path_to_file
		react_file_path = BASE_REACT_PATH + user_path_to_file

		if self.attemptFileCreation(closure_file_path):
			self.populateClosureFile(closure_file_path)
			
		if self.attemptFileCreation(react_file_path):
			self.populateReactFile(react_file_path)
		
	def attemptFileCreation(self, file_to_create):
		if os.path.exists(file_to_create):
			sublime.error_message('File at %s already exists' % file_to_create)
			return False
		else:
			base_dir_path, file_name = os.path.split(file_to_create)
			self.createDirectory(base_dir_path)
			self.createFile(file_to_create)
			return True

	def createDirectory(self, base_dir_path):
		if not os.path.exists(base_dir_path):
			next_dir_up = os.path.split(base_dir_path)[0]
			if not os.path.exists(next_dir_up):
				self.createDirectory(next_dir_up)
			os.mkdir(base_dir_path)

	def createFile(self, file_to_create):
		with file(file_to_create, 'a'):
			os.utime(file_to_create, None)

	def populateClosureFile(self, closure_file_path):
		view = self.window.open_file(closure_file_path)
		view.settings().set('is_Closure', True)
		self.setModuleNameSettingOnView(view)

	def populateReactFile(self, react_file_path):
		view = self.window.open_file(react_file_path)
		view.settings().set('is_Closure', False)
		self.setModuleNameSettingOnView(view)
	
	def setModuleNameSettingOnView(self, view):		
		view.settings().set('react_module_name', (BASE_REACT_MODULE_PREFIX + self.MODULE_NAME))
		view.settings().set('closure_module_name', (BASE_CLOSURE_MODULE_PREFIX + self.MODULE_NAME))
		
#Based on https://github.com/noklesta/SublimeQuickFileCreator/blob/master/SublimeQuickFileCreator.py
class MakeReactFilesCommand(MakeReactFilesBase):
	MODULE_NAME = None
	PATH_QUESTION_TEXT = 'Specify path starting from closure and react base directories:'
	MODULE_NAME_QUESTION_TEXT = 'Specify module name to provide, minus prefix:'

	def run(self):
		self.runCommand()

class PopulateNewFilesListener(sublime_plugin.EventListener):
	def on_load(self, view):
		if view.settings().get('is_Closure'):
			self.populateClosureFile(view)
		else:
			self.populateReactFile(view)

	def populateClosureFile(self, view):
		snippet = """goog.provide('$1');

goog.require('$2');

/**
 * @constructor
 * @extends {}
 */
$1 = function () {
  goog.base(this);
};
goog.inherits($1, /* Put extended here */);

/** @inheritDoc */
$1.prototype.enterDocument = function () {
  goog.base(this, 'enterDocument');
};

/** @inheritDoc */
$1.prototype.onLoaded = function () {
  goog.base(this, 'onLoaded');
  this.update_();
};

/**
 * @private
 */
$1.prototype.update_ = function () {
  React.render(
    <$2 />,
    this.getElement()
  );
};
"""
		self.populateViewWithGivenSnippet(view, snippet)

	def populateReactFile(self, view):
		snippet = """goog.provide('$2');

/** @lends {React.ReactComponent} */
$2Definition = {};

$2Definition.mixins = [];

/** @inheritDoc */
$2Definition.propTypes = {
};

/**
 * @suppress {globalThis}
 * @inheritDoc
 */
$2Definition.render = function () {
};

$2 = React.createClass($2Definition);
"""
		self.populateViewWithGivenSnippet(view, snippet)

	def populateViewWithGivenSnippet(self, view, snippet):
		edit = view.begin_edit()
		replacement = snippet.replace("$1", str(view.settings().get('closure_module_name')))
		template_text = replacement.replace("$2", str(view.settings().get('react_module_name')))
		view.insert(edit, 0, template_text)
		view.end_edit(edit)
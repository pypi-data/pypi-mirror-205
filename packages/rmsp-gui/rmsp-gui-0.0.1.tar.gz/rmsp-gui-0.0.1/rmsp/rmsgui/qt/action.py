# A list of RMS actions that require GUI dialogs 
from PyQt5.Qt import QFileDialog

from .dialog import RMSEntryDeletionConfirmationDialog
from .dialog import RMSLibraryDialog, RMSTemplateDialog

class RMSActionQT():
	def __init__(self, window, rms_interactor, rmspool_interactor, rmstemplatelib_interactor):
		self.window = window
		self.rms_interactor = rms_interactor
		self.rmspool_interactor = rmspool_interactor
		self.rmstemplatelib_interactor = rmstemplatelib_interactor
	
	def register_file(self):
		fn = QFileDialog.getOpenFileNames(self.window, "Register files")
		for f in fn[0]:
			self.rms_interactor.request("register_file", args=[f])
		
	def confirm_and_fetch_resource_content(self):
		pass
	
	def confirm_and_delete(self, rmsids):
		dlg = RMSEntryDeletionConfirmationDialog(rmsids, self.window)
		if dlg.exec():
			self.rms_interactor.request("delete", args=[*rmsids])
		else:
			pass
	
	def run_library_selection(self):
		dlg = RMSLibraryDialog(self.rmstemplatelib_interactor, self, self.window)
		dlg.exec()
		
	def edit_and_run_template(self, bookname, chaptername, bookmark):
		dlg = RMSTemplateDialog(self.rmstemplatelib_interactor, bookname, chaptername, bookmark, self.window)
		if dlg.exec():
			arguments = dlg.templateWidget.getBoundArguments()
			self._run_template(bookname, chaptername, bookmark, arguments)
			
			

	def _run_template(self, bookname, chaptername, bookmark, ba):
		request_result = self.rmstemplatelib_interactor.request("run", [bookname, chaptername, bookmark],
											kwargs={"args":ba.args, "kwargs":ba.kwargs},
											callback=self._run_template_callback)
	def _run_template_callback(self, request_result):
		job = request_result.result
		self.rmstemplatelib_interactor.request("execute_builder", args=[], kwargs={})
# 		execute_builder
		rmsids = [u.get_full_id() for u in job.unruntasks]
		task_io = self.rms_interactor.execute("find_connected_nodes", args=[rmsids], kwargs={"distance":1})
		self.window.fc.add_nodes(rmsids + task_io)
		self.window.fc.auto_order()
	

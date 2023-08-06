from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import datetime
from .widget import RMSTemplateWidget, RMSBookWidget

class RMSEntryEditDialog(QDialog):
	'''
	The RMS Entry Dialog that allows people to edit the node's description, tags and info.
	
	Note that UnrunTask is handled separately.
	'''
	def __init__(self, rmsobj, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Edit RMS Entry")
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self._updated_fields = {}
		self.layout = QGridLayout()
		
		self.layout.addWidget(QLabel(rmsobj.get_type().name + ": " + rmsobj.get_id()), 0, 0, 1, 3)
		self.layout.addWidget(QLabel("Description: "), 1, 0)
		self.description_box = QTextEdit()
		self.description_checkbox = QCheckBox("isNone")
		if rmsobj.description is None:
			self.description_checkbox.setCheckState(Qt.Checked)
			self.description_box.setEnabled(False)
		else:
			self.description_checkbox.setCheckState(Qt.Unchecked)
			self.description_box.setEnabled(True)
			self.description_box.setText(rmsobj.description)
		self.description_checkbox.stateChanged.connect(self.onDescriptionStateChange)
		self.description_box.textChanged.connect(self.onDescriptionTextChange)
		self.layout.addWidget(self.description_box, 1, 1)
		self.layout.addWidget(self.description_checkbox, 1, 2)
		self.layout.addWidget(self.buttonBox, 2, 0)
		self.setLayout(self.layout)
	def onDescriptionStateChange(self, state):
		self.description_box.setEnabled(False if state == Qt.Checked else True)
		self._updated_fields["description"] = None if self.description_checkbox.checkState == Qt.Checked else ("'" + self.description_box.toPlainText() + "'")
		
	def onDescriptionTextChange(self):
		self._updated_fields["description"] = None if self.description_checkbox.checkState == Qt.Checked else ("'" + self.description_box.toPlainText() + "'")
	
	@property
	def updated_fields(self):
		return self._updated_fields
	
# class RMSUnrunTaskEditDialog(QDialog):
# 	'''
# 	The RMS Entry Dialog that allows people to edit the node's description, tags and info.
# 	
# 	Note that UnrunTask is handled separately.
# 	'''
# 	def __init__(self, rmscontroller, rmsobj, parent=None):
# 		super().__init__(parent=parent)
# 		self.setWindowTitle("Edit RMS Unrun Task")
# 		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
# 		self.buttonBox = QDialogButtonBox(QBtn)
# 		self.buttonBox.accepted.connect(self.accept)
# 		self.buttonBox.rejected.connect(self.reject)
# 		self.layout = QVBoxLayout()
# 		self.editWidget = RMSUnrunTaskEditWidget(rmscontroller, rmsobj)
# 		self.layout.addWidget(self.editWidget)
# 		self.layout.addWidget(self.buttonBox)
# 		self.setLayout(self.layout)
# 	def getArguments(self):
# 		return self.editWidget.getArguments()	
# 	
# 	
# class RMSUnrunTaskInputArgumentSelectionDialog(QDialog):
# 	'''
# 	Allow the user the select what argument the resource / fileresource points at
# 	'''
# 	def __init__(self, unruntask, parent=None):
# 		super().__init__(parent=parent)
# 		self.unruntask = unruntask
# 		self.setWindowTitle("Confirm Fetching RMS Entry Content")
# 		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
# 		self.buttonBox = QDialogButtonBox(QBtn)
# 		self.buttonBox.accepted.connect(self.accept)
# 		self.buttonBox.rejected.connect(self.reject)
# 		self.ql = QListWidget()
# 		self.ql.setSelectionMode(QAbstractItemView.SingleSelection)
# 		for p in unruntask.ba.signature.parameters.keys():
# 			item = QListWidgetItem(self.ql)
# 			item.setData(Qt.DisplayRole, p)
# 			if p in unruntask.ba.arguments:
# 				item.setForeground(Qt.black)
# 				item.setData(Qt.ToolTipRole, str(unruntask.ba.arguments[p])) # May need to update resource
# 			else:
# 				item.setForeground(Qt.red)
# 				item.setData(Qt.ToolTipRole, "[Empty]")
# 		self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
# 		self.ql.itemSelectionChanged.connect(self.customItemChange)
# 		self.statusLabel = QLabel()
# 		self.customItemChange()
# 		# Layout
# 		self.layout = QVBoxLayout()
# 		self.layout.addWidget(QLabel("Select the input argument you want to link your data to"))
# 		self.layout.addWidget(self.ql)
# 		self.layout.addWidget(self.statusLabel)
# 		self.layout.addWidget(self.buttonBox)
# 		self.setLayout(self.layout)
# 	
# 	def customItemChange(self):
# 		self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(self.ql.selectedItems()) == 1)
# 		if len(self.ql.selectedItems()) == 1:
# 			p = self.ql.selectedItems()[0].data(Qt.DisplayRole)
# 			if self.unruntask.ba.signature.parameters[p].kind == inspect.Parameter.VAR_POSITIONAL:
# 				self.statusLabel.setText(f"Your resource will be appended to {p}")
# 			elif self.unruntask.ba.signature.parameters[p].kind == inspect.Parameter.VAR_KEYWORD:
# 				self.statusLabel.setText(f"Your will be asked to input the key to your resource and added to {p}")
# 			else:
# 				self.statusLabel.setText(f"Your resource will be assigned to {p}")
# 		else:
# 			self.statusLabel.setText("You must select one argument to assign the resource")
# 	@property
# 	def selected_argument_name(self):
# 		if len(self.ql.selectedItems()) == 1:
# 			return self.ql.selectedItems()[0].data(Qt.DisplayRole)
# 		else:
# 			return None
# 	@property
# 	def key(self):
# 		return None
# 	
# class RMSResourceSelectionDialog(QDialog):
# 	def __init__(self, rmscontroller, parent, rmstypes={"Resource", "File Resource", "Task", "Pipe"}):
# 		super().__init__(parent=parent)
# 		self.setWindowTitle("Select RMS Resource")
# 		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
# 		self.buttonBox = QDialogButtonBox(QBtn)
# 		self.buttonBox.accepted.connect(self.accept)
# 		self.buttonBox.rejected.connect(self.reject)
# 		self.layout = QVBoxLayout()
# 		self.searchWidget = RMSSearchWidget(rmscontroller, rmstypes=rmstypes)
# 		self.searchWidget.setVisible(True)
# 		self.layout.addWidget(self.searchWidget)
# 		self.layout.addWidget(self.buttonBox)
# 		self.setLayout(self.layout)
# 	
# 	def selected_rmsobjs(self):
# 		return self.searchWidget.selected_rmsobjs()
# 	
class RMSEntryDeletionConfirmationDialog(QDialog):
	'''
	The RMS Entry Dialog that allows people to delete the nodes
	'''
	def __init__(self, rmsids, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Confirm RMS Entry Deletion")
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.layout = QGridLayout()
		self.layout.addWidget(QLabel("Are you sure to delete the following RMS Entry?"), 0, 0)
		self.layout.addWidget(QLabel("\n".join([str(rmsid) for rmsid in rmsids])), 1, 0)
		self.layout.addWidget(self.buttonBox, 2, 0)
		self.setLayout(self.layout)


class RMSEntryFetchContentConfirmationDialog(QDialog):
	'''
	'''
	def __init__(self, resources, required_tasks, required_resources, parent=None):
		super().__init__(parent=parent)
			
		rmsids = [rmsobj.get_full_id() for rmsobj in resources]
		self.setWindowTitle("Confirm Fetching RMS Entry Content")
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.layout = QGridLayout()
		self.layout.addWidget(QLabel("Are you sure to fetch the resources?"), 0, 0)
		
		info = {"No. of Tasks": str(len(required_tasks)),
				"No. of Resources": str(len(required_resources)),
				"Estimated time": str(sum((task.run_time for task in required_tasks), datetime.timedelta()))
			   }
		self.layout.addWidget(QLabel("\n".join(list(map(lambda i: f"{i[0]}: {i[1]}", info.items())))), 1, 0)
		self.layout.addWidget(self.buttonBox, 2, 0)
		self.setLayout(self.layout)

class RMSConfirmRunUnrunTaskDialog(QDialog):
	'''
	Allow the user the select what argument the resource / fileresource points at
	'''
	def __init__(self, unruntasks, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Confirm Running Unrun Task")
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.ql = QListWidget()
		self.ql.setSelectionMode(QAbstractItemView.NoSelection)
		for unruntask in unruntasks:
			item = QListWidgetItem(self.ql)
			item.setData(Qt.DisplayRole, unruntask.uid)
		
		# Layout
		self.layout = QVBoxLayout()
		self.layout.addWidget(QLabel(f"Are you sure to run the following {len(unruntasks)} unrun tasks?"))
		self.layout.addWidget(self.ql)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)


class RMSEntryFetchContentWarningDialog(QDialog):
	'''
	'''
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setWindowTitle("Warning: Fetching RMS Entry Content")
		QBtn = QDialogButtonBox.Ok
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.layout = QVBoxLayout()
		self.layout.addWidget(QLabel("No content needs to be fetched"))
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)

class RMSLibraryDialog(QDialog):
	# Wrapper for switching versions
	update_library_signal = pyqtSignal(object)	
	
	def __init__(self, rmstemplatelib_interactor, rms_actioner, parent=None):
		super().__init__(parent=parent)
		self.rms_actioner = rms_actioner
		self.rmstemplatelib_interactor = rmstemplatelib_interactor
		self.setWindowTitle("RMS Book Selection")
		
		self.update_library_signal.connect(self.update_library)
		
		self.bookwidgets = {}
		self.layout = QHBoxLayout()
		self.manifest_panel = QListWidget()
		self.manifest_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.manifest_panel.setMinimumSize(100, 100)
		self.manifest_panel.itemSelectionChanged.connect(self.update_widget)
		rmstemplatelib_interactor.request("get_books", callback=lambda request_result: self.update_library_signal.emit(request_result.result))
		self.layout.addWidget(self.manifest_panel)
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel	
		self.setLayout(self.layout)
		
	def update_library(self, rmsbooks):
		for bookname, book in rmsbooks.items():
			item = QListWidgetItem(self.manifest_panel)
			item.setData(Qt.UserRole, book)
			item.setData(Qt.DisplayRole, bookname)
		
	def update_widget(self):
		for k, v in self.bookwidgets.items():
			v.hide()
		for i in self.manifest_panel.selectedItems():
			bookname = i.data(Qt.DisplayRole)
			book = i.data(Qt.UserRole)
			if bookname not in self.bookwidgets:
				widget = RMSBookWidget(self.rms_actioner, bookname, book)
				widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
				self.bookwidgets[bookname] = widget
				self.layout.addWidget(widget)
			self.bookwidgets[bookname].show()
			
class RMSTemplateDialog(QDialog):
	'''
	The RMS Entry Dialog that allows people to edit the node's description, tags and info.

	Note that UnrunTask is handled separately.
	'''
	def __init__(self, rmstemplatelib_interactor, bookname, chaptername, bookmark, parent=None):
		super().__init__(parent=parent)
		self.bookname = bookname
		self.chaptername = chaptername
		self.bookmark = bookmark
		
		self.setWindowTitle("Edit RMS Unrun Task")
		QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		self.buttonBox = QDialogButtonBox()
		
		self.buttonBox.addButton(QDialogButtonBox.Ok)
		self.buttonBox.addButton(QDialogButtonBox.Cancel)
		self.buttonBox.accepted.connect(self.confirm_template)
		self.buttonBox.rejected.connect(self.reject)
		self.layout = QVBoxLayout()
		self.templateWidget = RMSTemplateWidget(rmstemplatelib_interactor, bookname, chaptername, bookmark)
		self.layout.addWidget(self.templateWidget)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)
	
	def confirm_template(self):
		if not self.templateWidget.checkArguments():
			self.templateWidget.addArgumentCheckHints()
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Warning)
			msgBox.setText("Please fix all parameters first.")
			msgBox.setWindowTitle("Message")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		else:
			self.templateWidget.close_fig()
			self.accept()
	def closeEvent(self, event):
		self.templateWidget.close_fig()
		event.accept()
			
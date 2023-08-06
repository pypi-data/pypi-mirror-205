

import os
import datetime
import uuid
import threading
from dataclasses import dataclass
import inspect
import json
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas#FigureCanvas

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from rmsp.rmscore import RMSEntry, RMSEntryType, Resource, FileResource, Pipe
from rmsp.rmscore import _get_func_ba
from rmsp.rmstemplate import InputFileType, OutputFileType



class RMSEntryDescriptionFormatter():
	'''
	A class that formats RMS Entries into description text. 
	'''
	def __init__(self, rms_interactor):
		self.rms_interactor = rms_interactor
		
	def format_rmsobjs(self, rmsids):
		if len(rmsids) == 1:
			return self.format_rmsobj(list(rmsids)[0])
		return f"{len(rmsids)} nodes selected."
# 		rmsobjs = [self.rms_interactor.get(rmsid) for rmsid in rmsids if self.rms.has(rmsid)]
# 		return f"{len(rmsobjs)} nodes selected.\n" + "[" + ", ".join([f"({str(rmsobj.get_type())}, \"{str(rmsobj.get_id())}\")" for rmsobj in rmsobjs]) + "]\n"
	
		
	def format_rmsobj(self, rmsid):
		'''
		Convert an RMS Entry into description text
		'''
		rmsobj = self.rms_interactor.execute("get", [rmsid]) 
		# RESOURCE
		if rmsobj.get_type() == RMSEntryType.RESOURCE:
			info = {}
			info["Description"] = str(rmsobj.description)
			if rmsobj.has_content:
				info["Type"] = str(rmsobj.content_type) + (" (Volatile)" if rmsobj.volatile else "")
			else:
				info["Type"] = "Content is not available"
			if len(rmsobj.info) > 0:
				info["Information"] = str(rmsobj.info)
		# FILE RESOURCE
		elif rmsobj.get_type() == RMSEntryType.FILERESOURCE:
			info = {"Name":os.path.basename(rmsobj.file_path), "Location":os.path.dirname(rmsobj.file_path)}
			if rmsobj.description is not None:
				info["Description"] = rmsobj.description
			if len(rmsobj.info) > 0:
				info["Information"] = str(rmsobj.info)
		# TASK
		elif rmsobj.get_type() == RMSEntryType.TASK:
			pipe = self.rms_interactor.execute("get", [(RMSEntryType.PIPE, rmsobj.pid)])
			info = {"Pipe name": pipe.func_name + " (" + rmsobj.pid + ")", 
					"Parameters": self.create_task_param_description(rmsobj, pipe),
					"Begin Time": str(rmsobj.begin_time),
					"End Time": str(rmsobj.end_time),
					"Duration": str(rmsobj.end_time - rmsobj.begin_time)}
			if "sourcecode" in pipe.info:
				info["Source code"] = "\n" + pipe.info["sourcecode"]
			if len(rmsobj.info) > 0:
				info["Information"] = str(rmsobj.info)
		# PIPE
		elif rmsobj.get_type() == RMSEntryType.PIPE:
			info = {"Pipe name": rmsobj.func_name}
			if "sourcecode" in rmsobj.info:
				info["Source code"] = "\n" + rmsobj.info["sourcecode"]
			
		# UNRUNTASK
		elif rmsobj.get_type() == RMSEntryType.UNRUNTASK:
			pipe = self.rms_interactor.execute("get", [(RMSEntryType.PIPE, rmsobj.pid)])
			info = {"Pipe name": self.pipe.func_name + " (" + rmsobj.pid + ")", 
					"Parameters": "".join("\n\t" + k + ": " + self.convert_value(v, rmsobj.ba.signature.parameters[k].kind) for k,v in rmsobj.ba.arguments.items())}
		elif rmsobj.get_type() == RMSEntryType.VIRTUALRESOURCE:
			info = {}
		return ("RMS Database - " + self.rms_interactor.execute("get_dbid") + "\n"
			+ rmsobj.get_type().name + " - " + rmsobj.get_id()
			+ "\n============================================\n"
			+ "\n".join(map(lambda i: i[0] + ": " + i[1], info.items())))

	def convert_value(self, v, kind=None):
		if kind is not None and kind == inspect.Parameter.VAR_POSITIONAL:
			return "[" + ", ".join([self.convert_value(arg) for arg in v]) + "]"
		if kind is not None and kind == inspect.Parameter.VAR_KEYWORD: # Untested
			return "{" + ", ".join([k + ": " + self.convert_value(arg) for k, arg in v.items()]) + "}"
		if isinstance(v, Resource):
			return "(Resource) " + v.rid
		elif isinstance(v, FileResource):
			return "(File) " + v.file_path + " (" + v.fid + ")"
		elif isinstance(v, Pipe):
			return "(Pipe) " + v.func_name + " (" + v.pid + ")"
		else:
			return str(v)
	def create_task_param_description(self, task, pipe):
		
		args = task.args
		kwargs = task.kwargs
		ba = _get_func_ba(pipe.func, args, kwargs, partial=False)
		sig = ba.signature
		return "".join("\n\t" + k + ": " + self.convert_value(v, sig.parameters[k].kind) for k,v in ba.arguments.items())

class DescriptionWidget(QWidget):
	'''
	The description widget that contains the description part and a tab of analyses
	'''
	update_signal = pyqtSignal(object)
	
	def __init__(self, rmsDescriptionFormatter, analysis_factory, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rmsDescriptionFormatter = rmsDescriptionFormatter
		self.analysis_factory = analysis_factory
		self.initUI()
		self.update_signal.connect(self._update)
	
	def initUI(self):
		self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                         QSizePolicy.MinimumExpanding))

		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.descriptionArea = QTextEdit()
		self.analysisTab = QTabWidget()
		
		splitter = QSplitter(Qt.Vertical)
		splitter.addWidget(self.descriptionArea)
		splitter.addWidget(self.analysisTab)
		splitter.setSizes([100,100])
		self.layout.addWidget(splitter)
		# update description area tab dist
		font = self.descriptionArea.font()
		fontMetrics = QFontMetricsF(font)
		spaceWidth = fontMetrics.width(' ')
		self.descriptionArea.setTabStopDistance(spaceWidth * 4)
		
		
		# Call update
		self.update([])
		
	def sizeHint(self):
		return QSize(400,400)

	
	def onSelectionChange(self, old_rmsids, rmsids):
		self.update(rmsids)
		
	def update(self, rmsids):
		self.update_signal.emit(rmsids)
		
	def _update(self, rmsids):
		if len(rmsids) == 0:
			description = ""
# 		elif len(rmsids) == 1:
# 			description = self.rmsDescriptionFormatter.format_rmsobj(next(iter(rmsids)))
# 		else:
		else:
			description =  self.rmsDescriptionFormatter.format_rmsobjs(rmsids)
		self.descriptionArea.setText(description)
		
		
		self.analysisTab.clear()
		analysis_widgets = self.analysis_factory.find_analysis_widgets(rmsids)
		for tab_name, widget in analysis_widgets.items():
			self.analysisTab.addTab(widget, tab_name)

class RMSSearchResult():
	def __init__(self, name, rmsobj, description_text):
		self.name = name
		self.rmsobj = rmsobj
		self.description_text = description_text

class RMSSearchListWidget(QListWidget):
	# mimeTypes?
	def mimeData(self, items):
		rmsids = [i.data(Qt.UserRole) for i in items]
		d = QMimeData()
		d.setData("application/json", QByteArray.fromHex(json.dumps(rmsids).encode().hex().encode()))
		return d

class RMSSearchResultFormatter():
	'''
	A class to format the RMSEntry into search result
	'''
	def __init__(self, rms_interactor):
		self.rms_interactor = rms_interactor
		pass
	def format_rmsobj(self, rmsobj):
		rmsid = rmsobj.get_full_id()
		if rmsid[0] == RMSEntryType.RESOURCE:
			return RMSSearchResult(rmsobj.rid, rmsobj, "")
		if rmsid[0] == RMSEntryType.FILERESOURCE:
			return RMSSearchResult(os.path.basename(rmsobj.file_path) + " (" + rmsobj.file_path + ")", rmsobj, rmsobj.description)
		if rmsid[0] == RMSEntryType.TASK:
			pipename = self.rms_interactor.execute("get", [(RMSEntryType.PIPE, rmsobj.pid)]).func_name 
			return RMSSearchResult(rmsobj.tid + "(" + pipename + ")", rmsobj, "")
		if rmsid[0] == RMSEntryType.PIPE:
			return RMSSearchResult(rmsobj.func_name, rmsobj, "")
		else:
			raise Exception()

	def format_rmsobjs(self, rmsobjs):
		#return f"{len(rmsobjs)} nodes selected.\n" + "[" + ", ".join([f"({str(rmsobj.get_type())}, \"{str(rmsobj.get_id())}\")" for rmsobj in rmsobjs]) + "]\n"
		return [self.format_rmsobj(rmsobj) for rmsobj in rmsobjs]

class RMSSearchWidget(QWidget):
	update_result_panel_signal = pyqtSignal(object, object)
	
	def __init__(self, rms_interactor, *args, rmstypes={"Resource", "File Resource", "Task", "Pipe"}, **kwargs):
		super().__init__(*args, **kwargs)
		self.search_result_formatter = RMSSearchResultFormatter(rms_interactor)
		self.rms_interactor = rms_interactor
		
		self.saved_search_text = {"Pipe":"", "Task":"", "Resource":"", "File Resource":""}
		
		# The lock makes sure that only one request is updating the panel
		# Only the last request will be able to update the panel
		self.updateLock = threading.Lock()
		
		self.initSignal()
		self.initUI()
		
	def initSignal(self):
		self.update_result_panel_signal.connect(self.update_result_panel)
		
	def initUI(self):
		self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                                 QSizePolicy.MinimumExpanding))
		self.selection_contents = self
		self.layout = QGridLayout(self.selection_contents)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		
		
		self.selection_combobox = QComboBox(self.selection_contents)
		self.selection_combobox.addItems(["Resource", "File Resource", "Task", "Pipe"])
		self.selection_combobox.currentIndexChanged.connect(self.on_selection_change)
		self.layout.addWidget(self.selection_combobox)
		
		self.selection_search = QLineEdit(self.selection_contents)
		self.layout.addWidget(self.selection_search)
		self.selection_search.textEdited.connect(self.on_selection_search_text_edited)

		self.result_panel = RMSSearchListWidget(self.selection_contents)
		self.layout.addWidget(self.result_panel)
		self.result_panel.setDragDropMode(QAbstractItemView.DragDrop)
		self.result_panel.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.result_panel.setAcceptDrops(False)
		self.result_panel.setContextMenuPolicy(Qt.ActionsContextMenu)
# 		self.result_panel.selectionChanged()
		copyPathAction = QAction("Copy path", self)
		copyPathAction.triggered.connect(self.copy_path_method)
		self.result_panel.addAction(QAction("Empty 1", self))
		self.result_panel.addAction(QAction("Empty 2", self))
		self.result_panel.addAction(copyPathAction)
		
		# Set default combobox item to index 1
		self.selection_combobox.setCurrentIndex(1)
	def sizeHint(self):
		return QSize(100,100)
		
		
# 		self.result_panel.itemDoubleClicked.connect(lambda item: self.view_contents.nodeEditDialog(item.data(Qt.UserRole)))
	def copy_path_method(self):
		if self.selection_combobox.currentText() == "File Resource":
			fids = [item.data(Qt.UserRole) for item in self.result_panel.selectedItems()]
			if len(fids) == 0:
				return
			elif len(fids) == 1:
				fp = self.rms_interactor.execute("get", [fids[0]]).file_path
				clipboard = QApplication.clipboard()
				clipboard.setText(repr(fp))
			else:
				fps_str = "[" + ", ".join([repr(self.rms_interactor.execute("get", [fid]).file_path) for fid in fids]) + "]"
				clipboard = QApplication.clipboard()
				clipboard.setText(fps_str)

	def on_selection_change(self, i):
		self.selection_search.setText(self.saved_search_text[self.selection_combobox.currentText()])
		self._request_search_db(self.selection_search.text())
		
	def on_selection_search_text_edited(self, t):
		self._request_search_db(t)
		self.saved_search_text[self.selection_combobox.currentText()] = t
		
	def _request_search_db(self, search_text):
		self.updateLock.acquire()
		search_request_id = uuid.uuid4().hex
		self.current_search_request_id = search_request_id
		self.updateLock.release()
		
		#listener = types.SimpleNamespace(onRequestUpdate=lambda request_result: self.update_result_panel_signal.emit(search_request_id, request_result.result))
		callback = lambda request_result: self.update_result_panel_signal.emit(search_request_id, request_result.result)
		if self.selection_combobox.currentText() == "Resource":
			self.rms_interactor.request("search_db", ["r", search_text], 
									callback=callback)
		elif self.selection_combobox.currentText() == "File Resource":
			self.rms_interactor.request("search_db", ["f", search_text], callback=callback)
		elif self.selection_combobox.currentText() == "Task":
			self.rms_interactor.request("search_db", ["t", search_text], callback=callback)
		elif self.selection_combobox.currentText() == "Pipe":
			self.rms_interactor.request("search_db", ["p", search_text], callback=callback)
		else:
			raise Exception()
		
	def update_result_panel(self, search_request_id, raw_search_results):
		self.updateLock.acquire()
		if search_request_id == self.current_search_request_id:
			self.result_panel.clear()
			for search_result in self.search_result_formatter.format_rmsobjs(raw_search_results):
				item = QListWidgetItem(self.result_panel)
				item.setData(Qt.ToolTipRole, search_result.description_text)
				item.setData(Qt.UserRole, search_result.rmsobj.get_full_id())
				item.setData(Qt.DisplayRole, search_result.name)
		self.updateLock.release()
			
	def selected_rmsobjs(self):
		return [item.data(Qt.UserRole) for item in self.result_panel.selectedItems()]

class RMSStatWidget(QWidget):
	
	def __init__(self, rms_interactor, rmspool_interactor, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rms_interactor = rms_interactor
		self.rmspool_interactor = rmspool_interactor
		self.timer=QTimer(self)
		self.timer.timeout.connect(self.update_stat)
		self.initUI()

	def initUI(self):
		self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,
                                         QSizePolicy.Minimum))

		self.layout = QGridLayout(self)
		self.setLayout(self.layout)
		row = 0
		col = 0
		self.layout.addWidget(QLabel("Pending tasks"), row, col)
		self.pending_tasks_text = QLabel("")
		self.layout.addWidget(self.pending_tasks_text, row, col+1)
		row += 1
		
		self.layout.addWidget(QLabel("Running tasks"), row, col)
		self.running_tasks_text = QLabel("")
		self.layout.addWidget(self.running_tasks_text, row, col+1)
		row += 1
		
		self.layout.addWidget(QLabel("Finished tasks"), row, col)
		self.finished_tasks_text = QLabel("")
		self.layout.addWidget(self.finished_tasks_text, row, col+1)
		row += 1
		
		self.layout.addWidget(QLabel("Error tasks"), row, col)
		self.error_tasks_text = QLabel("")
		self.layout.addWidget(self.error_tasks_text, row, col+1)
		row += 1
		
		self.layout.addWidget(QLabel("Last updated"), row, col)
		self.last_updated_text = QLabel("")
		self.layout.addWidget(self.last_updated_text, row, col+1)
		row += 1
		
		col = 2
		row = 0
		self.layout.addWidget(QLabel("RMS Task"), row, col)
		self.task_number_text = QLabel("")
		self.layout.addWidget(self.task_number_text, row, col+1)
		row += 1
		self.layout.addWidget(QLabel("RMS Resource"), row, col)
		self.resource_number_text = QLabel("")
		self.layout.addWidget(self.resource_number_text, row, col+1)
		row += 1
		self.layout.addWidget(QLabel("RMS FileResource"), row, col)
		self.fileresource_number_text = QLabel("")
		self.layout.addWidget(self.fileresource_number_text, row, col+1)
		row += 1
		self.layout.addWidget(QLabel("RMS Pipe"), row, col)
		self.pipe_number_text = QLabel("")
		self.layout.addWidget(self.pipe_number_text, row, col+1)
		row += 1

		col = 4
		row = 0
		self.layout.addWidget(QLabel("CPU Load"), row, col)
		self.cpu_load_text = QLabel("")
		self.layout.addWidget(self.cpu_load_text, row, col+1)
		row += 1
		self.layout.addWidget(QLabel("Memory usage"), row, col)
		self.ram_text = QLabel("")
		self.layout.addWidget(self.ram_text, row, col+1)
		row += 1
# 		self.layout.addWidget(QLabel("RMS FileResource"), row, col)
# 		self.fileresource_number_text = QLabel("")
# 		self.layout.addWidget(self.fileresource_number_text, row, col+1)
# 		row += 1
# 		self.layout.addWidget(QLabel("RMS Pipe"), row, col)
# 		self.pipe_number_text = QLabel("")
# 		self.layout.addWidget(self.pipe_number_text, row, col+1)
# 		row += 1
		
		##################################################
# 		self.update_btn = QPushButton("Update")
# 		self.update_btn.clicked.connect(self.update_stat)
# 		self.layout.addWidget(self.update_btn, 5, 0, 1, 6)
		self.cb = QCheckBox("Auto-update")
		self.cb.stateChanged.connect(self.btnstate)
		self.cb.setChecked(True)
		self.layout.addWidget(self.cb, 4, 2, 1, 4)
		row += 1
		
	def btnstate(self):
		if self.cb.isChecked():
			self.update_stat()
			self.timer.start(10000)
		else:
			self.timer.stop()
	def update_stat(self):
		self.pending_tasks_text.setText(str(self.rmspool_interactor.execute("stat", ["pending"], {})))
		self.running_tasks_text.setText(str(self.rmspool_interactor.execute("stat", ["running"], {})))
		self.finished_tasks_text.setText(str(self.rmspool_interactor.execute("stat", ["finished"], {})))
		self.error_tasks_text.setText(str(self.rmspool_interactor.execute("stat", ["error"], {})))
		
		self.task_number_text.setText(str(self.rms_interactor.execute("stat", ["t"], {})))
		self.fileresource_number_text.setText(str(self.rms_interactor.execute("stat", ["f"], {})))
		self.resource_number_text.setText(str(self.rms_interactor.execute("stat", ["r"], {})))
		self.pipe_number_text.setText(str(self.rms_interactor.execute("stat", ["p"], {})))
		
		cpu = self.rmspool_interactor.execute("stat", ["cpu"], {})
		self.cpu_load_text.setText(f"{cpu*100:.1f}%")
		m = self.rmspool_interactor.execute("stat", ["memory"], {})
		self.ram_text.setText(f"{m*100:.1f}%")
		self.last_updated_text.setText(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


#######################################################################
@dataclass
class RMSTemplateInput:
	status: str
	namelabel: QLabel
	typelabel: QLabel
	textedit: QLineEdit
	rmsentry: RMSEntry
	widget: QWidget
@dataclass
class KeywordRMSTemplateInput(RMSTemplateInput):
	keytextedit: QLineEdit
@dataclass
class VarRMSTemplateInput:
	rmsinputs: dict
	layout: QLayout
	
def convert_to_bool(s):
	'''
	A method to parse string (case insensitive) to boolean according to the text meaning.
	
	| true, yes, t, y, 1 are all regarded as True
	| false, no, f, n, 0 are all regarded as False
	
	Note that boolean(s) has a different meaning.
	
	This function is usually used in argument parsing
	
	.. code-block:: python
	
		convert_to_bool("yes") # True
		
		convert_to_bool("NO") # False
		
		convert_to_bool("ambiguous") # Exception raised
		
	'''
	if s.lower() in ("true", "yes", "t", "y", "1"):
		return True
	elif s.lower() in ("false", "no", "f", "n", "0"):
		return False
	else:
		raise Exception("Unable to interpret boolean value from: " + s)

class RMSTemplateWidget(QWidget):
	def __init__(self, rmstemplatelib_interactor, bookname, chaptername, bookmark, description=None):
		super().__init__()
		self.rmstemplatelib_interactor = rmstemplatelib_interactor
		self.bookname = bookname
		self.chaptername = chaptername
		self.bookmark = bookmark
		self.func_signature = self.rmstemplatelib_interactor.execute("get_func_signature", [bookname, chaptername, bookmark])
		self.section = self.rmstemplatelib_interactor.execute("get_section", [bookname, chaptername, bookmark])
		self.doc = self.rmstemplatelib_interactor.execute("get_doc", [bookname, chaptername, bookmark])
		
		self.ba = self.func_signature.bind_partial()		
		self.ba.apply_defaults()
		self.rmsinputs = {}
		
		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.addArgumentCheckHints)
		self.timer2 = QTimer()
		self.timer2.setSingleShot(True)
		self.timer2.timeout.connect(self.simulate)
		self.initUI()
		
	def delayTextChanged(self):
		if not self.timer.isActive():
			self.timer.start(500)
		if not self.timer2.isActive():
			self.timer2.start(500)
	def createRowComponent(self, parent, display_paramname, anno):
		'''
		Create a row that contains the parameter label, a value box, 3 buttons (Text, Selection, Delete) # Add one type box
		'''
		parameter_name_label = QLabel(display_paramname)
		parent.addWidget(parameter_name_label)
		parameter_type_label = QLabel(anno.__name__)
		parent.addWidget(parameter_type_label)
		parameter_box = QLineEdit()
		parameter_box.setPlaceholderText("(empty string)")
		parameter_box.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
		parameter_box.textChanged.connect(self.delayTextChanged)
		parent.addWidget(parameter_box)
		text_button = QPushButton()
		text_button.setText("T")
		text_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		parent.addWidget(text_button)
		rmsentry_button = QPushButton()
		rmsentry_button.setText("..")
		rmsentry_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		parent.addWidget(rmsentry_button)
		delete_button = QPushButton()
		delete_button.setText("-")
		delete_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		parent.addWidget(delete_button)
#		 delete_button.setMinimumSize(QSize)
		return parameter_name_label, parameter_type_label, parameter_box, text_button, rmsentry_button, delete_button
	def createKeywordRowComponent(self, parent, display_paramname):
		'''
		Similar to createRowComponent, but also create a keyword box in addition
		'''
		
		parameter_name_label = QLabel(display_paramname)
		parent.addWidget(parameter_name_label)
		keyword_box = QLineEdit()
		parent.addWidget(keyword_box)
		parameter_box = QLineEdit()
		parent.addWidget(parameter_box)
		text_button = QPushButton()
		text_button.setText("T")
		parent.addWidget(text_button)
		rmsentry_button = QPushButton()
		rmsentry_button.setText("..")
		parent.addWidget(rmsentry_button)
		delete_button = QPushButton()
		delete_button.setText("-")
		parent.addWidget(delete_button)
		return keyword_box, parameter_box, text_button, rmsentry_button, delete_button

	def addRMSInputRow(self, parent, display_paramname, anno):
		'''
		Add the RMS input row created using createRowComponent
		'''
		widget = QWidget()
		layout = QHBoxLayout()
		widget.setLayout(layout)
		parent.addWidget(widget)
		namelabel, typelabel, parameter_box, text_button, rmsentry_button, delete_button = self.createRowComponent(layout, display_paramname, anno)
		return widget, layout, namelabel, typelabel, parameter_box, text_button, rmsentry_button, delete_button

	def addKeywordRMSInputRow(self, parent, display_paramname):
		'''
		Add the RMS input row created using createKeywordRowComponent
		'''
		widget = QWidget()
		layout = QHBoxLayout()
		widget.setLayout(layout)
		parent.addWidget(widget)
		keyword_box, parameter_box, text_button, rmsentry_button, delete_button = self.createKeywordRowComponent(layout, display_paramname)
		return widget, layout, keyword_box, parameter_box, text_button, rmsentry_button, delete_button

		
	def createRMSInput(self, widget, namelabel, typelabel, parameter_box, has_value, value=None):
		if has_value:
			if isinstance(value, RMSEntry):
				rmsinput = RMSTemplateInput("r", namelabel, typelabel, parameter_box, value, widget)
			else:
				rmsinput = RMSTemplateInput("t", namelabel, typelabel, parameter_box, None, widget)
				#parameter_box.setText(json.dumps(value))
				parameter_box.setText(str(value))
		else:
			rmsinput = RMSTemplateInput("n", namelabel, typelabel, parameter_box, None, widget)
		self.initialize_rmsinput(rmsinput)
		return rmsinput
	def createKeywordRMSInput(self, widget, keyword_box, parameter_box, key, has_value, value=None):
		if has_value:
			if isinstance(value, RMSEntry):
				rmsinput = KeywordRMSTemplateInput("r", parameter_box, value, widget, keyword_box)
			else:
				rmsinput = KeywordRMSTemplateInput("t", parameter_box, None, widget, keyword_box)
				#parameter_box.setText(json.dumps(value))
				parameter_box.setText(str(value))
		else:
			rmsinput = KeywordRMSTemplateInput("n", parameter_box, None, widget, keyword_box)
			keyword_box.setEnabled(False)
# 		keyword_box.setText(json.dumps(key))
		keyword_box.setText(str(key))
		self.initialize_rmsinput(rmsinput)
		return rmsinput
	
	
	def createNormalRMSInputSet(self, display_paramname, layout, has_value, value, anno):
		'''
		Add row components using addRMSInputRow, and link the components to functions 
		'''
		widget, layout, namelabel, typelabel, parameter_box, text_button, file_button, delete_button = self.addRMSInputRow(layout, display_paramname, anno)
		rmsinput = self.createRMSInput(widget, namelabel, typelabel, parameter_box, has_value, value)
# 		rmsentry_button.clicked.connect(lambda checked, rmsinput=rmsinput: self.selectRMSPrompt(rmsinput))
		if anno == InputFileType:
			file_button.clicked.connect(lambda checked, rmsinput=rmsinput: self.selectOpenFilePrompt(rmsinput))
		elif anno  == OutputFileType:
			file_button.clicked.connect(lambda checked, rmsinput=rmsinput: self.selectSaveFilePrompt(rmsinput))
		text_button.clicked.connect(lambda checked, rmsinput=rmsinput: self.useTextParameter(rmsinput))
		delete_button.clicked.connect(lambda checked, rmsinput=rmsinput: self.removeParameter(rmsinput))
		self.rmsinputs[display_paramname] = rmsinput
	def createPositionalRMSInputSet(self, parent_rmsinput, layout, has_value, value):
		'''
		Specifically designed to handle the var-positional parameters 
		'''
		widget, layout, parameter_box, text_button, rmsentry_button, delete_button = self.addRMSInputRow(layout, "-")
		rmsinput = self.createRMSInput(widget, parameter_box, has_value, value=value)
		rmsentry_button.clicked.connect(lambda checked, rmsinput=rmsinput, parent_rmsinput=parent_rmsinput: self.selectRMSPromptVarPositional(rmsinput, parent_rmsinput))
		text_button.clicked.connect(lambda checked, rmsinput=rmsinput, parent_rmsinput=parent_rmsinput: self.useTextParameterVarPositional(rmsinput, parent_rmsinput))
		delete_button.clicked.connect(lambda checked, rmsinput=rmsinput, parent_rmsinput=parent_rmsinput: self.removeParameterVarPositional(rmsinput, parent_rmsinput))
		parent_rmsinput.rmsinputs.append(rmsinput)
	def createKeywordRMSInputSet(self, parent_rmsinput, layout, key, has_value, value):
		'''
		Specifically designed to handle the var-keyword parameters
		'''
		widget, layout, keyword_box, parameter_box, text_button, rmsentry_button, delete_button = self.addKeywordRMSInputRow(layout, "-")
		rmsinput = self.createKeywordRMSInput(widget, keyword_box, parameter_box, key, has_value, value=value) # Different from positional
		rmsentry_button.clicked.connect(lambda checked, rmsinput=rmsinput, parent_rmsinput=parent_rmsinput: self.selectRMSPromptVarKeyword(rmsinput, parent_rmsinput))
		text_button.clicked.connect(lambda checked, rmsinput=rmsinput, parent_rmsinput=parent_rmsinput: self.useTextParameterVarKeyword(rmsinput, parent_rmsinput))
		delete_button.clicked.connect(lambda checked, rmsinput=rmsinput, parent_rmsinput=parent_rmsinput: self.removeParameterVarKeyword(rmsinput, parent_rmsinput))
		parent_rmsinput.rmsinputs.append(rmsinput)
		
	def initialize_rmsinput(self, rmsinput):
		if rmsinput.status == "n":
			self.removeParameter(rmsinput)
		elif rmsinput.status == "t":
			self.useTextParameter(rmsinput)
		elif rmsinput.status == "r":
			self.selectRMSPrompt(rmsinput, prompt=False)
		else:
			raise Exception()
			
	def useTextParameter(self, rmsinput):
		if rmsinput.status != "t":
			rmsinput.textedit.setText("")
#			 rmsinput.textedit.setFocusPolicy(Qt.StrongFocus)
#			 rmsinput.textedit.setFocus(Qt.OtherFocusReason)
			QTimer.singleShot(0, lambda rmsinput=rmsinput: rmsinput.textedit.setFocus(Qt.OtherFocusReason))
		rmsinput.textedit.palette().setColor(QPalette.Base, Qt.red)
		rmsinput.textedit.setEnabled(True)
		rmsinput.status = "t"
	def selectOpenFilePrompt(self, rmsinput, prompt=True):
		if prompt:
			f = QFileDialog.getOpenFileName()
			if f[0] != '':
				print(f[0])
				rmsinput.textedit.setEnabled(True)
				rmsinput.textedit.setText(f[0])
				rmsinput.textedit.palette().setColor(QPalette.Base, Qt.red)
				
				rmsinput.status = "t"
	def selectSaveFilePrompt(self, rmsinput, prompt=True):
		if prompt:
			f = QFileDialog.getSaveFileName()
			if f[0] != '':
				print(f[0])
				rmsinput.textedit.setEnabled(True)
				rmsinput.textedit.setText(f[0])
				rmsinput.textedit.palette().setColor(QPalette.Base, Qt.red)
				rmsinput.status = "t"
	def removeParameter(self, rmsinput):
		rmsinput.textedit.setText("No parameter value")
		rmsinput.textedit.palette().setColor(QPalette.Base, Qt.red)
		rmsinput.textedit.setEnabled(False)
		rmsinput.status = "n"

	def useTextParameterVarPositional(self, rmsinput, parent_rmsinput):
		if rmsinput.status == "n":
			self.createPositionalRMSInputSet(parent_rmsinput, parent_rmsinput.layout, False, None)
		self.useTextParameter(rmsinput)
		
	def selectRMSPromptVarPositional(self, rmsinput, parent_rmsinput):
		oldrmsinputstatus = rmsinput.status
		self.selectRMSPrompt(rmsinput)
		if rmsinput.status == "r":
			if oldrmsinputstatus == "n":
				self.createPositionalRMSInputSet(parent_rmsinput, parent_rmsinput.layout, False, None)
		
	def removeParameterVarPositional(self, rmsinput, parent_rmsinput):
		if rmsinput.status != "n":
			parent_rmsinput.rmsinputs.remove(rmsinput)
			rmsinput.widget.deleteLater()

	def useTextParameterVarKeyword(self, rmsinput, parent_rmsinput):
		if rmsinput.status == "n":
			self.createKeywordRMSInputSet(parent_rmsinput, parent_rmsinput.layout, "", False, None)
		rmsinput.keytextedit.setEnabled(True)
		self.useTextParameter(rmsinput)
		
	def selectRMSPromptVarKeyword(self, rmsinput, parent_rmsinput):
		oldrmsinputstatus = rmsinput.status
		self.selectRMSPrompt(rmsinput)
		if rmsinput.status == "r":
			rmsinput.keytextedit.setEnabled(True)
			if oldrmsinputstatus == "n":
				self.createKeywordRMSInputSet(parent_rmsinput, parent_rmsinput.layout, "", False, None)
		
	def removeParameterVarKeyword(self, rmsinput, parent_rmsinput):
		if rmsinput.status != "n":
			parent_rmsinput.rmsinputs.remove(rmsinput)
			rmsinput.widget.deleteLater()
		

	def initUI(self):
		''' 
		The UI is 
		Part 1: Description
		Part 2: Pane
		2.1 argument
		2.2 var positional pane
		2.3 var keyword pane
		
		'''
		ba = self.ba
# 		ba.bind_partial()
# 		ba.apply_defaults()
		s = self.func_signature

		uiPane = QVBoxLayout()
		self.setLayout(uiPane)

		

		if self.doc is not None:
			docstringbox = QTextEdit()
			if self.doc["type"] == "html":
				docstringbox.setHtml(self.doc["content"])
			docstringbox.setReadOnly(True)
		else:
# 			description_str = ""
# 			description_str += self.func_info["name"] + "\n"
# 			if "doc" in self.func_info:
# 				description_str += self.func_info["doc"] 
			description_str = self.section["title"] + "\n" + self.section["description"]
			docstringbox = QPlainTextEdit(description_str)
			docstringbox.setReadOnly(True)
# 		uiPane.addWidget(docstringbox)
			
# 		uiPane.addWidget(QLabel(f"Edit the parameters for function {self.section['title']}"))
		paramScrollArea = QScrollArea()
# 		uiPane.addWidget(paramScrollArea)

		paramScrollArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
		paramScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);
		paramScrollArea.setWidgetResizable(True);
		paramScrollAreaWidget = QWidget()
		paramScrollArea.setWidget(paramScrollAreaWidget)
		pane = QVBoxLayout(paramScrollAreaWidget)
		
		fast_load_widget = QWidget()
		layout = QHBoxLayout()
		fast_load_widget.setLayout(QHBoxLayout())
		
		self.load_param_text = QLineEdit()
		self.load_param_text.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
		load_param_button = QPushButton("Load")
		save_param_button = QPushButton("Save")
# 		layout.addWidget(self.load_param_text)
# 		layout.addWidget(load_param_button)
		load_param_button.clicked.connect(lambda checked: self.load_param())
		save_param_button.clicked.connect(lambda checked: self.save_param())
		pane.addWidget(self.load_param_text)
		pane.addWidget(load_param_button)
		pane.addWidget(save_param_button)
# 		pane.addWidget(fast_load_widget)

		for p, parameter in s.parameters.items():
# 			if p == "rms":
# 				continue
			if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
				raise Exception()
			if parameter.kind == inspect.Parameter.VAR_KEYWORD:
				raise Exception()
			if parameter.annotation == inspect._empty:
				raise Exception()
			self.createNormalRMSInputSet(p, pane, p in ba.arguments, value=ba.arguments[p] if p in ba.arguments else None, anno=parameter.annotation)

		splitter_tb = QSplitter(Qt.Vertical)
		splitter_tb.addWidget(docstringbox)
		splitter_tb.addWidget(paramScrollArea)
		splitter_tb.setSizes([100,200])
			
		self.tsw = TemplateSimulatorFlowWidget()
		splitter_lr = QSplitter(Qt.Horizontal)
		splitter_lr.addWidget(splitter_tb)
		splitter_lr.addWidget(self.tsw)
		splitter_lr.setSizes([500,500])
		uiPane.addWidget(splitter_lr)
		
		self.simulate()
# 			if parameter.annotation == typing.List:
# 				pane.addWidget(QLabel(f"{p} - VAR_POSITIONAL"))
# 				scrollArea = QScrollArea()
# 				scrollArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
# 				scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);
# 				scrollArea.setWidgetResizable(True)
# 				scrollWidget = QWidget()
# 				scrollArea.setWidget(scrollWidget)
# 				varVBox = QVBoxLayout(scrollWidget)
# 				pane.addWidget(scrollArea)
				
# 				vprmsinput = VarRMSInput([], varVBox) ###
# 				self.rmsinputs[p] = vprmsinput
				
# 				for arg in ba.arguments[p]:
# 					self.createPositionalRMSInputSet(vprmsinput, varVBox, True, value=arg)
# 				self.createPositionalRMSInputSet(vprmsinput, varVBox, False, value=None)
# 				varVBox.setContentsMargins(0,0,0,0)
# 			elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
# 				pane.addWidget(QLabel(f"{p} - VAR_KEYWORD"))
# 				scrollArea = QScrollArea()
# 				scrollArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
# 				scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn);
# 				scrollArea.setWidgetResizable(True)
# 				scrollWidget = QWidget()
# 				scrollArea.setWidget(scrollWidget)
# 				varVBox = QVBoxLayout(scrollWidget)
# 				pane.addWidget(scrollArea)
# 				vkrmsinput = VarRMSInput([], varVBox) ###
# 				self.rmsinputs[p] = vkrmsinput
				
# 				for key, arg in ba.arguments[p].items():
# 					self.createKeywordRMSInputSet(vkrmsinput, varVBox, key, True, value=arg)
# 				self.createKeywordRMSInputSet(vkrmsinput, varVBox, "", False, value=None)
# 				varVBox.setContentsMargins(0,0,0,0)
# 			else:
				
	def save_param(self):
		try:
			ba = self.getBoundArguments()
			clipboard = QApplication.clipboard()
			clipboard.setText(json.dumps(ba.arguments))
		except:
			pass

	def load_param(self):
		j = json.loads(self.load_param_text.text())
		parameters = self.func_signature.parameters
		for input_key, input_value in j.items():
			parameter = parameters[input_key]
# 			if p == "rmsp":
# 				arguments[p] = self.rms
# 				continue
			if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
				args = []
# 				for rmsinput in self.rmsinputs[p].rmsinputs:
# 					if rmsinput.status == "n":
# 						pass
# 					elif rmsinput.status == "t":
# 						args.append(self.parse(rmsinput.textedit.text(), parameter.annotation))
# 					elif rmsinput.status == "r":
# 						args.append(rmsinput.rmsentry)
# 					else:
# 						raise Exception()
# 				arguments[p] = args
				pass
			elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
				pass
# 				kwargs = {}
# 				for rmsinput in self.rmsinputs[p].rmsinputs:
# 					if rmsinput.status == "n":
# 						pass
# 					elif rmsinput.status == "t":
# 						if json.loads(rmsinput.keytextedit.text()) in kwargs:
# 							print(f"WARNING: duplicated keys in {p} - {rmsinput.keytextedit.text()}")
# 						kwargs[json.loads(rmsinput.keytextedit.text())] = json.loads(rmsinput.textedit.text())
# 					elif rmsinput.status == "r":
# 						if json.loads(rmsinput.keytextedit.text()) in kwargs:
# 							print(f"WARNING: duplicated keys in {p} - {rmsinput.keytextedit.text()}")
# 						kwargs[json.loads(rmsinput.keytextedit.text())] = rmsinput.rmsentry
# 					else:
# 						raise Exception()
# 				arguments[p] = kwargs
			else:
# 				print(input_key)
				rmsinput = self.rmsinputs[input_key]
				rmsinput.status = "t"
				rmsinput.textedit.setText(str(input_value))
# 				if rmsinput.status == "n":
# 					pass
# 				elif rmsinput.status == "t":
# 					rmsinput.textedit.setText(str, parameter.annotation)
# 				elif rmsinput.status == "r":
# 					arguments[p] = self.rms_interactor
# 				else:
# 					raise Exception()
# 		self.simulate()
	def checkArguments(self):
		return not self.addArgumentCheckHints()
	def addArgumentCheckHints(self):
		s = self.func_signature
		h = False
		for p, parameter in s.parameters.items():
			if p not in self.rmsinputs:
				continue
			if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
				pass
			elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
				pass
			else:
				rmsinput = self.rmsinputs[p]
				if rmsinput.status == "n":
					rmsinput.namelabel.setStyleSheet("color: red");
					h = True
				elif rmsinput.status == "t":
					try:
						self.parse(rmsinput.textedit.text(), parameter.annotation)
						if parameter.annotation == InputFileType:
							if self.rmstemplatelib_interactor.execute("is_file_exist", args=[rmsinput.textedit.text()]):
								rmsinput.namelabel.setStyleSheet("color: black");
							else:
								h = True
								rmsinput.namelabel.setStyleSheet("color: red");
						else:
							rmsinput.namelabel.setStyleSheet("color: black")
					except:
						h = True
						rmsinput.namelabel.setStyleSheet("color: red");
 					
				elif rmsinput.status == "r":
					pass
# 					arguments[p] = rmsinput.rmsentry
		return h
		
	def parse(self, t, anno):
		if anno == str:
			v = t
		elif anno == int:
			v = int(t)
		elif anno == float:
			v = float(t)
		elif anno == bool:
			v = convert_to_bool(t)
		elif anno == InputFileType or anno == OutputFileType:
			v = t
		else:
			v = t
		return v
	
	def simulate(self):
		try:
			ba = self.getBoundArguments()
		except:
			return
		ts = self.rmstemplatelib_interactor.execute("simulate", args=[self.bookname, self.chaptername, self.bookmark],
					kwargs={
						"args":ba.args, 
						"kwargs":ba.kwargs
						})
		fig, ax = self.tsw.fig, self.tsw.ax
		ax.cla()
		g = nx.DiGraph()
	
		for u in ts.unruntasks_db.values():
			for v in u.input_virtualresources:
				g.add_edge(v.get_full_id(), u.get_full_id())
			for v in u.output_virtualresources + u.output_files:
				g.add_edge(u.get_full_id(), v.get_full_id())
	
	
		pos = nx.nx_agraph.graphviz_layout(g, prog="dot")
		pos = {k: (v[0], v[1] + 20 * idx) for idx, (k, v) in enumerate(sorted(pos.items(), key=lambda x: (x[1][1], x[1][0])))}
		labels = {i: "" if i[0] != RMSEntryType.VIRTUALRESOURCE else (os.path.basename(ts.virtualresources_db[i[1]].file_path) if ts.virtualresources_db[i[1]].file_path is not None else "") for i in g.nodes}
		colormap = ["grey" if i[0] == RMSEntryType.UNRUNTASK else ("green" if ts.virtualresources_db[i[1]].file_path is None else ("red" if ts.virtualresources_db[i[1]].file_path in ts.rfdb else "orange")) for i in g.nodes]
	
		nx.draw(g, pos=pos, node_color=colormap, ax=ax)
		text = nx.draw_networkx_labels(g, pos, labels=labels, font_size=6, ax=ax)
		for _, t in text.items():
			t.set_rotation(-10) 
		fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
# 		self.tsw.fig = fig
		self.tsw.fcSignal.emit()
		
	def getBoundArguments(self):
		arguments = {}
		s = self.func_signature
		ba = s.bind_partial() # Do not apply defaults
		for p, parameter in s.parameters.items():
			if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
				args = []
				for rmsinput in self.rmsinputs[p].rmsinputs:
					if rmsinput.status == "n":
						pass
					elif rmsinput.status == "t":
						args.append(self.parse(rmsinput.textedit.text(), parameter.annotation))
					elif rmsinput.status == "r":
						args.append(rmsinput.rmsentry)
					else:
						raise Exception()
				arguments[p] = args
			elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
				kwargs = {}
				for rmsinput in self.rmsinputs[p].rmsinputs:
					if rmsinput.status == "n":
						pass
					elif rmsinput.status == "t":
						if json.loads(rmsinput.keytextedit.text()) in kwargs:
							print(f"WARNING: duplicated keys in {p} - {rmsinput.keytextedit.text()}")
						kwargs[json.loads(rmsinput.keytextedit.text())] = json.loads(rmsinput.textedit.text())
					elif rmsinput.status == "r":
						if json.loads(rmsinput.keytextedit.text()) in kwargs:
							print(f"WARNING: duplicated keys in {p} - {rmsinput.keytextedit.text()}")
						kwargs[json.loads(rmsinput.keytextedit.text())] = rmsinput.rmsentry
					else:
						raise Exception()
				arguments[p] = kwargs
			else:
				rmsinput = self.rmsinputs[p]
				if rmsinput.status == "n":
					pass
				elif rmsinput.status == "t":
					arguments[p] = self.parse(rmsinput.textedit.text(), parameter.annotation)
				elif rmsinput.status == "r":
					arguments[p] = rmsinput.rmsentry
				else:
					raise Exception()
		for k, v in arguments.items():
			ba.arguments[k] = v 
		return ba
	def close_fig(self):
		self.timer.stop()
		self.timer2.stop()
		self.tsw.fc.setVisible(False)
		self.tsw.ax.cla() # ****
		self.tsw.fig.clf() # ****
		self.tsw.fc.close()
		
	
class TemplateSimulatorFlowWidget(QWidget):
	fcSignal = pyqtSignal()
	def __init__(self):
		super().__init__()
		self.initUI()
		self.fcSignal.connect(self.onFigureUpdate)
		
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		fig, ax = plt.subplots()
		self.fig = fig
		self.ax = ax
		self.fc = FigureCanvas(self.fig)
		self.layout.addWidget(self.fc)
		
	def onFigureUpdate(self):
# 		if self.fc is not None:
# 			self.layout.removeWidget(self.fc)
		self.fc.draw()
		self.fc.setVisible(True)
		
	
	

class RMSBookWidget(QWidget):
	# Wrapper for switching versions
	
	def __init__(self, rms_actioner, bookname, book):
		super().__init__()
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.widget_dict = {}
		self.layout.addWidget(QLabel("Select Pipeline Version"))
		
		self.cb = QComboBox()
		self.layout.addWidget(self.cb)
		chapters = []
		for chaptername, chapter in book.content["chapter"].items():
			self.cb.addItem(chaptername)
			self.widget_dict[chaptername] = RMSChapterWidget(rms_actioner, bookname, chaptername, chapter, [])
			chapters.append(chaptername)
		self.cb.currentIndexChanged.connect(self.selectionchange)
		self.prev_chapter = None
		idx = max(list(range(len(chapters))), key=lambda i: chapters[i])
		self.cb.setCurrentIndex(idx)
		self.selectionchange(idx)
		
		
	def selectionchange(self, i):
		if self.prev_chapter is not None:
			self.widget_dict[self.prev_chapter].hide()
		chaptername = self.cb.currentText()
		self.layout.addWidget(self.widget_dict[chaptername])
		self.widget_dict[chaptername].show()
		self.prev_chapter = chaptername




class RMSChapterWidget(QWidget):
	def __init__(self, rms_actioner, bookname, chaptername, c, bookmark):
		super().__init__()
		self.rms_actioner = rms_actioner
		self.bookname = bookname
		self.chaptername = chaptername
		self.bookmark = bookmark
		if c['type'] == "container":
			layout = QVBoxLayout()
			self.setLayout(layout)
			layout.addWidget(QLabel(c['title']))
			for idx, j in enumerate(c['content']):
				layout.addWidget(RMSChapterWidget(rms_actioner, bookname, chaptername, j, bookmark + [idx]))
		elif c['type'] == "pipeline":
			layout = QHBoxLayout()
			self.setLayout(layout)
			p = QPushButton(c["title"])
			layout.addWidget(p)
			layout.addWidget(QLabel(c["title"]))
# 			description = c['description']
# 			if len(description) > 0:
# 				with open(description) as f:
# 					description = f.read()
# 			self.description = description
			p.clicked.connect(self.run_template)
		else:
			raise Exception()
			
	def run_template(self):
		self.rms_actioner.edit_and_run_template(self.bookname, self.chaptername, self.bookmark)


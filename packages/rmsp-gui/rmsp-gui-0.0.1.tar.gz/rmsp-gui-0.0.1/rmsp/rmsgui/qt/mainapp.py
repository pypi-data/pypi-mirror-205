
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from rmsp.rmscore import RMSEntryType, RMSUpdateEvent
from ..flowcontroller import RMSFlowController

from .widget import RMSEntryDescriptionFormatter
from .action import RMSActionQT
from .widget import RMSStatWidget, RMSSearchWidget, DescriptionWidget
from .analysis import AnalysisFactory
from .flowview import RView


class QtRMSUpdateListener(QObject):
	rms_update_signal = pyqtSignal(object)
		
	def __init__(self, func):
		super().__init__()
		self.rms_update_signal.connect(func)
	def onRMSUpdate(self, events):
		self.rms_update_signal.emit(events)
		
class RMSWindow(QMainWindow):
	"""
	Main Window
	
	Create the different areas
	
	"""
	add_message_signal = pyqtSignal(str)
	
# 	def rmsobj_edit_func(self, rmsobj):
# 		if rmsobj.get_type() == RMSEntryType.UNRUNTASK:
# 			dlg = RMSUnrunTaskEditDialog(self.controller, rmsobj)
# 			if dlg.exec():
# 				return dlg.getArguments()
# 			return None
# 		dlg = RMSEntryEditDialog(rmsobj, self)
# 		if dlg.exec():
# 			return dlg.updated_fields
# 		else:
# 			return None
# 		
# 	def rmsobj_fetch_resource_func(self, resources, required_tasks, required_resources):
# 		if len(required_tasks) == 0:
# 			dlg = RMSEntryFetchContentWarningDialog(self)
# 			dlg.exec()
# 			return None
# 		dlg = RMSEntryFetchContentConfirmationDialog(resources, required_tasks, required_resources, self)
# 		if dlg.exec():
# 			return resources
# 		else:
# 			return None
# 	def link_unruntask_func(self, unruntask):
# 		dlg = RMSUnrunTaskInputArgumentSelectionDialog(unruntask, self)
# 		if dlg.exec():
# 			return dlg.selected_argument_name, dlg.key
# 		else:
# 			return None
# 	def select_resources_func(self):
# 		dlg = RMSResourceSelectionDialog(self.controller, self)
# 		if dlg.exec():
# 			return dlg.selected_rmsobjs()
# 		else:
# 			return None
	
	def _add_message_log(self, s):
		self.message_log_area.moveCursor(QTextCursor.End)
		self.message_log_area.insertPlainText(datetime.datetime.now().strftime("[%Y/%m/%d %H:%M:%S]") + " " + s + "\n")
	def add_message_log(self, s):
		self.add_message_signal.emit(s)
	def onRMSUpdate(self, events):
		for event, rmsid in events:
			rmstype = RMSEntryType(rmsid[0])
			if event == RMSUpdateEvent.DELETE:
				msg = f"A {rmstype.name} is deleted: {rmsid[1]}"
				self.add_message_log(msg)
			elif event == RMSUpdateEvent.INSERT:
				msg = f"A {rmstype.name} is inserted: {rmsid[1]}"
				self.add_message_log(msg)
			elif event == RMSUpdateEvent.REPLACE:
				msg = f"A {rmstype.name} is replaced: {rmsid[1]}"
				self.add_message_log(msg)
# 				if rmsid[0] == RMSEntryType.TASK:
	def _createCentralWidget(self, parent):
		# Central widget
		centralWidget = QWidget(parent)
		centralWidget.setObjectName("widget")
		p = centralWidget.palette()
		p.setColor(centralWidget.backgroundRole(), Qt.white)
		centralWidget.setPalette(p)
		return centralWidget
		
	def _createDescriptionArea(self):
		## Description area
		rmsDescriptionFormatter = RMSEntryDescriptionFormatter(self.rms_interactor)
		analysis_factory = AnalysisFactory(self.rms_interactor)
		description_scroll_area = QScrollArea(self.centralWidget)
		description_scroll_area.setGeometry(0, 0, 400, 400)
		description_scroll_area.setWidgetResizable(True)
		description_scroll_area.verticalScrollBar().setVisible(False)
		description_contents = DescriptionWidget(rmsDescriptionFormatter, analysis_factory, description_scroll_area)
		description_scroll_area.setWidget(description_contents)
		self.description_contents = description_contents
		return description_scroll_area
	def _createFlowViewArea(self):
		view_scroll_area = QScrollArea(self.centralWidget)
		view_scroll_area.setGeometry(0, 0, 400, 400)
		view_scroll_area.setWidgetResizable(True)
		view_scroll_area.verticalScrollBar().setVisible(False)
		
		#self.gridLayout.addWidget(self.view_scroll_area, 0, 0, 2, 1)
		
		#view_contents = RView(self.controller, view_scroll_area)
		view_contents = RView(self.fc, view_scroll_area)
# 		rmsDescriptionFormatter = RMSEntryDescriptionFormatter(view_panel_controller.rmsp)
		#self.view_contents = RView(view_panel_controller, rmsDescriptionFormatter, self.view_scroll_area)
		view_contents.setGeometry(0, 0, 400, 800)
		view_contents.setMinimumSize(380, 1000)
# 		view_contents.register_description(self.description_contents)
		view_scroll_area.setFocusProxy(view_contents)
		self.fc.register_selection_listener(self.description_contents)
		view_scroll_area.setWidget(view_contents)
		return view_scroll_area
	def _createSearchArea(self):
		return RMSSearchWidget(self.rms_interactor, self.centralWidget)
	def _createMessageLogArea(self):
		message_log_area = QPlainTextEdit(self.centralWidget)
		message_log_area.setReadOnly(True)
		message_log_area.setMinimumSize(100, 100)
		message_log_area.setMaximumHeight(50)
		return message_log_area
	def _createStatArea(self):
		return RMSStatWidget(self.rms_interactor, self.rmspool_interactor)
	
	def __init__(self, rms_interactor, rmspool_interactor, rmstemplatelib_interactor, parent=None):
		super().__init__(parent)
		self.rms_interactor = rms_interactor
		self.rmspool_interactor = rmspool_interactor
		self.rmstemplatelib_interactor = rmstemplatelib_interactor
		
		self.rms_actioner = RMSActionQT(self, rms_interactor, rmspool_interactor, rmstemplatelib_interactor)
		self.fc = RMSFlowController(rms_interactor)
		self.fc.rms_actioner = self.rms_actioner
		
		
		# Window Layout
		self.setWindowTitle("Resource Management System GUI")
		self.resize(1600, 800)
		self._createActions()
		self._createMenuBar()
		self._createStatusBar()
		
		# Inner Layout
		self.centralWidget = self._createCentralWidget(parent)
		self.setCentralWidget(self.centralWidget)

		## Interlink between different areas
		self.selection = None
		
		## Area Creation
		self.description_scroll_area = self._createDescriptionArea()
		self.view_scroll_area = self._createFlowViewArea()
		self.search_area = self._createSearchArea()
		self.message_log_area = self._createMessageLogArea()
		self.stat_area = self._createStatArea()
		
		# Connection
		## SPLITTER #
		splitter_right_tb = QSplitter(Qt.Vertical)
		splitter_right_tb.addWidget(self.description_scroll_area)
		splitter_right_tb.addWidget(self.search_area)
		splitter_right_tb.setSizes([200,200])

		splitter_top_lr = QSplitter(Qt.Horizontal)
		splitter_top_lr.addWidget(self.view_scroll_area)
		splitter_top_lr.addWidget(splitter_right_tb)
		splitter_right_tb.setSizes([500,100])
		
		splitter_bot_lr = QSplitter(Qt.Horizontal)
		splitter_bot_lr.addWidget(self.message_log_area)
		splitter_bot_lr.addWidget(self.stat_area)
		splitter_right_tb.setSizes([50,50])
		
		splitter_tb = QSplitter(Qt.Vertical)
		splitter_tb.addWidget(splitter_top_lr)
		splitter_tb.addWidget(splitter_bot_lr)
		splitter_tb.setSizes([100,200])

		hbox = QHBoxLayout(self.centralWidget)		
		hbox.addWidget(splitter_tb)
		
		
		self.add_message_signal.connect(self._add_message_log)
		self.rms_interactor.register_listener("rms", self.onRMSUpdate)
# 		self.rms_actioner.edit_and_run_template("PROcapDataAnalysis", "20230417", [0,0])
		
			
	def _createMenuBar(self):
		menuBar = self.menuBar()
		# RMS menu
		rmsMenu = QMenu("&RMS", self)
		menuBar.addMenu(rmsMenu)
		rmsMenu.addAction(self.actionRegisterFiles)
		rmsMenu.addAction(self.actionRunLibrarySelection)

	def _createToolBars(self):
		pass
		
	def _createStatusBar(self):
		# The status bar will later be linked to the actions
		self.statusbar = self.statusBar()		
		# Temporary message
# 		self.statusbar.showMessage("Ready", 3000)
		# Permanent widget
		self.cLabel = QLabel(f"Ready")
		self.statusbar.addWidget(self.cLabel)
		self.wcLabel = QLabel(f"RMS GUI beta-test")
		self.statusbar.addPermanentWidget(self.wcLabel)
	def _createActions(self):
		self.actionRegisterFiles = QAction(self)
		self.actionRegisterFiles.setText("Register files")
		self.actionRegisterFiles.triggered.connect(self.rms_actioner.register_file)
		
		self.actionRunLibrarySelection = QAction(self)
		self.actionRunLibrarySelection.setText("Run RMS Templates")
		self.actionRunLibrarySelection.triggered.connect(self.rms_actioner.run_library_selection)





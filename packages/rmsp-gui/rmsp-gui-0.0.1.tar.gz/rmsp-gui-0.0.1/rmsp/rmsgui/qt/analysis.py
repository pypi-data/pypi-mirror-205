from abc import ABC, ABCMeta
USE_WEB=False
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os
import queue
import time
import itertools
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib_venn


from biodata.baseio import get_text_file_extension
from biodata.bed import BED3Reader
import genomictools

from rmsp.rmscore import RMSEntryType

if USE_WEB:
	from PyQt5.QtWebEngineWidgets import QWebEngineView
def _plot_fast_bar_20210429(x, height, width=0.8, bottom=0, *, align='center', ax=None, **kwargs):
	if ax is None:
		ax = plt.gca()
	if np.ndim(bottom) == 0:
		bottom = np.repeat(bottom, len(height))
	ny2 = np.repeat(bottom, 4)
	ny = list(itertools.chain.from_iterable([(b, h+b, h+b, b) for h, b in zip(height, bottom)]))
	if align == 'center':
		modifier = width / 2
	else:
		modifier = 0
	
	nx = list(itertools.chain.from_iterable([(i - modifier, i - modifier, i + width - modifier, i + width - modifier) for i in x]))
	combined_kwargs = dict(linewidth=0)
	combined_kwargs.update(kwargs)
	
	artist = ax.fill_between(nx, ny, ny2, **combined_kwargs)
	artist.sticky_edges.y.append(min(bottom))
	return artist
def _plot_histogram_20210430(data, bin_size=None, nbins=None, min_value=None, max_value=None, left_bound=True, right_bound=True, cumulative=False, ax=None, **kwargs):
	if ax is None:
		ax = plt.gca()
	if min_value is None:
		min_value = min(data)
	if max_value is None:
		max_value = max(data)
	
	if nbins is None and bin_size is None:
		raise Exception("You need to set either nbins or bin_size")
	elif nbins is not None and bin_size is None:
		bin_size = (max_value - min_value) / nbins
		bins = np.linspace(min_value, max_value, nbins+1)
	elif nbins is None and bin_size is not None:
		bins = np.arange(min_value, max_value + bin_size, step=bin_size)
		nbins = len(bins) - 1
	elif nbins is not None and bin_size is not None:
		raise Exception("You need to set either nbins or bin_size, but not both")
	step_size=bin_size
	max_value = min_value + nbins * bin_size
	if not right_bound:
		bins = np.append(bins, np.inf)
	if not left_bound:
		bins = np.concatenate([[-np.inf], bins])
	h = np.histogram(data, bins=bins)
	if not left_bound: 
		x = np.concatenate([[h[1][1] - step_size / 2], h[1][1:-1] + step_size/2])
	else:
		x = h[1][:-1] + step_size/2
		
	_normalize = None # I don't wan to use this now
	if _normalize is None:
		y = h[0]/sum(h[0])
	else:
		y = h[0] / _normalize 
	if cumulative:
		y = np.cumsum(y)
	ax.plot(x, y, **kwargs)
	if "label" in kwargs:
		del kwargs["label"]
	_plot_fast_bar_20210429(x, y, width=step_size, alpha=0.2, ax=ax, **kwargs)
	ax.set_xlim(min(x) - step_size / 2, max(x) + step_size / 2)
	if nbins < 11:
		xt = np.linspace(min_value, max_value, nbins+1)
	else:
		xt = np.linspace(min_value, max_value, 5)
	ax.set_xticks(xt)
		
	return ax
	
class AnalysisFactory():
	def __init__(self, rms_interactor):
		self.rms_interactor = rms_interactor
		self.analysis_widgets = {}
		
		self._register()
		if USE_WEB:
			self.method_widget = MethodWidget()
			raise Exception("Under development")
		else:
			self.method_widget = TextMethodWidget()
	def _register(self):
		'''
		Default registered module
		'''
		# Resources
		self.register("GC", GenomicCollectionWidget())
		self.register("MFIG", MatplotlibFigureWidget())
		self.register("Venn", VennWidget())
		## Two way overlaps
		## Two way venn
		## pd 
		
		# Files
		self.register("BED", BEDWidget())
		self.register("BW", BigWigWidget())
		self.register("Image", DisplayImageWidget())
		# XLS
		# svg
		#self.register("FASTA", FASTAWidget())
		#self.register("txt", FASTAWidget())
		
		
	def register(self, name, analysis_widget):
		self.analysis_widgets[name] = analysis_widget
		
	def find_analysis_widgets(self, rmsids):
		'''
		Ask each registered analysis widget to check if they can process the selected RMSids
		'''
		rmsobjs = [self.rms_interactor.execute("get", [rmsid]) for rmsid in rmsids if self.rms_interactor.execute("has", [rmsid])]
# 		rmsobjs = [self.rmscontroller.get(rmsid) for rmsid in rmsids if self.rmscontroller.has(rmsid)]
		
		# Display help for unruntask
		if len(rmsobjs) == 1:
			if next(iter(rmsobjs)).get_type() == RMSEntryType.UNRUNTASK:
				func = self.rms_interactor.execute("get", [(RMSEntryType.PIPE, next(iter(rmsobjs)).pid)]).func
				self.method_widget.run(func)
				return {"Help":self.method_widget}
			
		contents = []
		content_types = []
		file_paths = []
		for rmsobj in rmsobjs:
			if rmsobj.get_type() == RMSEntryType.RESOURCE:
				if not rmsobj.has_content:
					return {}
				contents.append(rmsobj.content)
				content_types.append(rmsobj.content_type)
			elif rmsobj.get_type() == RMSEntryType.FILERESOURCE:
				file_paths.append(rmsobj.file_path)
			else:
				return {}
# 		for wname, analysis_widget in self.analysis_widgets.items() if analysis_widget.check_validity(content_types, file_paths
		aws = {wname:analysis_widget for wname, analysis_widget in self.analysis_widgets.items() if analysis_widget.check_validity(content_types, file_paths)}
		for analysis_widget in aws.values():
			analysis_widget.update_analysis(contents, file_paths)
		return aws
			

class QueueThread(QThread):
	def __init__(self, func, *args, **kwargs):
		super().__init__()
		self.func = func
		self.args = args
		self.kwargs = kwargs
	def run(self):
		self.func(*self.args, **self.kwargs)

class AnalysisWidget(QWidget):
	'''
	Subclass should override _run method.
	Analysis can be implemented to be interruptible by constantly checking whether the queue is empty.
	All analysis widget should not obtain extra information from rms 
	'''
	def __init__(self):
		super().__init__()
		self.queue = queue.Queue()
		self.qthread = QueueThread(self._queue_checker)
		self.qthread.start()
		
	def _queue_checker(self):
		while True:
			contents, file_paths = self.queue.get() # Block until someone queue
			self._interrupt()
			while not self.queue.empty():
				contents, file_paths = self.queue.get()
			# Can try to interrupt the running tasks
			self._run(contents, file_paths)
			time.sleep(0.1)
	def _interrupt(self):
		pass
	def _run(self, contents, file_paths): # Abstract method
		pass

	def check_validity(self, contents, file_paths):
		'''
		Checkk if the analysis widget is valid, given the contents and file paths.
		'''
		return False
	
	def update_analysis(self, contents, file_paths):
		'''
		This method is called when to tell the analysis widget that new analysis is used. 
		'''
		self.queue.put((contents, file_paths))


class LoaderWidget(QWidget):
	finished = pyqtSignal(bool)
	def __init__(self, widget):
		super().__init__()
		self.widget = widget
		self.initUI()
		self.finished.connect(lambda finished: self.setFinished(finished))
		
	def initUI(self):
		self.layout = QVBoxLayout()
		self.loadingIcon = QLabel()

		self.movie = QMovie(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "res/loading.gif")) 
		self.movie.setBackgroundColor(QColor("white"))
		self.loadingIcon.setMovie(self.movie)
		self.movie.start()

# 		self.loadingIcon.setText("Loading")
		self.setLayout(self.layout)
		self.setFinished(False)
	
	def setFinished(self, finished):
		self.layout.removeWidget(self.loadingIcon)
		self.loadingIcon.setParent(None)
		self.layout.removeWidget(self.widget)
		self.widget.setParent(None)
		self.widget.setVisible(False)
		self.loadingIcon.setVisible(False)
		if finished:
			self.layout.addWidget(self.widget)
			self.widget.setVisible(True)
		else:
			self.layout.addWidget(self.loadingIcon)
			self.loadingIcon.setVisible(True)			


class PandasDataFrameWidget(AnalysisWidget): # Unfinished
	fcSignal = pyqtSignal()
	statSignal = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.initUI()
		self.fcSignal.connect(self.onFigureUpdate)
		self.statSignal.connect(self.onStatUpdate)
		
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.statWidget = LoaderWidget(QTextEdit())
		self.fcWidget   = LoaderWidget(FigureCanvas(plt.Figure(tight_layout=True)))
		self.layout.addWidget(self.statWidget)
		self.layout.addWidget(self.fcWidget)
		self.layout.addWidget(QLabel("Place holder for parameters"))

	def onStatUpdate(self, stat):
		self.statWidget.widget.setText(stat)
	
	def onFigureUpdate(self):
		self.fcWidget.widget.draw()
		
	
	def _run(self, contents, file_paths):
		try:
			self.fcWidget.finished.emit(False)
			self.statWidget.finished.emit(False)
			# GCS
			time.sleep(3)
			gcs = contents
			lengths = [[len(r.genomic_pos) for r in gc] for gc in gcs]
			flatten_lengths = list(itertools.chain.from_iterable(lengths))
			# Stat
			stat = {"Total":len(flatten_lengths), "Median": f"{np.median(flatten_lengths):.0f}", "Mean": f"{np.mean(flatten_lengths):.0f}", "Max": np.max(flatten_lengths), "Min": np.min(flatten_lengths)}
			#print("\n".join([f"{k}: {v}" for k, v in stat.items()]))
			s = "\n".join([f"{k}: {v}" for k, v in stat.items()])
			self.statSignal.emit(s)
			self.statWidget.finished.emit(True)
			
			# Fig
			fig = self.fcWidget.widget.figure
			fig.clear()
			ax = fig.add_subplot(111)
			for b in lengths:
				_plot_histogram_20210430(b, 10, max_value=max(b), ax=ax)
			ax.set_xlabel("Length (bp)")
			ax.set_ylabel("Frequency")
			ax.set_title("Size Distribution")
			self.fcSignal.emit()
			self.fcWidget.finished.emit(True)
		except Exception as e:
			print(e)
			
class MethodWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		vbox = QVBoxLayout(self)
		self.webEngineView = QWebEngineView()
		vbox.addWidget(self.webEngineView)
		self.setLayout(vbox)

	
	def run(self, func):
		import os
		module = func.__module__
		name = func.__qualname__
		description_file = f"path"
		if os.path.exists(description_file):
			qurl = QUrl.fromLocalFile(description_file)
			qurl.setFragment(module + "." + name)
		else:
			qurl = QUrl("about:blank")
		print(str(qurl))
		self.webEngineView.load(qurl)
class TextMethodWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		vbox = QVBoxLayout(self)
		self.text_edit = QTextEdit()
		vbox.addWidget(self.text_edit)
		self.setLayout(vbox)

	
	def run(self, func):
		module = func.__module__
		name = func.__qualname__
		doc = func.__doc__
		self.text_edit.setText(f"{module}\n{name}\n{doc}\n")
		

class MatplotlibFigureWidget(AnalysisWidget):
	fcSignal = pyqtSignal()
	def __init__(self):
		super().__init__()
		self.initUI()
		self.fcSignal.connect(self.onFigureUpdate)
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.fc = None
		
	def onFigureUpdate(self):
		if self.fc is not None:
			self.layout.removeWidget(self.fc)
		self.fc = FigureCanvas(self.fig)
		self.layout.addWidget(self.fc)
		self.fc.draw()
		self.fc.setVisible(True)	#self.fc.draw()
		
	def check_validity(self, content_types, file_paths):
		if len(content_types) != 1 or len(file_paths) != 0:
			return False
		t = content_types[0]
		return issubclass(t, matplotlib.figure.Figure)
	
	def _run(self, contents, file_paths):
		self.fig = contents[0]
		
		self.fcSignal.emit()         
	
class GenomicCollectionWidget(AnalysisWidget):
	fcSignal = pyqtSignal()
	statSignal = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.initUI()
		self.fcSignal.connect(self.onFigureUpdate)
		self.statSignal.connect(self.onStatUpdate)
		
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.statWidget = LoaderWidget(QTextEdit())
		self.fcWidget   = LoaderWidget(FigureCanvas(plt.Figure(tight_layout=True)))
		self.layout.addWidget(self.statWidget)
		self.layout.addWidget(self.fcWidget)
		self.layout.addWidget(QLabel("Place holder for parameters"))

	def onStatUpdate(self, stat):
		self.statWidget.widget.setText(stat)
	
	def onFigureUpdate(self):
		self.fcWidget.widget.draw()
		
	def check_validity(self, content_types, file_paths):
		if len(content_types) != 1 or len(file_paths) != 0:
			return False
		t = content_types[0]
		return issubclass(t, genomictools.GenomicCollection)
	
	def _run(self, contents, file_paths):
		try:
			self.fcWidget.finished.emit(False)
			self.statWidget.finished.emit(False)
			# GCS
			gcs = contents
			lengths = [[len(r.genomic_pos) for r in gc] for gc in gcs]
			flatten_lengths = list(itertools.chain.from_iterable(lengths))
			# Stat
			stat = {"Total":len(flatten_lengths), "Median": f"{np.median(flatten_lengths):.0f}", "Mean": f"{np.mean(flatten_lengths):.0f}", "Max": np.max(flatten_lengths), "Min": np.min(flatten_lengths)}
			s = "\n".join([f"{k}: {v}" for k, v in stat.items()])
			self.statSignal.emit(s)
			self.statWidget.finished.emit(True)
			
			# Fig
			fig = self.fcWidget.widget.figure
			fig.clear()
			ax = fig.add_subplot(111)
			for b in lengths:
				_plot_histogram_20210430(b, 10, max_value=max(b), ax=ax)
			ax.set_xlabel("Length (bp)")
			ax.set_ylabel("Frequency")
			ax.set_title("Size Distribution")
			self.fcSignal.emit()
			self.fcWidget.finished.emit(True)
		except Exception as e:
			print(e)


class SettingWidget(QWidget):
	def __init__(self, update_func):
		super().__init__()
		self.update_func = update_func
		self.layout=QGridLayout()
		self.setLayout(self.layout)
		update_button = QPushButton("Update")
		update_button.clicked.connect(self.callUpdate)
		self.layout.addWidget(update_button, 0, 0, 1, 2)
		self.row_idx = 1
		self.setting_default_map = {}
		self.setting_entry_map = {} 
		
	def addSetting(self, key, label_name=None, default_value=""):
		if label_name is None:
			label_name = key
		self.layout.addWidget(QLabel(label_name), self.row_idx, 0)
		t = QLineEdit(default_value)
		self.layout.addWidget(t, self.row_idx, 1)
		self.row_idx += 1
		self.setting_entry_map[key] = t
		self.setting_default_map[key] = default_value
	def reset(self):
		for key, default_value in self.setting_default_map.items():
			self.setting_entry_map[key].setText(default_value)
	def callUpdate(self):
		params = {k:v.text() for k, v in self.setting_entry_map.items()}
		print(params)
		self.update_func(params)
		
def _convert_setting_value(s, func, default_blank=None):
	if s == "":
		return default_blank
	else:
		return func(s)
	
	
	
class BEDWidget(AnalysisWidget):
	fcSignal = pyqtSignal()
	statSignal = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.initUI()
		self.fcSignal.connect(self.onFigureUpdate)
		self.statSignal.connect(self.onStatUpdate)
		
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.statWidget = LoaderWidget(QTextEdit())
		self.fcWidget  = LoaderWidget(FigureCanvas(plt.Figure(tight_layout=True)))
		self.layout.addWidget(self.statWidget, stretch=3)
		self.layout.addWidget(self.fcWidget, stretch=8)
		self.setting_widget = SettingWidget(self._update_figure_setting)
		
		self.setting_widget.addSetting("bin_size", default_value="10")
		self.setting_widget.addSetting("min_value")
		self.setting_widget.addSetting("max_value")
		
		self.layout.addWidget(self.setting_widget, stretch=3)

	def onStatUpdate(self, stat):
		self.statWidget.widget.setText(stat)
	
	def onFigureUpdate(self):
		self.fcWidget.widget.draw()
		
	def check_validity(self, content_types, file_paths):
		if len(content_types) != 0 or len(file_paths) == 0:
			return False
		return all(get_text_file_extension(f).lower() == "bed" for f in file_paths)

	def _plot_histogram(self, bin_size=10, nbins=None, min_value=None, max_value=None, left_bound=True, right_bound=True, cumulative=False):
		#bin_size=None, nbins=None, min_value=None, max_value=None, left_bound=True, right_bound=True, cumulative=False, ax=None, **kwargs
		fig = self.fcWidget.widget.figure
		fig.clear()
		ax = fig.add_subplot(111)
		for k, b in self.lengths.items():
			_plot_histogram_20210430(b, bin_size, nbins, min_value, max_value, left_bound, right_bound, cumulative, ax=ax, label=k)
		ax.set_xlabel("Length (bp)")
		ax.set_ylabel("Frequency")
		ax.set_title("Size Distribution")
# 		ax.legend()
		
	def _update_figure_setting(self, params):
		self.fcWidget.finished.emit(False)
		hist_params = {k:_convert_setting_value(v, int) for k, v in params.items()}
		self._plot_histogram(**hist_params)
		self.fcSignal.emit()
		self.fcWidget.finished.emit(True)
	
	def _run(self, contents, file_paths):
		try:
			self.fcWidget.finished.emit(False)
			self.statWidget.finished.emit(False)
			# GCS
			#time.sleep(3)
			self.setting_widget.reset()			
			import os
			common_path = os.path.commonpath(file_paths)
			if not os.path.isdir(common_path):
				common_path = os.path.dirname(common_path)
			target_file_dict = {p: os.path.relpath(p, common_path) for p in file_paths}

			gcs = {target_file_dict[f]:BED3Reader.read_all(genomictools.GenomicCollection, f) for f in file_paths}
			lengths = {k:[len(r.genomic_pos) for r in gc] for k, gc in gcs.items()}
			self.lengths = lengths
			
			flatten_lengths = list(itertools.chain.from_iterable(lengths.values()))
			# Stat
			stat = {"Total":len(flatten_lengths), "Median": f"{np.median(flatten_lengths):.0f}", "Mean": f"{np.mean(flatten_lengths):.0f}", "Max": np.max(flatten_lengths), "Min": np.min(flatten_lengths)}
			s = "\n".join([f"{k}: {v}" for k, v in stat.items()])
			self.statSignal.emit(s)
			self.statWidget.finished.emit(True)
			
			# Fig
			self._plot_histogram()
			self.fcSignal.emit()
			self.fcWidget.finished.emit(True)
			
		except Exception as e:
			print(e)

class BigWigWidget(AnalysisWidget):
	chromSignal = pyqtSignal(str)
	statSignal = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.initUI()
		self.statSignal.connect(self.onStatUpdate)
		self.chromSignal.connect(self.onChromUpdate)
		
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.statWidget = LoaderWidget(QTextEdit())
		self.chromWidget   = LoaderWidget(QTextEdit())
		self.layout.addWidget(self.statWidget)
		self.layout.addWidget(self.chromWidget)
# 		self.layout.addWidget(QLabel("Place holder for parameters"))

	def onStatUpdate(self, stat):
		self.statWidget.widget.setText(stat)
	def onChromUpdate(self, chrom):
		self.chromWidget.widget.setText(chrom)
	
# 	def onFigureUpdate(self):
# 		self.fcWidget.widget.draw()
		
	def check_validity(self, content_types, file_paths):
		if len(content_types) != 0 or len(file_paths) != 1:
			return False
		f = file_paths[0]
		return get_text_file_extension(f).lower() == "bw" or get_text_file_extension(f).lower() == "bigwig"

	def _run(self, contents, file_paths):
		try:
# 			self.fcWidget.finished.emit(False)
			self.statWidget.finished.emit(False)
			# GCS
			#time.sleep(3)
			import pyBigWig
			bw = pyBigWig.open(file_paths[0])
			
			time.sleep(10)
			s = "\n".join([f"{k}: {v}" for k, v in bw.header().items()])
			self.statSignal.emit(s)
			self.statWidget.finished.emit(True)
			
			s = "Chromosomes\n----------------------\n" + "\n".join([f"{k}: {v}" for k, v in bw.chroms().items()])
			self.chromSignal.emit(s)
			self.chromWidget.finished.emit(True)
			
			# Fig
# 			fig = self.fcWidget.widget.figure
# 			fig.clear()
# 			ax = fig.add_subplot(111)
# 			for b in lengths:
# 				plot_histogram(b, 10, max_value=max(b), ax=ax)
# 			ax.set_xlabel("Length (bp)")
# 			ax.set_ylabel("Frequency")
# 			ax.set_title("Size Distribution")
# 			self.fcSignal.emit()
# 			self.fcWidget.finished.emit(True)
		except Exception as e:
			print(e)

class VennWidget(AnalysisWidget):
	fcSignal = pyqtSignal()
# 	statSignal = pyqtSignal(str)

	def __init__(self):
		super().__init__()
		self.initUI()
		self.fcSignal.connect(self.onFigureUpdate)
# 		self.statSignal.connect(self.onStatUpdate)
		
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.fcWidget   = LoaderWidget(FigureCanvas(plt.Figure(tight_layout=True)))
		self.layout.addWidget(self.fcWidget)
	
	def onFigureUpdate(self):
		self.fcWidget.widget.draw()
		
	def check_validity(self, content_types, file_paths):
		if (len(content_types) != 2 and len(content_types) != 3) or len(file_paths) != 0:
			return False
		return all(issubclass(t, set) for t in content_types)
	
	def _run(self, contents, file_paths):
		try:
			self.fcWidget.finished.emit(False)
			# GCS
			#time.sleep(3)
			subsets = contents
			
			# Fig
			fig = self.fcWidget.widget.figure
			fig.clear()
			ax = fig.add_subplot(111)
			if len(subsets) == 2:
				matplotlib_venn.venn2(subsets, ax=ax)
			elif len(subsets) == 3:
				matplotlib_venn.venn3(subsets, ax=ax)
			else:
				raise Exception()
			#ax.set_title("Size Distribution")
			self.fcSignal.emit()
			self.fcWidget.finished.emit(True)
		except Exception as e:
			print(e)






class MyGraphicsView(QGraphicsView):
	def __init__(self):
		QGraphicsView.__init__(self)
		self.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)
		self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.setDragMode(QGraphicsView.ScrollHandDrag)
	def wheelEvent(self,event):        
		adj = (event.delta()/120) * 0.1
		self.scale(1+adj,1+adj)
class View(QGraphicsView):
	def __init__(self):
		super().__init__()
		self.zoom = 1
		self.rotate = 0
		#self.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)
		self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.setDragMode(QGraphicsView.ScrollHandDrag)
		
	def fitInView(self, *args, **kwargs):
		super().fitInView(*args, **kwargs)
		self.zoom = self.transform().m11()

	def wheelEvent(self, event):
		x = event.angleDelta().y() / 120
		if x > 0:
			self.zoom *= 1.05
			self.updateView()
		elif x < 0:
			self.zoom /= 1.05
			self.updateView()

	def updateView(self):
		self.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))



# class QGraphicsSceneExtended(QGraphicsScene):
# 	
# 	def set_(self):
# 		pass
# 	def contextMenuEvent(self, event):
# 		self.
class DisplayImageWidget(AnalysisWidget):
	# need to add support on resizing image
	fcSignal = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.initUI()
		self.fcSignal.connect(self.onFigureUpdate)
		
		
	def initUI(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self._view = View()
		self.fcWidget = LoaderWidget(self._view)
		self.layout.addWidget(self.fcWidget)
		self._graphicsScene = QGraphicsScene(self)
		self._view.setScene(self._graphicsScene)
		


	def onFigureUpdate(self):
		for i in list(self._graphicsScene.items()):
			self._graphicsScene.removeItem(i)
		self._graphicsScene.addPixmap(self.im)
		
		#self.fcWidget.widget.setPixmap(self.im)
		
	def check_validity(self, content_types, file_paths):
		import os
		if len(content_types) != 0 or len(file_paths) != 1:
			return False
		ext = os.path.splitext(file_paths[0])[1].lower()
		return ext in [".png", ".jpg", ".gif"]
	
	def _run(self, contents, file_paths):
		try:
			self.fcWidget.finished.emit(False)
			
			# Fig
			file_path = file_paths[0]
			self.im = QPixmap(file_path)
			self.fcSignal.emit()
			self.fcWidget.finished.emit(True)
		except Exception as e:
			print(e)

# 
# def _plot_gc_histogram(fig, gcs):
# 	fig.clear()
# 	ax = fig.add_subplot(111)
# 	for gc in gcs:
# 		b = [len(r.genomic_pos) for r in gc]
# 		print(f"Len: {len(b)}")
# 		plot_histogram(b, 10, max_value=max(b), ax=ax)
# 	ax.set_xlabel("Length (bp)")
# 	ax.set_ylabel("Frequency")
# 	ax.set_title("Size Distribution")
# 	import time
# 	time.sleep(3)
# 	return fig			
# def _get_gc_stat(gcs):
# 	import numpy as np
# 	l = [len(r.genomic_pos) for gc in gcs for r in gc]
# 	return {"Total":len(l), "Median": f"{np.median(l):.0f}", "Mean": f"{np.mean(l):.0f}", "Max": np.max(l), "Min": np.min(l)}
# 					
# class GenomicCollectionWidget(QWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.initUI()
# 
# 	def initUI(self):
# 		self.layout = QHBoxLayout()
# 		self.setLayout(self.layout)
# 		self.statWidget = LoaderWidget(QTextEdit())
# 		self.lwidget = LoaderWidget(FigureCanvas(plt.Figure(tight_layout=True)))
# 		self.layout.addWidget(self.statWidget)
# 		self.layout.addWidget(self.lwidget)
# 		self.layout.addWidget(QLabel("Place holder for parameters"))
# 	
# 
# 	def update(self, contents, file_paths):
# 		# Length distribution
# 		self.lwidget.setFinished(False)
# 		self.thread, self.worker = create_task(_plot_gc_histogram, self.lwidget.widget.figure, contents)
# 		self.thread.finished.connect(lambda: self.lwidget.widget.draw())
# 		self.thread.finished.connect(lambda: self.lwidget.setFinished(True))
# 		self.thread.start()
# 		
# 		# GC stat
# 		self.sthread, self.sworker = create_task(_get_gc_stat, contents)
# 		self.sthread.finished.connect(lambda: self.statWidget.widget.setText("\n".join([f"{k}: {v}" for k, v in self.sworker.result.items()])))
# 		self.sthread.finished.connect(lambda: self.statWidget.setFinished(True))
# 		self.sthread.start()
# 	
# 	
	
	
	
	
# 	
# from biodata.bed import BED3Reader
# from genomictools import GenomicCollection
# def _process_bed_files(fig, file_paths):
# 	print(file_paths)
# 	print("Ok-1")
# 	gcs = [BED3Reader.read_all(GenomicCollection, file_path) for file_path in file_paths]
# 	print("Ok-2")
# 	_plot_gc_histogram(fig, gcs)
# 	print("Ok-3")
# 	stat = _get_gc_stat(gcs)
# 	print("Ok-4")
# 	return stat
# 	
# 	
# class BEDWidget(QWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.initUI()
# 
# 	def initUI(self):
# 		self.layout = QHBoxLayout()
# 		self.setLayout(self.layout)
# 		self.statWidget = LoaderWidget(QTextEdit())
# 		self.lwidget = LoaderWidget(FigureCanvas(plt.Figure(tight_layout=True)))
# 		self.layout.addWidget(self.statWidget)
# 		self.layout.addWidget(self.lwidget)
# 		self.layout.addWidget(QLabel("Place holder for parameters"))
# 	
# 
# 	def update(self, contents, file_paths):
# 		print("Update called")
# 		# Length distribution
# 		self.lwidget.setFinished(False)
# 		self.thread, self.worker = create_task(_process_bed_files, self.lwidget.widget.figure, file_paths)
# 		self.thread.finished.connect(lambda: self.lwidget.widget.draw())
# 		self.thread.finished.connect(lambda: self.lwidget.setFinished(True))
# 		self.thread.finished.connect(lambda: self.statWidget.widget.setText("\n".join([f"{k}: {v}" for k, v in self.worker.result.items()])))
# 		self.thread.finished.connect(lambda: self.statWidget.setFinished(True))
# 		self.thread.start()
# 	

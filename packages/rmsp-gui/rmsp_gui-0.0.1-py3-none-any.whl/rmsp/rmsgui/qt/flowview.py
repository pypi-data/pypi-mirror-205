from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from rmsp.rmscore import RMSEntryType
import os


		
class RNode(QWidget):
	'''
	Draggable Widget
	'''
	def __init__(self, rmsobj, view_panel, *args, **kwargs):
		super(RNode, self).__init__(view_panel, *args, **kwargs)
		self.rmsobj = rmsobj
		self.view_panel = view_panel
		self.setFixedSize(20,20)
		self.edges = []
		self.textnodes = []
#		 self.setAttribute(Qt.WA_StyledBackground, True)
#		 self.setStyleSheet('background-color: red')
		self.selected = False
		self.assign_default_color()
		
	def assign_default_color(self):
		self.color = QColor(0,0,0,255)
	def set_color(self, r, g, b):
		self.color = QColor(r,g,b,255)
	def register_edge(self, edge):
		self.edges.append(edge)
	def register_textnode(self, textnode):
		self.textnodes.append(textnode)
		
	def _get_rnode_mask(self):
		'''
		This define the shape
		'''
		return None
	def get_center_pos(self):
		return QPoint(self.pos().x() + self.size().width() // 2, self.pos().y() + self.size().height() // 2)
	def get_contact_pos(self, other_pos):
		return self.get_center_pos()
	def resizeEvent(self, event):
		self.setMask(self._get_rnode_mask())
	def setSelected(self, selected):
		self.selected = selected
		self.update()
	
	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.view_panel.nodeSelection([self.rmsobj.get_full_id()], event.modifiers())
		self.view_panel.setFocus()
# 		if event.modifiers() == Qt.NoModifier:
# # 			self.view_panel.nodeSelection(self.rmsobj.get_full_id())
# 			self.view_panel.request_addSelection()
# 		elif event.modifiers() == Qt.ControlModifier:
# 			self.view_panel.nodeControlSelection(self.rmsobj.get_full_id())
	def mouseReleaseEvent(self, event):
		pass
	def mouseDoubleClickEvent(self, event):
		self.view_panel.requestEdit(self.rmsobj)
	def mouseMoveEvent(self, event):
		if not(event.buttons() & Qt.LeftButton):
			return
		else:
			drag = QDrag(self)

			mimedata = QMimeData()
			mimedata.setText("ABC")

			drag.setMimeData(mimedata)
			drag.setHotSpot(event.pos())
			drag.exec_(Qt.CopyAction | Qt.MoveAction)

	def moveEvent(self, event):
		for edge in self.edges:
			edge.update_edge_position()
		for textnode in self.textnodes:
			textnode.update_position()
# 	def contextMenuEvent(self, event):
# 		self.view_panel.contextMenuFromNode(event, self)


class RResource(RNode):
	def __init__(self, resource, view_panel, *args, **kwargs):
		super(RResource, self).__init__(resource, view_panel, *args, **kwargs)
		self.resource = resource
#		 self.setAttribute(Qt.WA_StyledBackground, True)
#		 self.setStyleSheet('background-color: red')
		self.setFixedSize(20,20)
		self.setToolTip(resource.rid)
	def assign_default_color(self):
		self.color = QColor(255, 0, 0, 255)
		
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(Qt.NoPen)
		if self.selected:
			self.color.setAlpha(255)
		else:
			self.color.setAlpha(100)
		if self.rmsobj.has_content:
			bs = Qt.SolidPattern
		else:
			bs = Qt.Dense3Pattern
		painter.setBrush(QBrush(self.color, bs))
		painter.drawRect(self.rect())

	def _get_rnode_mask(self):
		w = self.size().width()
		h = self.size().height()
		return QRegion(QRect(0,0,w,h),QRegion.Ellipse)

	def get_contact_pos(self, other_point):
		l = QLineF(self.get_center_pos(), other_point).length()
		if l == 0:
			return self.get_center_pos()
		ratio = self.size().width() / 2 / l
		extension = other_point - self.get_center_pos()
		return QPoint(self.get_center_pos().x() + int(extension.x() * ratio), self.get_center_pos().y() + int(extension.y() * ratio))
#	 def _get_rnode_mask(self):
#		 w = self.size().width()
#		 h = self.size().height()
#		 return QRegion(QPolygon([QPoint(w//2, 0),
#				   QPoint(w, h//2),
#				   QPoint(w//2, h),
#				   QPoint(0, h//2)]))
class RVirtualResource(RNode):
	def __init__(self, vr, view_panel, *args, **kwargs):
		super(RVirtualResource, self).__init__(vr, view_panel, *args, **kwargs)
		self.vr = vr
#		 self.setAttribute(Qt.WA_StyledBackground, True)
#		 self.setStyleSheet('background-color: red')
		self.setFixedSize(20,20)
		self.setToolTip(vr.vid)
	def assign_default_color(self):
		self.color = QColor(156, 188, 0, 255)
		
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(Qt.NoPen)
		if self.selected:
			self.color.setAlpha(255)
		else:
			self.color.setAlpha(100)
# 		if self.view_panel.controller.has_upstream([self.vr]):
		bs = Qt.SolidPattern
# 		else:
# 			bs = Qt.DiagCrossPattern
		painter.setBrush(QBrush(self.color, bs))
		painter.drawRect(self.rect())

	def _get_rnode_mask(self):
		w = self.size().width()
		h = self.size().height()
		return QRegion(QRect(0,0,w,h),QRegion.Ellipse)

	def get_contact_pos(self, other_point):
		l = QLineF(self.get_center_pos(), other_point).length()
		if l == 0:
			return self.get_center_pos()
		ratio = self.size().width() / 2 / l
		extension = other_point - self.get_center_pos()
		return QPoint(self.get_center_pos().x() + int(extension.x() * ratio), self.get_center_pos().y() + int(extension.y() * ratio))


class RTask(RNode):
	def __init__(self, task, view_panel, *args, **kwargs):
		super(RTask, self).__init__(task, view_panel, *args, **kwargs)
		self.task = task
		self.setFixedSize(20,20)
		self.setToolTip(task.tid)
	def _get_rnode_mask(self):
		w = self.size().width()
		h = self.size().height()
		return QRegion(QRect(0,0,w,h),QRegion.Ellipse)
	def get_contact_pos(self, other_point):
		l = QLineF(self.get_center_pos(), other_point).length()
		if l == 0:
			return self.get_center_pos()
		ratio = self.size().width() / 2 / l
		extension = other_point - self.get_center_pos()
		return QPoint(self.get_center_pos().x() + int(extension.x() * ratio), self.get_center_pos().y() + int(extension.y() * ratio))
	def assign_default_color(self):
		self.color = QColor(80, 80, 80, 255)
	
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(Qt.NoPen)
		if self.selected:
			self.color.setAlpha(255)
		else:
			self.color.setAlpha(100)
		bs = Qt.SolidPattern
		painter.setBrush(QBrush(self.color, bs))
		painter.drawRect(self.rect())

class RPipe(RNode):
	def __init__(self, pipe, view_panel, *args, **kwargs):
		super(RPipe, self).__init__(pipe, view_panel, *args, **kwargs)
		self.setAcceptDrops(True)
		self.pipe = pipe
#		 self.setAttribute(Qt.WA_StyledBackground, True)
#		 self.setStyleSheet('background-color: grey')
		self.setFixedSize(10,10)
		self.setToolTip(pipe.pid)
	def _get_rnode_mask(self):
		w = self.size().width()
		h = self.size().height()
		return QRegion(QRect(0,0,w,h),QRegion.Ellipse)
	def get_contact_pos(self, other_point):
		l = QLineF(self.get_center_pos(), other_point).length()
		if l == 0:
			return self.get_center_pos()
		ratio = self.size().width() / 2 / l
		extension = other_point - self.get_center_pos()
		return QPoint(self.get_center_pos().x() + int(extension.x() * ratio), self.get_center_pos().y() + int(extension.y() * ratio))
	def assign_default_color(self):
		self.color = QColor(80, 245, 80, 255)
	
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(Qt.NoPen)
		if self.selected:
			self.color.setAlpha(255)
		else:
			self.color.setAlpha(100)
# 		if self.rmsobj.ready:
# 			bs = Qt.SolidPattern
# 		else:
# 			bs = Qt.DiagCrossPattern
		bs = Qt.SolidPattern
		painter.setBrush(QBrush(self.color, bs))
		painter.drawRect(self.rect())



class RUnrunTask(RNode):
	def __init__(self, unruntask, view_panel, *args, **kwargs):
		super(RUnrunTask, self).__init__(unruntask, view_panel, *args, **kwargs)
		self.setAcceptDrops(True)
		self.unruntask = unruntask
#		 self.setAttribute(Qt.WA_StyledBackground, True)
#		 self.setStyleSheet('background-color: grey')
		self.setFixedSize(20,20)
		self.setToolTip(unruntask.uid)
	def _get_rnode_mask(self):
		w = self.size().width()
		h = self.size().height()
		return QRegion(QRect(0,0,w,h),QRegion.Ellipse)
	def get_contact_pos(self, other_point):
		l = QLineF(self.get_center_pos(), other_point).length()
		if l == 0:
			return self.get_center_pos()
		ratio = self.size().width() / 2 / l
		extension = other_point - self.get_center_pos()
		return QPoint(self.get_center_pos().x() + int(extension.x() * ratio), self.get_center_pos().y() + int(extension.y() * ratio))
	def assign_default_color(self):
		self.color = QColor(80, 245, 80, 255)
	
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(Qt.NoPen)
		if self.selected:
			self.color.setAlpha(255)
		else:
			self.color.setAlpha(100)
		if self.rmsobj.ready:
			bs = Qt.SolidPattern
		else:
			bs = Qt.DiagCrossPattern
		painter.setBrush(QBrush(self.color, bs))
		painter.drawRect(self.rect())

	def dragEnterEvent(self, event):
		# Create link from Resource or FileResource to this UnrunTask
		if isinstance(event.source(), RResource) or isinstance(event.source(), RFileResource):
			event.acceptProposedAction()
	
	def dropEvent(self, event):
		# Create link from Resource or FileResource to this UnrunTask
		if isinstance(event.source(), RResource) or isinstance(event.source(), RFileResource):
			self.view_panel.requestLinkUnrunTask(self.rmsobj, event.source().rmsobj)
			event.acceptProposedAction()



	
class RFileResource(RNode):
	def __init__(self, fileresource, view_panel, *args, **kwargs):
		super(RFileResource, self).__init__(fileresource, view_panel, *args, **kwargs)
		self.fileresource = fileresource
#		 self.setAttribute(Qt.WA_StyledBackground, True)
#		 self.setStyleSheet('background-color: blue')
		self.setToolTip(fileresource.file_path)
	def _get_rnode_mask(self):
		w = self.size().width()
		h = self.size().height()
		return QRegion(QRect(0,0,w,h),QRegion.Ellipse)
#	 def resizeEvent(self, event):
#		 self.setMask(self._get_rnode_mask())
	def get_contact_pos(self, other_point):
		l = QLineF(self.get_center_pos(), other_point).length()
		if l == 0:
			return self.get_center_pos()
		ratio = self.size().width() / 2 / l
		extension = other_point - self.get_center_pos()
		return QPoint(self.get_center_pos().x() + int(extension.x() * ratio), self.get_center_pos().y() + int(extension.y() * ratio))
	def assign_default_color(self):
		self.color = QColor(0, 0, 255, 255)
	
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(Qt.NoPen)
		if self.selected:
			self.color.setAlpha(255)
		else:
			self.color.setAlpha(100)
		bs = Qt.SolidPattern
		painter.setBrush(QBrush(self.color, bs))
		painter.drawRect(self.rect())

	def expand_above(self):
		self.expand_above()
	
	
class REdge(QWidget):
	def __init__(self, start_node, end_node, *args, **kwargs):
		super(REdge, self).__init__(*args, **kwargs)
		start_node.register_edge(self)
		end_node.register_edge(self)
		self.start_node = start_node
		self.end_node = end_node
		self.update_edge_position()
		
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.black)
		painter.setBrush(Qt.white)
		
		
		painter.drawLine(self.start_pos - self.pos(), self.end_pos - self.pos())
		painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
		poly = QPolygon([p - self.pos() for p in self.arrow_points])
		painter.drawPolygon(poly)
		
	
	def update_edge_position(self):
		start_pos = self.start_node.get_contact_pos(self.end_node.get_center_pos())
		end_pos = self.end_node.get_contact_pos(self.start_node.get_center_pos())
		angle = QLineF(end_pos, start_pos).angle()
		l1 = QLineF(end_pos, start_pos)
		l1.setAngle(angle + 30)
		l1.setLength(8)
		l2 = QLineF(end_pos, start_pos)
		l2.setAngle(angle - 30)
		l2.setLength(8)
		points = [
			QPoint(end_pos),
			l1.p2().toPoint(),
			l2.p2().toPoint(),
			]
		self.start_pos = start_pos
		self.end_pos = end_pos
		self.arrow_points = points
		xmin = min(start_pos.x(), end_pos.x(), l1.p2().toPoint().x(), l2.p2().toPoint().x())
		xmax = max(start_pos.x(), end_pos.x(), l1.p2().toPoint().x(), l2.p2().toPoint().x())
		ymin = min(start_pos.y(), end_pos.y(), l1.p2().toPoint().y(), l2.p2().toPoint().y())
		ymax = max(start_pos.y(), end_pos.y(), l1.p2().toPoint().y(), l2.p2().toPoint().y())
		self.setGeometry(xmin,
						  ymin,
						  max(xmax - xmin + 1, 1),
						  max(ymax - ymin + 1, 1))
	
class RText(QLabel):
	def __init__(self, node, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.node = node
		self.node.register_textnode(self)
	def update_position(self):
		p = self.node.get_center_pos()
		self.move(p.x(), p.y())
		
		
		
		
class RView(QWidget):
	'''
	The main view panel
	'''
	# Node/edge addition and removal
	add_node_signal = pyqtSignal(object, tuple)
	add_edge_signal = pyqtSignal(object, object)	
	remove_node_signal = pyqtSignal(object)
	remove_edge_signal = pyqtSignal(object, object)
	
	highlight_criteria_signal = pyqtSignal()
	set_color_signal = pyqtSignal(object, object, object, object)
	reset_color_signal = pyqtSignal()
	move_node_signal = pyqtSignal(object, tuple, object)
	update_node_signal = pyqtSignal(object)
	nodeSelection_signal = pyqtSignal(object, object)
# 	addSelection_signal = pyqtSignal(object)
	updateSelectionDescription_signal = pyqtSignal()
# 	removeSelection_signal = pyqtSignal(object)
# 	removeAllSelections_signal = pyqtSignal()
# 	nodeControlSelection_signal = pyqtSignal(object)
# 	nodeShiftSelection_signal = pyqtSignal(object)
	nodeRemoval_signal = pyqtSignal(object)
	nodeRemoveAll_signal = pyqtSignal()
	update_selections_signal = pyqtSignal(object)
	
	def __init__(self, controller, *args, **kwargs):
		super(RView, self).__init__(*args, **kwargs)
		self.setAcceptDrops(True)
		controller.register_view_panel(self)
		self.controller = controller
		
		self.nodes = {}
		self.selected_rmsids = set()
		self.description_holders = []
		self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
		self.rubberBand.hide()
		self.rubberBandOrigin = None
		self.initSignal()
		#self.display_settings = {"task_text_visibility": pyqtProperty(bool)}
	def initSignal(self):
		self.add_node_signal.connect(self._add_node)
		self.add_edge_signal.connect(self._add_edge)
		self.remove_node_signal.connect(self._remove_node)
		self.remove_edge_signal.connect(self._remove_edge)
		self.highlight_criteria_signal.connect(self._highlight_criteria)
		self.set_color_signal.connect(self._set_color)
		self.reset_color_signal.connect(self._reset_color)
		self.move_node_signal.connect(self._move_node)
		self.update_node_signal.connect(self._update_node)
		self.update_selections_signal.connect(self._update_selections)
		self.nodeSelection_signal.connect(self._nodeSelection)
# 		self.addSelection_signal.connect(self._addSelection)
# 		self.updateSelectionDescription_signal.connect(self._updateSelectionDescription)
# 		self.removeSelection_signal.connect(self._removeSelection)
# 		self.removeAllSelections_signal.connect(self._removeAllSelections)
# 		self.nodeControlSelection_signal.connect(self._nodeControlSelection)
# 		self.nodeShiftSelection_signal.connect(self._nodeShiftSelection)
		self.nodeRemoval_signal.connect(self._nodeRemoval)
		self.nodeRemoveAll_signal.connect(self._nodeRemoveAll)

		
	# Send request to the controller
	def requestSelectAll(self):
		self.controller.select_all()
	def requestUpdateSelections(self, rmsids):
		self.controller.update_selections(rmsids)
	def requestExpandSelectedUpstream(self, distance):
		self.controller.expandSelectedUpstream(distance)
	def requestExpandSelectedDownstream(self, distance):
		self.controller.expandSelectedDownstream(distance)
# 	def requestFetchResourceContent(self, rmsids):
# 		self.controller.auto_fetch_resource_content(rmsids)
# 	def requestExpandDownstream(self, rmsids, distance):
# 		self.controller.expandDownstream(rmsids, distance)
# 	def requestExpandUpstream(self, rmsids, distance):
# 		self.controller.expandUpstream(rmsids, distance)
# 	def requestExpandDownstreamToFile(self, rmsids, distance):
# 		self.controller.expandDownstreamToFile(rmsids, distance)
# 	def requestExpandUpstreamToFile(self, rmsids, distance):
# 		self.controller.expandUpstreamToFile(rmsids, distance)
# 	def requestExpandAll(self, rmsids, distance):
# 		self.controller.expandAll(rmsids, distance)
# 	def requestCollapseDownstream(self, rmsids, distance):
# 		self.controller.collapseDownstream(rmsids)
# 	def requestCollapseUpstream(self, rmsids, distance):
# 		self.controller.collapseUpstream(rmsids)
# 
# 	def requestDelete(self, rmsids):
# 		self.controller.delete(rmsids)
# 	def requestEdit(self, rmsobj):
# 		self.controller.edit(rmsobj)
# 	def requestAutoOrder(self):
# 		self.controller.auto_order()
	# String-based key sequences
	def requestAdd(self, rmsids, xys=None):
		self.controller.add_nodes(rmsids, xys)
	def requestRemove(self, rmsids):
		self.controller.remove_nodes(rmsids)
	def requestRemoveAll(self):
		self.controller.remove_all_nodes()
# 	def requestCreateUnrunTasksFromTasks(self, tasks, xys=None):
# 		self.controller.create_and_add_unruntasks_from_tasks(tasks, xys)
		
	def requestLinkUnrunTask(self, unruntask, rmsobj):
		self.controller.link_unruntask(unruntask, rmsobj)
	def requestRunTask(self, unruntasks):
		self.controller.run_task(unruntasks)
		
	def register_description(self, description_holder):
		self.description_holders.append(description_holder)
#######################################################################################	
	def add_node(self, rmsid, xy):
		self.add_node_signal.emit(rmsid, xy)
	def add_edge(self, rmsid1, rmsid2):
		self.add_edge_signal.emit(rmsid1, rmsid2)
	def remove_node(self, rmsid):
		self.remove_node_signal.emit(rmsid)
	def remove_edge(self, rmsid1, rmsid2):
		self.remove_edge_signal.emit(rmsid1, rmsid2)
	def update_selections(self, rmsids):
		self.update_selections_signal.emit(rmsids)
	def highlight_criteria(self):
		self.highlight_criteria_signal.emit()
	def set_color(self, rmsid, r, g, b):
		self.set_color_signal.emit(rmsid, r, g, b)
	def reset_color(self):
		self.reset_color_signal.emit()
	def move_node(self, rmsid, xy, other_rmsids=set()):
		self.move_node_signal.emit(rmsid, xy, other_rmsids)
	def update_node(self, rmsid):
		self.update_node_signal.emit(rmsid)
	def nodeSelection(self, rmsids, modifiers):
		self.nodeSelection_signal.emit(rmsids, modifiers)
		
# 	def addSelection(self, rmsid):
# 		self.addSelection_signal.emit(rmsid)
		
# 	def updateSelectionDescription(self):
# 		self.updateSelectionDescription_signal.emit()
# 	def removeSelection(self, rmsid):
# 		self.removeSelection_signal.emit(rmsid)
# 	def removeAllSelections(self):
# 		self.removeAllSelections_signal.emit()
# 	def nodeControlSelection(self, rmsid):
# 		self.nodeControlSelection_signal.emit(rmsid)
# 	def nodeShiftSelection(self, rmsid):
# 		self.nodeShiftSelection_signal.emit(rmsid)
	def nodeRemoval(self, rmsid):
		self.nodeRemoval_signal.emit(rmsid)
	def nodeRemoveAll(self):
		self.nodeRemoveAll_signal.emit()
			
		
		
		
		
		
	def _add_node(self, rmsid, xy):
		rmsobj = self.controller.get(rmsid)
		
		textobj = None
		if rmsid[0] == RMSEntryType.FILERESOURCE:
			node = RFileResource(rmsobj, self)
			textobj = RText(node, os.path.basename(rmsobj.file_path), self)
		elif rmsid[0] == RMSEntryType.RESOURCE:
			node = RResource(rmsobj, self)
		elif rmsid[0] == RMSEntryType.TASK:
			node = RTask(rmsobj, self)
			textobj = RText(node, self.controller.get((RMSEntryType.PIPE, rmsobj.pid)).func_name, self)
		elif rmsid[0] == RMSEntryType.PIPE:
			node = RPipe(rmsobj, self)
		elif rmsid[0] == RMSEntryType.UNRUNTASK:
			node = RUnrunTask(rmsobj, self)
			textobj = RText(node, self.controller.get((RMSEntryType.PIPE, rmsobj.pid)).func_name, self)
		elif rmsid[0] == RMSEntryType.VIRTUALRESOURCE:
			node = RVirtualResource(rmsobj, self)
		else:
			raise Exception()
		
		node.setGeometry(xy[0], xy[1], 30, 30)
		node.setVisible(True)
		self.nodes[rmsid] = node
		
		if textobj is not None:
			textobj.update_position()
			textobj.setVisible(True)
			
		node.update()
# 		self.updateSelectionDescription()
		
	def _add_edge(self, rmsid1, rmsid2):
		edge = REdge(self.nodes[rmsid1], self.nodes[rmsid2], self)
		edge.setVisible(True)
		edge.lower()
		
	def _remove_node(self, rmsid):
# 		self.removeSelection(rmsid)
		node = self.nodes.pop(rmsid)
		for edge in list(node.edges):
			edge.start_node.edges.remove(edge)
			edge.end_node.edges.remove(edge)
			edge.deleteLater()
		for textnode in node.textnodes:
			textnode.deleteLater()
		node.deleteLater()
		
	def _remove_edge(self, rmsid1, rmsid2):
		node = self.nodes[rmsid1]
		for edge in list(node.edges):
			if edge.end_node.rmsobj.get_full_id() == rmsid2:
				edge.start_node.edges.remove(edge)
				edge.end_node.edges.remove(edge)
				edge.deleteLater()
	
	def _highlight_criteria(self):
		pass
	def _set_color(self, rmsid, r, g, b):
		self.nodes[rmsid].set_color(r,g,b)
		self.nodes[rmsid].update()
	def _reset_color(self):
		for node in self.nodes.values():
			node.assign_default_color()
			node.update()
	def _move_node(self, rmsid, xy, other_rmsids=set()):
		relative_x = int(xy[0]) - self.nodes[rmsid].pos().x()
		relative_y = int(xy[1]) - self.nodes[rmsid].pos().y()
		self.nodes[rmsid].move(int(xy[0]), int(xy[1]))
		other_rmsids = set(other_rmsids)
		for other_rmsid in other_rmsids:
			if other_rmsid != rmsid:
				self.nodes[other_rmsid].move(self.nodes[other_rmsid].pos().x() + relative_x, 
									self.nodes[other_rmsid].pos().y() + relative_y)
	def _update_node(self, rmsid):
		self.nodes[rmsid].update()
# 		self.updateSelectionDescription()
	# Selection
	def _nodeSelection(self, rmsids, modifiers):
		if modifiers == Qt.ControlModifier:
			new_rmsids = []
			for rmsid in self.selected_rmsids:
				if rmsid not in rmsids:
					new_rmsids.append(rmsid)
			for rmsid in rmsids:
				if rmsid not in self.selected_rmsids:
					new_rmsids.append(rmsid)
			self.requestUpdateSelections(new_rmsids)
# 			self.requestUpdateSelections(set.symmetric_difference(rmsids, self.selected_rmsids))
# 			if rmsid in self.selected_rmsids:
				
# 				self.requestUpdateSelections([x for x in self.selected_rmsids if rmsid != x])
# 				self.removeSelection(rmsid)
# 			else:
# 				self.addSelection(rmsid)
# 				self.requestUpdateSelections(self.selected_rmsids + set(rmsids))
		else:
			if set(rmsids) != set(self.selected_rmsids):
				self.requestUpdateSelections(rmsids)
# 	def _addSelection(self, rmsid):
# 		if rmsid in self.selected_rmsids:
# 			return
# 		self.selected_rmsids.add(rmsid)
# 		self.nodes[rmsid].setSelected(True)
# 		self.updateSelectionDescription()
# 	def _updateSelectionDescription(self):
# 		for description_holder in self.description_holders:
# 			description_holder.update(self.selected_rmsids)
# 		if len(self.selected_rmsids) == 0:
# 			description = ""
# 		elif len(self.selected_rmsids) == 1:
# 			description = self.rmsDescriptionFormatter.format_rmsobj(self.nodes[next(iter(self.selected_rmsids))].rmsobj)
# 		else:
# 			description = f"{len(self.selected_rmsids)} nodes selected.\n" + "[" + ", ".join([f"({str(self.nodes[node].rmsobj.get_type())}, \"{str(self.nodes[node].rmsobj.get_id())}\")" for node in self.selected_rmsids]) + "]\n" 
# 		for dh in self.description_holders:
# 			dh.setText(description)
		
# 	def _removeSelection(self, rmsid):
# 		if rmsid in self.selected_rmsids:
# 			self.nodes[rmsid].setSelected(False)
# 			self.selected_rmsids.remove(rmsid)
# 			self.updateSelectionDescription()
# 	def _removeAllSelections(self):
# 		for rmsid in self.selected_rmsids:
# 			self.nodes[rmsid].setSelected(False)
# 		self.selected_rmsids.clear()
# 		self.updateSelectionDescription()
# 	def _nodeControlSelection(self, rmsid):
# 		if rmsid in self.selected_rmsids:
# 			self.removeSelection(rmsid)
# 		else:
# 			self.addSelection(rmsid)
# 	def _nodeShiftSelection(self, rmsid):
# 		raise NotImplementedError()
		
	def _nodeRemoval(self, rmsid):
		raise NotImplementedError()
	def _nodeRemoveAll(self):
		raise NotImplementedError()
		
	def _update_selections(self, rmsids):
		for rmsid in self.selected_rmsids:
			if rmsid not in rmsids:
				if rmsid in self.nodes:
					self.nodes[rmsid].setSelected(False)
		for rmsid in rmsids:
			if rmsid not in self.selected_rmsids:
				if rmsid in self.nodes:
					self.nodes[rmsid].setSelected(True)
		self.selected_rmsids = rmsids
		
		
		
###################################################
	def dragEnterEvent(self, event):
		event.acceptProposedAction()
	
		
	
	def dropEvent(self, event):
		pos = event.pos()
		if isinstance(event.source(), RNode):
			# Moving RNode
			if event.keyboardModifiers() == Qt.ControlModifier:
				if isinstance(event.source(), RTask):
					self.requestCreateUnrunTasksFromTasks(self.selected_rmsids, [(event.pos().x(), event.pos().y())])
					event.acceptProposedAction()
			elif event.keyboardModifiers() == Qt.NoModifier:
				rnode = event.source()
				qpos = event.pos() - QPoint(rnode.size().width() // 2, rnode.size().height() // 2)
				self.move_node(rnode.rmsobj.get_full_id(), (qpos.x(), qpos.y()), self.selected_rmsids)
				event.acceptProposedAction()
		else:
			# Moving selected items from 
			for i in event.source().selectedItems():
				rmsid = i.data(Qt.UserRole)
				if rmsid[0] is RMSEntryType.PIPE:
					rmsobj = self.controller.create_unruntask(rmsid[1])
				else:
					rmsobj = self.controller.get(rmsid)
				self.requestAdd([rmsobj.get_full_id()], [(event.pos().x(), event.pos().y())])
			event.acceptProposedAction()
			
	def mousePressEvent(self, event):
		'''
		Handling remove selection
		'''
		if event.button() == Qt.LeftButton:
			self.rubberBandOrigin = event.pos()
			self.rubberBand.setGeometry(QRect(self.rubberBandOrigin, QSize()))
			self.rubberBand.show();
		self.setFocus()
	def mouseMoveEvent(self, event):
		self.rubberBand.setGeometry(QRect(self.rubberBandOrigin, event.pos()).normalized())
		
	def mouseReleaseEvent(self, event):
		self.rubberBand.hide()
		rmsids = []
		for rmsid, node in self.nodes.items():
			if self.rubberBand.geometry().intersects(node.geometry()):
				rmsids.append(rmsid)
		self.nodeSelection(rmsids, event.modifiers())
		self.setFocus()
	def keyPressEvent(self, event):
		key = event.key()
		modifiers = event.modifiers()
		if modifiers == Qt.NoModifier:
			if key == Qt.Key_A:
				self.requestExpandSelectedUpstream(1)
			if key == Qt.Key_B:
				self.requestExpandSelectedDownstream(1)
		elif modifiers == Qt.ControlModifier:
			if key == Qt.Key_A:
				self.requestSelectAll()

	def contextMenuEventX(self, event):
		menu = QMenu(self)
		separator = QAction(self)
		separator.setSeparator(True)
		menu.addAction(separator)

		
		# General menu items
		# Expand
		highlightAction = QAction("Highlight (Unimplemented)", self)
		highlightAction.triggered.connect(self.highlight_criteria)
		menu.addAction(highlightAction)
		resetColorAction = QAction("Reset all colors", self)
		resetColorAction.triggered.connect(self.reset_color)
		menu.addAction(resetColorAction)
		autoOrderAction = QAction("Auto Ordering", self)
		autoOrderAction.triggered.connect(self.requestAutoOrder)
		menu.addAction(autoOrderAction)
		removeAllAction = QAction("Remove all", self)
		removeAllAction.triggered.connect(self.requestRemoveAll)
		menu.addAction(removeAllAction)
		
		
		menu.exec(event.globalPos())
		
	def contextMenuEvent(self, event):
		menu = QMenu(self)
		separator = QAction(self)
		separator.setSeparator(True)
		
		menu.addAction(separator)

		menuitems = self.controller.get_context_menu()
# 		rmsids = [rmsid for rmsid in self.selected_rmsids]
# 		rtypes = set(rmsid[0] for rmsid in rmsids)
		
		
		# General menu items
		emptyAction = QAction("Empty slot", self)
		menu.addAction(emptyAction)
		for menuitem in menuitems:
			if menuitem is None:
				separator = QAction(self)
				separator.setSeparator(True)
				menu.addAction(separator)				
			else:
				name, func, enabled = menuitem
				action = QAction(name, self)
				action.triggered.connect(lambda checked, func=func: func())
				action.setEnabled(enabled)
				menu.addAction(action)
		menu.exec(event.globalPos())
		
# #			 self.mouseTimer.start(500)
#			 if event.modifiers() == Qt.NoModifier:
#				 self.view_panel.nodeSelection(self.rmsobj.get_full_id())
#			 elif event.modifiers() == Qt.ControlModifier:
#				 self.view_panel.nodeControlSelection(self.rmsobj.get_full_id())

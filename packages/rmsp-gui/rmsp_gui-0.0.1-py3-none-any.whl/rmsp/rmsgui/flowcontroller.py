import networkx as nx
import threading
from rmsp.rmscore import RMSEntryType, RMSUpdateEvent

class RMSFlowController():
	'''
	An RMS view panel controller 
	
	The design should be independent of what GUI basis is used.
	
	All functionality that requires true GUI input/output will need to be registered.   
	
	'''
	
		
	def __init__(self, rms_interactor):
		self.rms_interactor = rms_interactor
		self.lock = threading.Lock() # The lock may need to be updated
		self.graph = nx.DiGraph() # The internal flow graph
		self.view_panels = [] # The associated view panels
		self.selection_listeners = []
		self.rmsobjs_db = {}
		self.node_selections = []
		self.rms_interactor.register_listener("rms", self.onRMSUpdate)
	######################################################
	# Registration
	######################################################
	def register_view_panel(self, view_panel):
		self.view_panels.append(view_panel)

	def register_selection_listener(self, listener):
		self.selection_listeners.append(listener)
		
	#####################################################
	# Basic Node / edge interaction
	#
	# Only node addition, update and removal is supported. 
	# Edges are automatically added.  
	#####################################################
	def add_nodes(self, rmsids, xys=None):
		'''
		Add rmsobjs if it is not present
		
		Always call udpate_nodes even if the rmsobjs are already present
		'''
		
		if xys is None:
			xys = [(0,0)] * len(rmsids)
		filtered_rmsids = [rmsid for rmsid, xy in zip(rmsids, xys) if rmsid not in self.graph]
		self.lock.acquire()
		for rmsid in filtered_rmsids: 
			self.graph.add_node(rmsid)
		self._draw_nodes(filtered_rmsids, xys)
		self._update_node_connected_edges(rmsids)
		self.lock.release()
				
	def remove_nodes(self, rmsids):
		self.lock.acquire()
		self.graph.remove_nodes_from(rmsids)
		self._erase_nodes(rmsids)
		self.lock.release()
	def remove_all_nodes(self):
		rmsids = list(self.graph.nodes)
		self.remove_nodes(rmsids)
		
	def update_selections(self, rmsids):
		if set(self.node_selections) == set(rmsids):
			return
		self.node_selections = rmsids
		self._update_selections(rmsids)
		for listener in self.selection_listeners:
			listener.onSelectionChange(self.node_selections, rmsids)
	def _update_node_connected_edges(self, rmsids):
		'''
		Update rmsobjs 
		'''
		target_rmsids = list(self.graph.nodes)
		# Refresh all edges
		existing_edges = set()
		for rmsid in rmsids:
			for rmsid1, rmsid2 in list(self.graph.out_edges(rmsid)) + list(self.graph.in_edges(rmsid)):
				existing_edges.add((rmsid1, rmsid2))
		updated_edges = set(self.rms_interactor.execute("find_direct_connections", [rmsids, target_rmsids], {}))
		self._remove_edges(existing_edges - updated_edges)
		self._add_edges(updated_edges - existing_edges)
		
		# Notify update for view panel
		#?
# 		for view_panel in self.view_panels:
# 			for rmsid in rmsids:
# 				view_panel.update_node(rmsid)
		
	def _add_edges(self, edges):
		'''
		Edge should be added automatically
		'''
		filtered_edges = []
		for rmsid1, rmsid2 in edges:
# 			if self.graph.has_node(rmsid1) and self.graph.has_node(rmsid2):
			if not self.graph.has_edge(rmsid1, rmsid2):
				self.graph.add_edge(rmsid1, rmsid2)
				filtered_edges.append([rmsid1, rmsid2])
		self._draw_edges(filtered_edges)
				
	def _remove_edges(self, edges):
		for rmsid1, rmsid2 in edges:
			if self.graph.has_edge(rmsid1, rmsid2):
				self.graph.remove_edge(rmsid1, rmsid2)
		self._erase_edges(edges)
			
	
	
	
	def _draw_nodes(self, rmsobjs, xys=None):
		for rmsobj, xy in zip(rmsobjs, xys):
			for view_panel in self.view_panels:
				view_panel.add_node(rmsobj, xy)

	def _draw_edges(self, rmsid_pairs):
		for view_panel in self.view_panels:
			for rmsid_pair in rmsid_pairs:
				view_panel.add_edge(rmsid_pair[0], rmsid_pair[1])
		
	def _erase_nodes(self, rmsids):
		for view_panel in self.view_panels:
			for rmsid in rmsids:
				view_panel.remove_node(rmsid)
	def _erase_edges(self, rmsid_pairs):
		for view_panel in self.view_panels:
			for rmsid_pair in rmsid_pairs:
				view_panel.remove_edge(rmsid_pair[0], rmsid_pair[1])
				
	def _update_selections(self, rmsids):
		for view_panel in self.view_panels:
			view_panel.update_selections(rmsids)
		
	def get(self, rmsid):
		return self.rms_interactor.execute("get", [rmsid])
	
	
	def select_all(self):
		self.update_selections(list(self.graph))
	def removeSelected(self):
		self.remove_nodes(self.node_selections)
	def expandSelectedUpstream(self, distance=-1):
		self.expandUpstream(self.node_selections, distance)
	def expandSelectedDownstream(self, distance=-1):
		self.expandDownstream(self.node_selections, distance)
	def expandDownstream(self, rmsids, distance=-1):
		if len(rmsids) > 0:
			self.add_nodes(self.rms_interactor.execute("find_connected_nodes", [rmsids, "downstream", distance]))
			self.auto_order()
	def expandUpstream(self, rmsids, distance=-1):
		if len(rmsids) > 0:
			self.add_nodes(self.rms_interactor.execute("find_connected_nodes", [rmsids, "upstream", distance]))
			self.auto_order()
	def expandDownstreamToFile(self, rmsids, distance=-1):
		self.add_nodes(self.rms_interactor.execute("find_connected_nodes", [rmsids, "downstream", distance, "f"]))
		self.auto_order()
	def expandUpstreamToFile(self, rmsids, distance=-1):
		self.add_nodes(self.rms_interactor.execute("find_connected_nodes", [rmsids, "upstream", distance, "f"]))
		self.auto_order()
	def expandAll(self, rmsids, distance=-1):
		self.add_nodes(self.rms_interactor.execute("find_connected_nodes", [rmsids, "all", distance]))
		self.auto_order()
	def collapseDownstream(self, args):
		'''
		Collapse any downstream nodes, except those with other parents 
		'''
		nodes_to_collapse = set(args)
		while len(nodes_to_collapse) > 0:
			out_nodes = set(edge[1] for node in nodes_to_collapse for edge in self.graph.out_edges(node))
			self.remove_nodes(nodes_to_collapse)
			nodes_to_collapse = set(node for node in out_nodes if len(self.graph.in_edges(node)) == 0)
# 	def collapseUpstream(self, args, distance=-1):
# 		self.add_nodes(self.rms.find_upstream_objs(args, distance))
# 		self.auto_order()
		
	def move_node(self, rmsid, xy):
		for view_panel in self.view_panels:
			view_panel.move_node(rmsid, xy)
	def highlight_nodes(self, rmsobjs, r, g, b):
		for view_panel in self.view_panels:
			for rmsobj in rmsobjs:
				view_panel.set_color(rmsobj.get_full_id(), r, g, b)
	def reset_color(self):
		for view_panel in self.view_panels:
			view_panel.reset_color()
	def auto_order(self):
		'''
		Organize the nodes on the board. 
		'''
		w = 500
		h = 500
		xmargin = 100
		ymargin = 100
		if len(self.graph.nodes) == 0:
			return
		self.lock.acquire()
		auto_positions = {(RMSEntryType(int(dn.split("_")[0])), dn.split("_")[1]):v for dn, v in nx.nx_pydot.pydot_layout(nx.relabel_nodes(self.graph, lambda k: "_".join([str(k[0].value), k[1]]), copy=True), prog="dot").items()}
#		 auto_positions = nx.drawing.nx_pydot.graphviz_layout(self.graph)
		xmin = min(xy[0] for xy in auto_positions.values())
		xmax = max(xy[0] for xy in auto_positions.values())
		ymin = min(xy[1] for xy in auto_positions.values())
		ymax = max(xy[1] for xy in auto_positions.values())
		xfactor = w / (xmax - xmin) if xmax != xmin else 0
		yfactor = h / (ymax - ymin) if ymax != ymin else 0
		new_auto_positions = {key:((xy[0] - xmin) * xfactor + xmargin, h - ((xy[1] - ymin) * yfactor) + ymargin) for key, xy in auto_positions.items()}
		for rmsid, xy in new_auto_positions.items():
			self.move_node(rmsid, xy)
		self.lock.release()
	def get_context_menu(self):
		nodes_selected = len(self.node_selections) > 0
		nodes_exist = len(self.graph) > 0
		# Expand
		return [
			["Expand Upstream", self.expandSelectedUpstream, nodes_selected],
			["Expand Downstream", self.expandSelectedDownstream, nodes_selected],
			None,
			["Remove", self.removeSelected, nodes_selected],
			["Remove all", self.remove_all_nodes, nodes_exist],
			None,
			["Delete", lambda rmsids=self.node_selections: self.rms_actioner.confirm_and_delete(rmsids), nodes_selected],
		]
# 		expandAllAction = QAction("Expand all", self)
# 		expandAllAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestExpandAll(rmsids, -1))
# 		menu.addAction(expandAllAction)
# 		expandUpstreamAction = QAction("Expand upstream", self)
# 		expandUpstreamAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestExpandUpstream(rmsids, -1))
# 		menu.addAction(expandUpstreamAction)
# 		expandDownstreamAction = QAction("Expand downstream", self)
# 		expandDownstreamAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestExpandDownstream(rmsids, -1))
# 		menu.addAction(expandDownstreamAction)
# 		
# 		expandOneUpstreamAction = QAction("Expand upstream 1", self)
# 		expandOneUpstreamAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestExpandUpstream(rmsids, 1))
# 		menu.addAction(expandOneUpstreamAction)
# 		expandOneDownstreamAction = QAction("Expand downstream 1", self)
# 		expandOneDownstreamAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestExpandDownstream(rmsids, 1))
# 		menu.addAction(expandOneDownstreamAction)
# 
# 		expandUpstreamToFileAction = QAction("Expand upstream to file", self)
# 		expandUpstreamToFileAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestExpandUpstreamToFile(rmsids, -1))
# 		menu.addAction(expandUpstreamToFileAction)
# 		expandDownstreamToFileAction = QAction("Expand downstream to file", self)
# 		expandDownstreamToFileAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestExpandDownstreamToFile(rmsids, -1))
# 		menu.addAction(expandDownstreamToFileAction)
# 		
# 		collapseUpstreamAction = QAction("Collapse upstream", self)
# 		collapseUpstreamAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestCollapseUpstream(rmsids, -1))
# 		menu.addAction(collapseUpstreamAction)
# 		collapseDownstreamAction = QAction("Collapse downstream", self)
# 		collapseDownstreamAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestCollapseDownstream(rmsids, -1))
# 		menu.addAction(collapseDownstreamAction)
# 
# 		removeAction = QAction("Remove", self)
# 		removeAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestRemove(rmsids))
# 		menu.addAction(removeAction)
# 		separator = QAction(self)
# 		separator.setSeparator(True)
# 		menu.addAction(separator)
# 		# Delete
# 		deleteAction = QAction("Delete", self)
# 		deleteAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestDelete(rmsids))
# 		menu.addAction(deleteAction)
# 
# 		separator = QAction(self)
# 		separator.setSeparator(True)
# 		menu.addAction(separator)
# 		
# # 		createRunChainAction = QAction("Create pipe to generate this", self)
# # 		deleteAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestCREATE(rmsids))
# # 		menu.addAction(deleteAction)
# 		
# 		separator = QAction(self)
# 		separator.setSeparator(True)
# 		menu.addAction(separator)
# 		
# 		fetchAction = QAction("Fetch content", self)
# 		fetchAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestFetchResourceContent(rmsids))
# 		menu.addAction(fetchAction)
# 		fetchAction.setEnabled(RMSEntryType.RESOURCE in rtypes)
# 		
# 		runTaskAction = QAction("Run task", self)
# 		runTaskAction.triggered.connect(lambda checked, rmsids=rmsids: self.requestRunTask(rmsids))
# 		menu.addAction(runTaskAction)
# 		runTaskAction.setEnabled(RMSEntryType.UNRUNTASK in rtypes)
# 		
# 	def create_and_add_unruntasks_from_tasks(self, rmsobjs, xys=None):
# 		print(rmsobjs)
# 		new_rmsobjs = self.rms.create_unruntask_chain(rmsobjs)
# 		self.add_nodes(new_rmsobjs)
# 		self.auto_order()
# # 		unruntasks = [self.create_unruntask_from_task(task) for task in rmsobjs]
# # 		self.add_nodes(unruntasks, xys)
# 
# 	def link_unruntask(self, unruntask, rmsobj):
# 		
# 		super().link_unruntask(unruntask, rmsobj)
# 		self.update_nodes([unruntask])

# 	def execute_template(self, func, arguments):
# 		'''
# 		Similar to the upstream, except the callback_func
# 		'''
# 		ba = inspect.signature(func).bind_partial()
# 		for k, v in arguments.items():
# 			ba.arguments[k] = v
# 		builder = self.rms.rmsb
# 		ba.arguments['rmsp'] = builder
# 		def callback_func(state, r, begin_time, end_time, pid, builder=builder, rmscontroller=self):
# 			if state == ProcessWrapState.COMPLETE:
# 				# Add more 
# 				unruntasks = builder.execute_builder()
# 				connected_resources = list(rmscontroller.rms.find_connected_objs(unruntasks, distance=1))
# 				rmscontroller.add_nodes(unruntasks + connected_resources)
# # 				rmscontroller._thread_update_nodes_signal.emit(unruntasks + connected_resources)
# 				
# 			else:
# 				# display_warning message()
# 				pass
# 		pw = ProcessWrap(func, args=ba.args, kwargs=ba.kwargs, callback=callback_func, use_thread=True)
# 		pw.start()
	
	def onRMSUpdate(self, events):
		delete_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.DELETE]
		insert_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.INSERT]
		modify_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.MODIFY]
		replace_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.REPLACE]
		
		to_insert_rmsids = []
		to_remove_rmsids = []
		for rmsid in replace_rmsids:
			if rmsid in self.graph:
				to_insert_rmsids.append(self.rms_interactor.execute("get", args=[rmsid]).replacement.get_full_id())
				to_remove_rmsids.append(rmsid)
		self.add_nodes(to_insert_rmsids)
		self.remove_nodes(to_remove_rmsids + delete_rmsids)
		self.auto_order()
			
	def onRMSUpdateOld(self, events):

# 		for log_func in self.log_funcs:
# 			for event, rmsid in events:
# 				if event == RMSUpdateEvent.DELETE:
# 					#if rmsid[0] == RMSEntryType.TASK:
# 					ss = str(rmsid[0])
# 					msg = f"A {ss} is deleted: {rmsid[1]}"
# 				else:
# 					rmsobj = self.rms.get(rmsid)
# 					msg = str(event) + str(rmsid)
# 					if event == RMSUpdateEvent.INSERT:
# 						if rmsobj.get_type() == RMSEntryType.TASK:
# 							msg = f"A task is complete. {rmsobj.get_id()}"
# 						if rmsobj.get_type() == RMSEntryType.FILERESOURCE:
# 							msg = f"New file is added: {rmsobj.file_path} {rmsobj.get_id()}"
# 				log_func(msg)
		
		# Logic
		# If a task is inserted, and the an associated unruntask is present in the graph
# 		events = list(filter(lambda er: er[1] in self.graph, events))

		delete_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.DELETE]
		insert_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.INSERT]
		modify_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.MODIFY]
		contentchange_rmsids = [rmsid for event, rmsid in events if event == RMSUpdateEvent.CONTENTCHANGE]
		
		# Only care about those on the board
		delete_rmsids = [delete_rmsid for delete_rmsid in delete_rmsids if delete_rmsid in self.graph]
		
		to_insert_rmsids = []
# 		for rmsid in delete_rmsids:
# 			if rmsid[0] == RMSEntryType.VIRTUALRESOURCE:
# 				#if self.rmsobjs_db[rmsid].replacement.get_full_id() in insert_rmsids:
# 				if self.rmsobjs_db[rmsid].replacement is not None:
# 					to_insert.append(self.rmsobjs_db[rmsid].replacement)
# 			elif rmsid[0] == RMSEntryType.UNRUNTASK:
# 				if self.rmsobjs_db[rmsid].replacement is not None:
# 					to_insert.append(self.rmsobjs_db[rmsid].replacement)
		
		current_rmsids = set([rmsid for rmsid in self.graph.nodes if rmsid not in delete_rmsids])
		related_insert_rmsids = set()
		latest_added_rmsids = current_rmsids
		
		while len(latest_added_rmsids) > 0:
			remaining_rmsids = [rmsid for rmsid in insert_rmsids if rmsid not in related_insert_rmsids]
			dcns = self.rms_interactor.execute("filter_directly_connected_nodes", remaining_rmsids, latest_added_rmsids)
			related_insert_rmsids.update(dcns) 
			latest_added_rmsids = dcns
		
		to_insert_rmsids.extend(related_insert_rmsids)
		
				
		self.update_nodes(modify_rmsids)
		self.remove_nodes(delete_rmsids)
		
# 		for rmsobj in to_insert:
# 			if rmsobj.get_type() == RMSEntryType.TASK:
# 				to_insert.extend(rmsobj.output_fileresources)
# 				to_insert.extend(rmsobj.output_resources)
# 		self.add_nodes(to_insert)
# 		
# 		for view_panel in self.view_panels:
# 			for rmsid in contentchange_rmsids:
# 				view_panel.update_node(rmsid)
# 		
		if len(to_insert_rmsids) > 0 or len(delete_rmsids) > 0:
			self.auto_order()
		
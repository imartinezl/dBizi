function JupyterCommManager() {
}

JupyterCommManager.prototype.register_target = function(plot_id, comm_id, msg_handler) {
  if (window.comm_manager || ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null))) {
	var comm_manager = window.comm_manager || Jupyter.notebook.kernel.comm_manager;
	comm_manager.register_target(comm_id, function(comm) {
	  comm.on_msg(msg_handler);
	});
  } else if ((plot_id in window.PyViz.kernels) && (window.PyViz.kernels[plot_id])) {
	window.PyViz.kernels[plot_id].registerCommTarget(comm_id, function(comm) {
	  comm.onMsg = msg_handler;
	});
  }
}

JupyterCommManager.prototype.get_client_comm = function(plot_id, comm_id, msg_handler) {
  if (comm_id in window.PyViz.comms) {
	return window.PyViz.comms[comm_id];
  } else if (window.comm_manager || ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null))) {
	var comm_manager = window.comm_manager || Jupyter.notebook.kernel.comm_manager;
	var comm = comm_manager.new_comm(comm_id, {}, {}, {}, comm_id);
	if (msg_handler) {
	  comm.on_msg(msg_handler);
	}
  } else if ((plot_id in window.PyViz.kernels) && (window.PyViz.kernels[plot_id])) {
	var comm = window.PyViz.kernels[plot_id].connectToComm(comm_id);
	comm.open();
	if (msg_handler) {
	  comm.onMsg = msg_handler;
	}
  }

  window.PyViz.comms[comm_id] = comm;
  return comm;
}

window.PyViz.comm_manager = new JupyterCommManager();
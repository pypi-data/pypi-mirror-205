# Resource Management System (RMS) GUI Manual

The package provides GUI support to the `rmsp` package. 

## Installation

```
pip install rmsp-gui
```

## Quick start

To start the RMS set up:

```python
DBPATH = "/path/to/db/"
DBNAME = "test.db"
DBRESDIR = "Resources/"
LIBPATH = f"{DBPATH}RMSLibrary/"
import sys
import logging
logger = logging.getLogger("rmspool")
logger.setLevel("INFO")
logger.addHandler(logging.StreamHandler(sys.stdout))

# RMS Core
from rmsp import rmscore
from rmsp import rmsbuilder
from rmsp.rmstemplate import RMSTemplateLibrary
rms = rmscore.ResourceManagementSystem(f"{DBPATH}{DBNAME}", f"{DBPATH}{DBRESDIR}")
rmspool = rmsbuilder.RMSProcessWrapPool(rms, 1)
rmsb = rmsbuilder.RMSUnrunTasksBuilder(rmspool)
rmstlib = RMSTemplateLibrary(rmsb, LIBPATH)

# Interactor
from rmsp.rmsinteractor import RMSPoolInteractionCore, RMSInteractionCore, RMSTemplateLibraryInteractionCore
from rmsp.interactorhelper import LocalInteractor
rms_interactor = LocalInteractor(RMSInteractionCore(rms))
rmspool_interactor = LocalInteractor(RMSPoolInteractionCore(rmspool))
rmstemplatelib_interactor = LocalInteractor(RMSTemplateLibraryInteractionCore(rmstlib))

```



#### Starting GUI in jupyter

```python
%gui qt5

from rmsp.rmsgui.qt.mainapp import RMSWindow
win = RMSWindow(rms_interactor, rmspool_interactor, rmstemplatelib_interactor)
win.showMaximized()


```

#### Starting GUI in python script

```python
from PyQt5.QtWidgets import QApplication
app = QApplication([])

from rmsp.rmsgui.qt.mainapp import RMSWindow
win = RMSWindow(rms_interactor, rmspool_interactor, rmstemplatelib_interactor)
win.showMaximized()

app.exec()
```



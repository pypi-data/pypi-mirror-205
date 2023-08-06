"""X-Socs new project wizard"""

import os
from functools import partial

from silx.gui import qt as Qt
from silx.gui import icons

from .FileChooser import FileChooser
from ..widgets.Containers import GroupBox
from ..process.MergeWidget import MergeWidget
from ..project.XsocsProject import XsocsProject
from .ProjectChooser import ProjectSummaryWidget


class XsocsWizard(Qt.QWizard):
    """New project wizard class"""

    (CreateId, SelectDataId, LoadXsocsId, ReviewId) = range(4)

    def __init__(self, parent=None):
        super(XsocsWizard, self).__init__(parent)

        self.__projectFile = None

        self.setPage(XsocsWizard.CreateId, NewProjectPage())
        self.setPage(XsocsWizard.SelectDataId, SelectDataPage())
        self.setPage(XsocsWizard.LoadXsocsId, LoadXsocsDataPage())
        self.setPage(XsocsWizard.ReviewId, ReviewProjectPage())

    projectFile = property(lambda self: self.__projectFile)

    @projectFile.setter
    def projectFile(self, projectFile):
        self.__projectFile = projectFile


class _BaseWizardPage(Qt.QWizardPage):
    """Base class for new project wizard pages"""

    def __init__(self, parent=None):
        super(_BaseWizardPage, self).__init__(parent)
        self.setTitle("X-Socs")

        icon = icons.getQPixmap("xsocs:gui/icons/xsocs")
        self.setPixmap(Qt.QWizard.WatermarkPixmap, icon)
        icon = icons.getQPixmap("xsocs:gui/icons/logo")
        self.setPixmap(Qt.QWizard.LogoPixmap, icon)


class LoadXsocsDataPage(_BaseWizardPage):
    """Create project from HDF5 file page"""

    def __init__(self, parent=None):
        super(LoadXsocsDataPage, self).__init__(parent)

        self.setSubTitle("New project: Load X-Socs data (HDF5).")

        layout = Qt.QVBoxLayout(self)

        group = GroupBox("Please select the X-Socs data file to load.")
        layout.addWidget(group)
        grpLayout = Qt.QHBoxLayout(group)
        filePicker = FileChooser(fileMode=Qt.QFileDialog.ExistingFile)
        grpLayout.addWidget(filePicker)

        self.registerField("XsocsDataFile*", filePicker.lineEdit)

    def nextId(self):
        return XsocsWizard.ReviewId

    def validatePage(self):
        projectFile = self.wizard().projectFile
        xsocsFile = self.wizard().field("XsocsDataFile")

        try:
            projectH5 = XsocsProject(projectFile, mode="a", gui=self)
        except Exception as ex:
            Qt.QMessageBox.critical(self, "Failed to open project file.", str(ex))
            return False

        try:
            projectH5.xsocsFile = xsocsFile
        except Exception as ex:
            Qt.QMessageBox.critical(self, "Failed to set data file.", str(ex))
            return False
        self.setCommitPage(True)
        return True


class SelectDataPage(_BaseWizardPage):
    """Choose between create project from HDF5 or from SPEC+EDF"""

    def __init__(self, parent=None):
        super(SelectDataPage, self).__init__(parent)

        self.setSubTitle("New project: Select data to load/import.")
        self.setTitle("Select input data.")

        self.__nextId = -1

        layout = Qt.QGridLayout(self)
        icon = icons.getQIcon("xsocs:gui/icons/logo")
        xsocsBn = Qt.QToolButton()
        xsocsBn.setIcon(icon)
        layout.addWidget(xsocsBn, 1, 1)
        layout.addWidget(Qt.QLabel("Load X-Socs Data (HDF5)."), 1, 2)

        icon = icons.getQIcon("xsocs:gui/icons/spec")
        specBn = Qt.QToolButton()
        specBn.setIcon(icon)
        layout.addWidget(specBn, 2, 1)
        layout.addWidget(Qt.QLabel("Import SPEC data."), 2, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(3, 1)
        layout.setColumnStretch(3, 1)

        xsocsBn.clicked.connect(partial(self.__buttonClicked, source="XSOCS"))
        specBn.clicked.connect(partial(self.__buttonClicked, source="SPEC"))

    def nextId(self):
        return self.__nextId

    def isComplete(self):
        return False

    def initializePage(self):
        self.setCommitPage(False)

    def __buttonClicked(self, source=None):
        self.__nextId = -1
        if source == "XSOCS":
            self.__nextId = XsocsWizard.LoadXsocsId
        if source == "SPEC":
            outputDir = os.path.dirname(self.wizard().projectFile)
            mergeWid = MergeWidget(parent=self, output_dir=outputDir)
            if mergeWid.exec_() == Qt.QDialog.Accepted:
                xsocsH5 = mergeWid.xsocsH5
                mergeWid.deleteLater()

                if xsocsH5 is not None:
                    projectFile = self.wizard().projectFile
                    try:
                        projectH5 = XsocsProject(projectFile, mode="a")
                    except Exception as ex:
                        Qt.QMessageBox.critical(
                            self, "Failed to open project file.", str(ex)
                        )
                        return

                    try:
                        projectH5.xsocsFile = xsocsH5
                    except Exception as ex:
                        Qt.QMessageBox.critical(
                            self, "Failed to set data file.", str(ex)
                        )
                        return

                    self.__nextId = XsocsWizard.ReviewId
                    self.setCommitPage(True)

        if self.__nextId != -1:
            self.wizard().next()


class ReviewProjectPage(_BaseWizardPage):
    """Last wizard page with project summary"""

    def __init__(self, parent=None):
        super(ReviewProjectPage, self).__init__(parent)

        self.setSubTitle("New project created.")

        layout = Qt.QVBoxLayout(self)
        group = GroupBox("Project Summary")
        layout.addWidget(group)
        grpLayout = Qt.QVBoxLayout(group)
        view = ProjectSummaryWidget()
        grpLayout.addWidget(view)

    def initializePage(self):
        """Fills the AcqParamWidget with info found in the input file"""
        view = self.findChild(ProjectSummaryWidget)
        view.setProjectFile(self.wizard().projectFile)

    def nextId(self):
        return -1


class NewProjectPage(_BaseWizardPage):
    """Select folder for new project page"""

    def __init__(self, parent=None):
        super(NewProjectPage, self).__init__(parent)
        layout = Qt.QVBoxLayout(self)

        self.setSubTitle("New project : select a project directory.")

        self.__selectedPath = ""

        group = GroupBox("Create new project into...")
        layout.addWidget(group)

        grpLayout = Qt.QHBoxLayout(group)
        filePicker = FileChooser(
            fileMode=Qt.QFileDialog.Directory,
            appendPath=os.path.sep + "xsocs.prj",
            options=Qt.QFileDialog.ShowDirsOnly,
        )
        filePicker.sigSelectionChanged.connect(self.__filePicked)
        grpLayout.addWidget(filePicker)

    def __filePicked(self, selectedPath):
        self.__selectedPath = selectedPath
        self.completeChanged.emit()

    def isComplete(self):
        return len(self.__selectedPath) > 0

    def validatePage(self):
        if not self.__selectedPath:
            return False

        if os.path.exists(self.__selectedPath):
            buttons = Qt.QMessageBox.Yes | Qt.QMessageBox.Cancel
            ans = Qt.QMessageBox.warning(
                self,
                "Overwrite?",
                (
                    "This folder already contains a"
                    " project.\n"
                    "Are you sure you want to "
                    "overwrite it?"
                ),
                buttons=buttons,
            )
            if ans == Qt.QMessageBox.Cancel:
                return False
        try:
            XsocsProject(self.__selectedPath, mode="w")
        except Exception as ex:
            Qt.QMessageBox.critical(self, "Failed to create file.", str(ex))
            return False
        self.wizard().projectFile = self.__selectedPath
        return True

    def nextId(self):
        return XsocsWizard.SelectDataId

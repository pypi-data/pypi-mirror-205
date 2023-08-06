import uuid

from qtpy.QtWidgets import QMessageBox

from ert._c_wrappers.enkf.enums.realization_state_enum import RealizationStateEnum
from ert.analysis import ErtAnalysisError, ESUpdate
from ert.gui.ertwidgets import resourceIcon
from ert.gui.ertwidgets.closabledialog import ClosableDialog
from ert.gui.tools import Tool
from ert.gui.tools.run_analysis import RunAnalysisPanel


def analyse(ert, target_fs, source_fs):
    """Runs analysis using target and source cases. Returns whether or not
    the analysis was successful."""
    es_update = ESUpdate(ert)

    for iens in (
        i
        for i, s in enumerate(source_fs.state_map)
        if s
        in (
            RealizationStateEnum.STATE_LOAD_FAILURE,
            RealizationStateEnum.STATE_UNDEFINED,
        )
    ):
        target_fs.state_map[iens] = RealizationStateEnum.STATE_PARENT_FAILURE
    es_update.smootherUpdate(source_fs, target_fs, str(uuid.uuid4()))


class RunAnalysisTool(Tool):
    def __init__(self, ert, notifier):
        self.ert = ert
        self.notifier = notifier
        super().__init__(
            "Run analysis", "tools/run_analysis", resourceIcon("formula.svg")
        )
        self._run_widget = None
        self._dialog = None
        self._selected_case_name = None

    def trigger(self):
        if self._run_widget is None:
            self._run_widget = RunAnalysisPanel(self.ert, self.notifier)
        self._dialog = ClosableDialog("Run analysis", self._run_widget, self.parent())
        self._dialog.addButton("Run", self.run)
        self._dialog.exec_()

    def run(self):
        target = self._run_widget.target_case()
        source_fs = self._run_widget.source_case()

        if len(target.strip()) == 0:
            self._report_empty_target()
            return

        target_fs = self.notifier.storage.create_ensemble(
            source_fs.experiment_id,
            name=target,
            ensemble_size=source_fs.ensemble_size,
            iteration=source_fs.iteration + 1,
            prior_ensemble=source_fs,
        )

        try:
            analyse(self.ert, target_fs, source_fs)
            error = None
        except ErtAnalysisError as e:
            error = str(e)
        except Exception as e:
            error = f"Uknown exception occured with error: {str(e)}"

        msg = QMessageBox()
        msg.setWindowTitle("Run analysis")
        msg.setStandardButtons(QMessageBox.Ok)

        if not error:
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Successfully ran analysis for case '{source_fs.name}'.")
            msg.exec_()
        else:
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                f"Unable to run analysis for case '{source_fs.name}'.\n"
                f"The following error occured: {error}"
            )
            msg.exec_()
            return

        self.notifier.ertChanged.emit()
        self._dialog.accept()

    def _report_empty_target(self):
        msg = QMessageBox()
        msg.setWindowTitle("Invalid target")
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Target case can not be empty")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

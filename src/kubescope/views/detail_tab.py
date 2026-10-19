import json
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from kubescope.models import (
    DetailRow,
    detail_sections,
    format_cpu,
    format_memory,
    safe_file_name,
)
from kubescope.theme import themed_stylesheet
from kubescope.utils.fonts import code_font
from kubescope.utils.json_view import style_json_view
from kubescope.views.widgets import LineNumberEditor, UsageChart

USAGE_REFRESH_MS = 5000
_STYLE = """
QLabel#sectionTitle { font-size: 16px; font-weight: 600; color: #16375f; }
QLabel#subTitle { font-size: 13px; font-weight: 600; color: #4f5966; }
QLabel#rowLabel { color: #4f5966; }
QLabel#rowValue { color: #20232a; }
QLabel#chip { color: #20232a; background: #f3f4f7; border: 1px solid #e1e3e9;
              border-radius: 4px; padding: 2px 8px; }
QLabel#note { color: #6b7380; }
QFrame#rowLine { background: #e1e3e9; max-height: 1px; border: none; }
"""


class DetailTab(QWidget):
    """The details of a resource: an overview laid out in sections (with the
    live usage of a Pod) and the raw JSON, one click apart."""

    def __init__(
        self, title: str, document: dict[str, Any], live_usage: bool = False
    ) -> None:
        super().__init__()
        self.document = document
        self.save_name = safe_file_name(title, ".json")
        self.busy = False
        self.closed = False

        self.editor = LineNumberEditor()
        self.editor.setReadOnly(True)
        self.editor.setFont(code_font())
        self.editor.setLineWrapMode(LineNumberEditor.LineWrapMode.NoWrap)
        self.highlighter = style_json_view(self.editor)
        self.editor.setPlainText(json.dumps(document, ensure_ascii=False, indent=2))

        self.cpu_chart = UsageChart(self.tr("CPU"), format_cpu)
        self.memory_chart = UsageChart(self.tr("Memory"), format_memory)
        self.usage_note = QLabel()
        self.usage_note.setObjectName("note")
        self.usage_box = QWidget()
        self.usage_box.setVisible(live_usage)

        self.overview = QScrollArea()
        self.overview.setWidgetResizable(True)
        self.overview.setFrameShape(QFrame.Shape.NoFrame)
        self.content = self._build_overview()
        self.overview.setWidget(self.content)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.overview)
        self.stack.addWidget(self.editor)

        self.overview_button = QPushButton(self.tr("Overview"))
        self.raw_button = QPushButton(self.tr("Raw JSON"))
        for index, button in enumerate((self.overview_button, self.raw_button)):
            button.setCheckable(True)
            button.setAutoExclusive(True)
            button.setProperty("variant", "secondary")
            button.clicked.connect(lambda _checked=False, i=index: self.show_page(i))
        header = QHBoxLayout()
        header.addWidget(self.overview_button)
        header.addWidget(self.raw_button)
        header.addStretch()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(header)
        layout.addWidget(self.stack)
        self.show_page(0)
        self.restyle()

    def show_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        self.overview_button.setChecked(index == 0)
        self.raw_button.setChecked(index == 1)

    @property
    def showing_raw(self) -> bool:
        return self.stack.currentIndex() == 1

    def restyle(self) -> None:
        self.content.setStyleSheet(themed_stylesheet(_STYLE))
        self.cpu_chart.update()
        self.memory_chart.update()

    def add_usage(self, usage: tuple[float, float] | None) -> None:
        """Add a sample to the charts; None says metrics-server has none."""
        if usage is None:
            self.cpu_chart.setVisible(False)
            self.memory_chart.setVisible(False)
            self.usage_note.setText(
                self.tr("Live usage needs metrics-server in the cluster.")
            )
            return
        self.cpu_chart.setVisible(True)
        self.memory_chart.setVisible(True)
        self.usage_note.setText(
            self.tr("Live usage from the Kubernetes Metrics Server")
        )
        self.cpu_chart.add_sample(usage[0])
        self.memory_chart.add_sample(usage[1])

    def _build_overview(self) -> QWidget:
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 12, 24)
        layout.setSpacing(0)
        usage = QVBoxLayout(self.usage_box)
        usage.setContentsMargins(0, 0, 0, 12)
        usage.addWidget(self._title(self.tr("Metrics")))
        usage.addWidget(self.usage_note)
        usage.addWidget(self.cpu_chart)
        usage.addWidget(self.memory_chart)
        layout.addWidget(self.usage_box)
        for section in detail_sections(self.document):
            indent = 0 if section.level == 1 else 16
            title = self._title(self._section_title(section.title), section.level)
            layout.addWidget(title)
            body = QVBoxLayout()
            body.setContentsMargins(indent, 0, 0, 0)
            body.setSpacing(0)
            for row in section.rows:
                body.addWidget(self._line())
                body.addLayout(self._row(row))
            layout.addLayout(body)
        layout.addStretch()
        return content

    def _section_title(self, title: str) -> str:
        return {
            "Properties": self.tr("Properties"),
            "Spec": self.tr("Spec"),
            "Status": self.tr("Status"),
            "Data": self.tr("Data"),
        }.get(title, title)

    @staticmethod
    def _title(text: str, level: int = 1) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sectionTitle" if level == 1 else "subTitle")
        label.setContentsMargins(0, 22 if level == 1 else 14, 0, 8)
        return label

    @staticmethod
    def _line() -> QFrame:
        line = QFrame()
        line.setObjectName("rowLine")
        line.setFixedHeight(1)
        return line

    def _row(self, row: DetailRow) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(16)
        label = QLabel(row.label)
        label.setObjectName("rowLabel")
        label.setToolTip(row.label)
        label.setFixedWidth(260)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(label)
        layout.addLayout(self._value(row), 1)
        return layout

    def _value(self, row: DetailRow) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        if row.table:
            layout.addWidget(self._table(row))
            return layout
        for value in row.values:
            label = QLabel(value)
            label.setObjectName("chip" if len(row.values) > 1 else "rowValue")
            # wrapping every label makes Qt size short ones too tightly
            label.setWordWrap(len(value) > 60 or "\n" in value)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(label, 0, Qt.AlignmentFlag.AlignLeft)
        return layout

    @staticmethod
    def _table(row: DetailRow) -> QTableWidget:
        table = QTableWidget(len(row.table), len(row.headers))
        table.setHorizontalHeaderLabels(row.headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        table.setWordWrap(False)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        header = table.horizontalHeader()
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        header.setFixedHeight(32)
        table.verticalHeader().setDefaultSectionSize(30)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        for y, cells in enumerate(row.table):
            for x, cell in enumerate(cells):
                table.setItem(y, x, QTableWidgetItem(cell))
        table.resizeColumnsToContents()
        header.setStretchLastSection(True)
        scrollbar = table.horizontalScrollBar().sizeHint().height()
        table.setFixedHeight(32 + 30 * table.rowCount() + scrollbar + 4)
        return table

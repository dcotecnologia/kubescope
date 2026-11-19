from typing import Any, cast

from PySide6.QtCore import QEvent
from PySide6.QtGui import QPixmap

from kubescope.utils.artifacthub import CatalogError, Chart, Results
from kubescope.views import plugins_catalog
from kubescope.views.plugins_catalog import InstallDialog
from tests.test_window_flows import _ready_window, _wait_until

CHART = Chart(
    "argo-cd", "argo", "10.18.0", "v3", "A Helm chart", True, True, False, "https://x"
)


def test_the_menu_has_plugins_with_catalog_and_installed_and_no_add_ons(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    ui = window.ui
    assert not hasattr(ui, "navAddons")
    assert ui.navPlugins.text() == "Plugins"
    assert ui.navPluginsCatalog.text() == "Catalog"
    assert ui.navPluginsInstalled.text() == "Installed"
    assert window._nav_views["addons"] is ui.navPluginsInstalled


def test_opening_the_catalog_searches_once_and_draws_a_card_per_chart(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    asked = []

    def search(query, *_args):
        asked.append(query)
        return Results([CHART], 1)

    monkeypatch.setattr(plugins_catalog, "search_charts", search)
    window._show_page(6)
    catalog = window.plugins_catalog
    _wait_until(lambda: catalog.charts is not None)
    window._show_page(6)

    assert asked == [""]
    assert window.ui.navPluginsCatalog.isChecked()
    assert catalog.ui.cardsGrid.count() == 1
    assert window.ui.pageTitle.text() == "Catalog"


def test_a_failed_search_says_so_and_a_stale_answer_is_ignored(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog

    def offline(*_args):
        raise CatalogError("no route")

    monkeypatch.setattr(plugins_catalog, "search_charts", offline)
    catalog.ui.searchInput.setText("argo")
    catalog.search()
    _wait_until(lambda: "no route" in catalog.ui.statusLabel.text())

    catalog._found("old", 0, Results([CHART], 1))  # an answer to an earlier search
    assert catalog.charts is None


def test_install_shows_the_commands_and_learn_more_opens_the_page(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog
    opened, shown = [], []
    monkeypatch.setattr(
        plugins_catalog.QDesktopServices, "openUrl", lambda url: opened.append(url)
    )
    monkeypatch.setattr(InstallDialog, "exec", lambda self: shown.append(self))

    catalog.learn_more(CHART)
    catalog.install(CHART)

    assert opened[0].toString() == "https://artifacthub.io/packages/helm/argo/argo-cd"
    assert "helm install argo-cd argo/argo-cd" in CHART.command
    assert isinstance(shown[0], InstallDialog)


def test_a_card_shows_the_logo_when_it_arrives_and_a_badge_per_seal(
    monkeypatch,
) -> None:
    from PySide6.QtCore import QBuffer, QByteArray, QIODevice
    from PySide6.QtGui import QColor, QImage
    from PySide6.QtWidgets import QLabel

    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog
    monkeypatch.setattr(plugins_catalog, "fetch_logo", lambda _id: None)
    chart = Chart(
        "argo-cd", "argo", "1", "1", "d", True, True, True, "https://x", "abcdef12"
    )
    catalog.charts = [chart]
    catalog.render()
    item = catalog.ui.cardsGrid.itemAt(0)
    assert item is not None
    card = item.widget()
    assert card is not None
    tips = {label.toolTip() for label in card.findChildren(QLabel)}
    assert {"Official", "Verified publisher", "CNCF"} <= tips

    image = QImage(8, 8, QImage.Format.Format_RGB32)
    image.fill(QColor("red"))
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, cast(Any, "PNG"))  # PySide takes a str, its stub bytes
    catalog._logo("abcdef12", bytes(data.data()))
    logo = catalog._logo_labels["abcdef12"][0]
    assert not logo.pixmap().isNull()
    catalog._logo("abcdef12", b"not an image")  # ignored


def test_a_second_search_still_loads_its_logos(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog
    chart = Chart("a", "r", "1", "1", "d", False, False, False, "https://x", "abcdef12")
    monkeypatch.setattr(
        plugins_catalog, "search_charts", lambda *_a: Results([chart], 1)
    )
    monkeypatch.setattr(plugins_catalog, "fetch_logo", lambda _id: None)
    for text in ("one", "two", "three"):
        catalog.ui.searchInput.setText(text)
        catalog.search()
        _wait_until(lambda: catalog.charts is not None and catalog._worker is None)
        _wait_until(lambda: catalog._logos is None)
        catalog.charts = None


def test_more_cards_fit_a_wider_page_and_load_more_asks_the_next_page(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog
    asked = []

    def search(query, offset=0):
        asked.append(offset)
        return Results([CHART], 3)

    monkeypatch.setattr(plugins_catalog, "search_charts", search)
    monkeypatch.setattr(plugins_catalog, "fetch_logo", lambda _id: None)
    catalog.search()
    _wait_until(lambda: catalog.charts is not None and catalog._worker is None)
    assert catalog.total == 3 and catalog.ui.cardsGrid.count() == 2  # card + button
    catalog.load_more()
    _wait_until(lambda: len(catalog.charts or []) == 2 and catalog._worker is None)
    assert asked == [0, 1]

    catalog._fit_columns = lambda: 5
    catalog.render()
    assert catalog._columns == 5


def test_a_search_that_breaks_says_so_and_a_stale_page_is_ignored(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog

    def broken(*_args):
        raise RuntimeError("boom")

    monkeypatch.setattr(plugins_catalog, "search_charts", broken)
    catalog.ui.searchInput.setText("x")
    catalog.search()
    _wait_until(lambda: "boom" in catalog.ui.statusLabel.text())

    catalog._failed("another text", "late")  # for a search that is not the last
    assert "late" not in catalog.ui.statusLabel.text()
    catalog.charts = [CHART]
    catalog._asked = "x"
    catalog._found("x", 5, Results([CHART], 9))  # not the page that comes next
    assert catalog.charts == [CHART]


def test_the_logos_are_read_in_order_stopping_when_asked_and_kept_for_a_redraw(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog
    reads = []
    monkeypatch.setattr(
        plugins_catalog,
        "fetch_logo",
        lambda i: reads.append(i) or (b"x" if i == "a" else None),
    )
    worker = plugins_catalog.LogoWorker(["a", "b"])
    got = []
    worker.logo.connect(lambda i, d: got.append(i))
    worker.run()
    assert reads == ["a", "b"] and got == ["a"]  # "b" has no image
    monkeypatch.setattr(worker, "isInterruptionRequested", lambda: True)
    worker.run()
    assert reads == ["a", "b"]  # asked to stop: reads nothing more

    chart = Chart("a", "r", "1", "1", "d", False, False, False, "https://x", "abcdef12")
    catalog._logos = plugins_catalog.LogoWorker([])  # a search is still reading
    catalog._logos.logo.connect(catalog._logo)
    catalog.charts = [chart]
    catalog._load_logos()
    catalog._pixmaps["abcdef12"] = QPixmap(4, 4)
    catalog.render()
    label = catalog._logo_labels["abcdef12"][0]
    assert not label.pixmap().isNull()  # a redraw keeps the logo
    window.close()


def test_a_wider_page_redraws_the_cards_in_more_columns(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    catalog = window.plugins_catalog
    catalog.charts = [CHART]
    catalog.render()
    catalog._fit_columns = lambda: 6
    catalog.eventFilter(catalog.ui.cardsScroll.viewport(), QEvent(QEvent.Type.Resize))
    assert catalog._columns == 6
    catalog.eventFilter(
        catalog.ui.cardsScroll.viewport(), QEvent(QEvent.Type.Resize)
    )  # the same width: nothing to redraw
    assert catalog._columns == 6

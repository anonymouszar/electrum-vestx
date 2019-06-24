#!/usr/bin/env python
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2015 Thomas Voegtlin
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import webbrowser

from .util import *
from electrum_vestx.i18n import _
from electrum_vestx.util import block_explorer_URL, profiler, TxMinedInfo
from electrum_vestx.logging import get_logger, Logger

_logger = get_logger(__name__)

try:
    from electrum_vestx.plot import plot_history, NothingToPlotException
except:
    _logger.info("qt/history_list: could not import electrum_pac.plot. This feature needs matplotlib to be installed.")
    plot_history = None

# note: this list needs to be kept in sync with another in kivy
TX_ICONS = [
    "unconfirmed.png",
    "warning.png",
    "unconfirmed.png",
    "offline_tx.png",
    "clock1.png",
    "clock2.png",
    "clock3.png",
    "clock4.png",
    "clock5.png",
    "confirmed.png",
]


class DashboardHistoryList(MyTreeWidget, AcceptFileDragDrop):

    def __init__(self, parent=None):
        MyTreeWidget.__init__(self, parent, self.create_menu, [], 3)
        self.refresh_headers()
        self.setColumnHidden(1, True)
        self.sortByColumn(0, Qt.AscendingOrder)
        self.start_timestamp = None
        self.end_timestamp = None
        self.years = []
        self.wallet = None

    def format_date(self, d):
        return str(datetime.date(d.year, d.month, d.day)) if d else _('None')

    def refresh_headers(self):
        headers = ['', '', _('Date'), _('Description') , _('Amount')]
        self.update_headers(headers)
        # Set fixed width for the first column
        self.header().setSectionResizeMode(0, QHeaderView.Fixed)
        self.header().resizeSection(0, 20)
        # Set default column width just in case there is no data
        self.header().setSectionResizeMode(1, QHeaderView.Fixed)
        self.header().resizeSection(1, 100)
        self.header().setSectionResizeMode(2, QHeaderView.Fixed)
        self.header().resizeSection(2, 100)
        self.header().setSectionResizeMode(4, QHeaderView.Fixed)
        self.header().resizeSection(4, 100)

    def get_domain(self):
        '''Replaced in address_dialog.py'''
        return self.wallet.get_addresses()

    @profiler
    def on_update(self):
        self.wallet = self.parent.wallet
        fx = self.parent.fx
        r = self.wallet.get_full_history(domain=self.get_domain(), from_timestamp=self.start_timestamp, to_timestamp=self.end_timestamp, fx=fx)
        self.transactions = r['transactions']
        self.summary = r['summary']
        if not self.years and self.transactions:
            from datetime import date
            start_date = self.transactions[0].get('date') or date.today()
            end_date = self.transactions[-1].get('date') or date.today()
            self.years = [str(i) for i in range(start_date.year, end_date.year + 1)]
        item = self.currentItem()
        current_tx = item.data(0, Qt.UserRole) if item else None
        self.clear()
        if fx: fx.history_used_spot = False
        blue_brush = QBrush(QColor("#1E1EFF"))
        red_brush = QBrush(QColor("#BC1E1E"))
        # Resize to content when there are data
        if len(self.transactions) > 0:
            self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            self.header().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        for tx_item in self.transactions:
            tx_hash = tx_item['txid']
            height = tx_item['height']
            conf = tx_item['confirmations']
            timestamp = tx_item['timestamp']
            value = tx_item['value'].value
            balance = tx_item['balance'].value
            label = tx_item['label']
            tx_mined_status = TxMinedInfo(height=tx_item['height'],
                                    conf=tx_item['confirmations'],
                                    timestamp=tx_item['timestamp'])
            status, status_str = self.wallet.get_tx_status(tx_hash, tx_mined_status)
            has_invoice = self.wallet.invoices.paid.get(tx_hash)
            icon = read_QIcon(TX_ICONS[status])
            v_str = self.parent.format_amount(value, is_diff=True, whitespaces=True)
            balance_str = self.parent.format_amount(balance, whitespaces=True)
            entry = ['', tx_hash, status_str, label, v_str, balance_str]
            fiat_value = None
            item = SortableTreeWidgetItem(entry)
            item.setIcon(0, icon)
            item.setToolTip(0, str(conf) + " confirmation" + ("s" if conf != 1 else ""))
            item.setData(0, SortableTreeWidgetItem.DataRole, (status, conf))
            if has_invoice:
                item.setIcon(3, read_QIcon("seal"))
            for i in range(len(entry)):
                if i>3:
                    item.setTextAlignment(i, Qt.AlignRight | Qt.AlignVCenter)
            if value and value < 0:
                item.setForeground(3, red_brush)
                item.setForeground(4, red_brush)
            if fiat_value and not tx_item['fiat_default']:
                item.setForeground(6, blue_brush)
            if tx_hash:
                item.setData(0, Qt.UserRole, tx_hash)
            self.insertTopLevelItem(0, item)
            if current_tx == tx_hash:
                self.setCurrentItem(item)

    def on_doubleclick(self, item, column):
        tx_hash = item.data(0, Qt.UserRole)
        tx = self.wallet.db.get_transaction(tx_hash)
        self.parent.show_transaction(tx)

    def update_item(self, wallet, tx_hash, tx_mined_status):
        if self.wallet is None:
            return
        conf = tx_mined_status.conf
        status, status_str = self.wallet.get_tx_status(tx_hash, tx_mined_status)
        icon = read_QIcon(TX_ICONS[status])
        items = self.findItems(tx_hash, Qt.UserRole|Qt.MatchContains|Qt.MatchRecursive, column=1)
        if items:
            item = items[0]
            item.setIcon(0, icon)
            item.setData(0, SortableTreeWidgetItem.DataRole, (status, conf))
            item.setText(2, status_str)

    def create_menu(self, position):
        self.selectedIndexes()
        item = self.currentItem()
        if not item:
            return
        tx_hash = item.data(0, Qt.UserRole)
        if not tx_hash:
            return
        tx_URL = block_explorer_URL(self.config, 'tx', tx_hash)
        tx = self.wallet.db.get_transaction(tx_hash)
        menu = QMenu()
        menu.addAction(_("Details"), lambda: self.parent.show_transaction(tx))
        if tx_URL:
            menu.addAction(_("View on block explorer"), lambda: webbrowser.open(tx_URL))
        menu.exec_(self.viewport().mapToGlobal(position))

    def onFileAdded(self, fn):
        return

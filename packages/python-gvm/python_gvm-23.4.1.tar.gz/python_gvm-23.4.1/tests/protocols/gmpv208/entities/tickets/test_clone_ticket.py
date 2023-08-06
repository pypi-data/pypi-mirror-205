# -*- coding: utf-8 -*-
# Copyright (C) 2019-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gvm.errors import RequiredArgument


class GmpCloneTicketTestMixin:
    def test_clone(self):
        self.gmp.clone_ticket("t1")

        self.connection.send.has_been_called_with(
            "<create_ticket><copy>t1</copy></create_ticket>"
        )

        self.gmp.clone_ticket(ticket_id="t1")

        self.connection.send.has_been_called_with(
            "<create_ticket><copy>t1</copy></create_ticket>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_ticket("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_ticket(None)

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_ticket(ticket_id=None)

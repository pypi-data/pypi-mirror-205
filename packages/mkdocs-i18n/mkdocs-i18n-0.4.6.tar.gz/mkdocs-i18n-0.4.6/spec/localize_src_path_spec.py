#
#   Copyright © 2020, 2021 Simó Albert i Beltran
#
#   This file is part of MkDocs i18n plugin.
#
#   Mkdocs i18n plugin is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   Foobar is distributed in the hope that it will be useful, but WITHOUT ANY
#   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#   details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with MkDocs i18n plugin. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

""" Document path localization tests for mkdocs-i18n"""

from expects import equal, expect
from mamba import before, description, it

import mkdocs_i18n

# pylint: disable=protected-access
with description("mkdocs_i18n") as self:
    with before.all:
        self.i18n = mkdocs_i18n.I18n()
        self.i18n.config = {
            "default_language": "default",
            "languages": {"default": "Default Language", "language": "Other language"},
        }
    with it(
        "localizes dir.name/page.name.language.md to dir.name/page.name.md and "
        "dir.name/page.name.default.md"
    ):
        urls = self.i18n._get_localized_src_paths(
            "dir.name/page.name.language.md", "default"
        )
        expect(["dir.name/page.name.md", "dir.name/page.name.default.md"]).to(
            equal(urls)
        )
    with it("localizes dir.name/page.name.md url to dir.name/page.name.language.md"):
        urls = self.i18n._get_localized_src_paths("dir.name/page.name.md", "language")
        expect(["dir.name/page.name.language.md"]).to(equal(urls))
    with it(
        "localizes dir.name/page.name.default.md to language "
        "dir.name/page.name.language.md"
    ):
        urls = self.i18n._get_localized_src_paths(
            "dir.name/page.name.default.md", "language"
        )
        expect(["dir.name/page.name.language.md"]).to(equal(urls))

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

""" Tests for mkdocs-i18n """

from bs4 import BeautifulSoup
from click.testing import CliRunner
from expects import equal, expect
from mamba import description, it
from mkdocs.__main__ import cli

nav_result = {
    "ca": [
        "Exemple de índex",
        "Secció",
        "Sense titol a nav",
        "Títol de página",
        "Solo castellano (Castellano)",
        "Subsecció",
        "Índex en un subdirectori",
        "Només català i castellà",
        "Pàgina amb títol traduit",
    ],
    "en": [
        "Index example",
        "Section",
        "No title in nav",
        "Page Title",
        "Solo castellano (Castellano)",
        "Subsection",
        "Index in a subdirectory",
        "Només català i castellà (Català)",
        "Solo catalan y castellano (Castellano)",
        "Page with title translated",
    ],
    "es": [
        "Ejemplo de índice",
        "Sección",
        "Sin titulo en nav",
        "Título de página",
        "Solo castellano",
        "Subsección",
        "Index in a subdirectory (English)",
        "Índex en un subdirectori (Català)",
        "Solo catalan y castellano",
        "Página con título traducido",
    ],
}

results = {
    "index.html": {
        "links": [("Català", "index.ca/"), ("Castellano", "index.es/")],
        "nav": nav_result["en"],
        "active_nav": ["Index example"],
        "alternate": [
            ("English", "."),
            ("Català", "index.ca/"),
            ("Castellano", "index.es/"),
        ],
    },
    "index.ca/index.html": {
        "links": [("Castellano", "../index.es/"), ("English", "../")],
        "nav": nav_result["ca"],
        "active_nav": ["Exemple de índex"],
        "alternate": [
            ("English", ".."),
            ("Català", "./"),
            ("Castellano", "../index.es/"),
        ],
    },
    "index.es/index.html": {
        "links": [("Català", "../index.ca/"), ("English", "../")],
        "nav": nav_result["es"],
        "active_nav": ["Ejemplo de índice"],
        "alternate": [
            ("English", ".."),
            ("Català", "../index.ca/"),
            ("Castellano", "./"),
        ],
    },
    "no-nav-title/index.html": {
        "links": [
            ("Català", "../no-nav-title.ca/"),
            ("Castellano", "../no-nav-title.es/"),
        ],
        "nav": nav_result["en"],
        "active_nav": ["Section", "No title in nav"],
        "alternate": [
            ("English", "./"),
            ("Català", "../no-nav-title.ca/"),
            ("Castellano", "../no-nav-title.es/"),
        ],
    },
    "no-nav-title.ca/index.html": {
        "links": [
            ("Castellano", "../no-nav-title.es/"),
            ("English", "../no-nav-title/"),
        ],
        "nav": nav_result["ca"],
        "active_nav": ["Secció", "Sense titol a nav"],
        "alternate": [
            ("English", "../no-nav-title/"),
            ("Català", "./"),
            ("Castellano", "../no-nav-title.es/"),
        ],
    },
    "no-nav-title.es/index.html": {
        "links": [
            ("Català", "../no-nav-title.ca/"),
            ("English", "../no-nav-title/"),
        ],
        "nav": nav_result["es"],
        "active_nav": ["Sección", "Sin titulo en nav"],
        "alternate": [
            ("English", "../no-nav-title/"),
            ("Català", "../no-nav-title.ca/"),
            ("Castellano", "./"),
        ],
    },
    "nav-title.ca/index.html": {
        "links": [
            ("Castellano", "../nav-title.es/"),
            ("English", "../nav-title.en/"),
        ],
        "nav": nav_result["ca"],
        "active_nav": ["Secció", "Títol de página"],
        "alternate": [
            ("English", "../nav-title.en/"),
            ("Català", "./"),
            ("Castellano", "../nav-title.es/"),
        ],
    },
    "nav-title.en/index.html": {
        "links": [
            ("Català", "../nav-title.ca/"),
            ("Castellano", "../nav-title.es/"),
        ],
        "nav": nav_result["en"],
        "active_nav": ["Section", "Page Title"],
        "alternate": [
            ("English", "./"),
            ("Català", "../nav-title.ca/"),
            ("Castellano", "../nav-title.es/"),
        ],
    },
    "nav-title.es/index.html": {
        "links": [
            ("Català", "../nav-title.ca/"),
            ("English", "../nav-title.en/"),
        ],
        "nav": nav_result["es"],
        "active_nav": ["Sección", "Título de página"],
        "alternate": [
            ("English", "../nav-title.en/"),
            ("Català", "../nav-title.ca/"),
            ("Castellano", "./"),
        ],
    },
    "only-es.es/index.html": {
        "links": [
            (
                "Català: Aquesta pàgina no està traduida al català.",
                None,
            ),
            (
                "English: This page isn't translated to English.",
                None,
            ),
        ],
        "nav": nav_result["es"],
        "active_nav": ["Sección", "Solo castellano"],
        "alternate": [
            ("English (Home)", ".."),
            ("Català (Inici)", "../index.ca/"),
            ("Castellano", "./"),
        ],
    },
    "dir/index.html": {
        "links": [
            ("Català", "../dir/index.ca/"),
            (
                "Castellano: Esta página no está traducida al castellano.",
                None,
            ),
        ],
        "nav": nav_result["en"],
        "active_nav": ["Section", "Subsection", "Index in a subdirectory"],
        "alternate": [
            ("English", "./"),
            ("Català", "index.ca/"),
            ("Castellano (Inicio)", "../index.es/"),
        ],
    },
    "dir/index.ca/index.html": {
        "links": [
            (
                "Castellano: Esta página no está traducida al castellano.",
                None,
            ),
            ("English", "../../dir/"),
        ],
        "nav": nav_result["ca"],
        "active_nav": ["Secció", "Subsecció", "Índex en un subdirectori"],
        "alternate": [
            ("English", "../"),
            ("Català", "./"),
            ("Castellano (Inicio)", "../../index.es/"),
        ],
    },
    "dir/no-en.ca/index.html": {
        "links": [
            ("Castellano", "../../dir/no-en.es/"),
            (
                "English: This page isn't translated to English.",
                None,
            ),
        ],
        "nav": nav_result["ca"],
        "active_nav": ["Secció", "Subsecció", "Només català i castellà"],
        "alternate": [
            ("English (Home)", "../.."),
            ("Català", "./"),
            ("Castellano", "../no-en.es/"),
        ],
    },
    "dir/no-en.es/index.html": {
        "links": [
            ("Català", "../../dir/no-en.ca/"),
            (
                "English: This page isn't translated to English.",
                None,
            ),
        ],
        "nav": nav_result["es"],
        "active_nav": ["Sección", "Subsección", "Solo catalan y castellano"],
        "alternate": [
            ("English (Home)", "../.."),
            ("Català", "../no-en.ca/"),
            ("Castellano", "./"),
        ],
    },
    "translated-title.ca/index.html": {
        "links": [
            ("Castellano", "../translated-title.es/"),
            ("English", "../translated-title.en/"),
        ],
        "nav": nav_result["ca"],
        "active_nav": ["Secció", "Subsecció", "Pàgina amb títol traduit"],
        "alternate": [
            ("English", "../translated-title.en/"),
            ("Català", "./"),
            ("Castellano", "../translated-title.es/"),
        ],
    },
    "translated-title.en/index.html": {
        "links": [
            ("Català", "../translated-title.ca/"),
            ("Castellano", "../translated-title.es/"),
        ],
        "nav": nav_result["en"],
        "active_nav": ["Section", "Subsection", "Page with title translated"],
        "alternate": [
            ("English", "./"),
            ("Català", "../translated-title.ca/"),
            ("Castellano", "../translated-title.es/"),
        ],
    },
    "translated-title.es/index.html": {
        "links": [
            ("Català", "../translated-title.ca/"),
            ("English", "../translated-title.en/"),
        ],
        "nav": nav_result["es"],
        "active_nav": [
            "Sección",
            "Subsección",
            "Página con título traducido",
        ],
        "alternate": [
            ("English", "../translated-title.en/"),
            ("Català", "../translated-title.ca/"),
            ("Castellano", "./"),
        ],
    },
}

with description("MkDocs") as self:
    with it("builds"):
        runner = CliRunner()
        result = runner.invoke(cli, ["build", "--strict"])
        print(result.output)
        expect(0).to(equal(result.exit_code))
    with it("localizes"):
        for filename, result in results.items():
            with open(f"site/{filename}", "r", encoding="utf8") as file:
                soup = BeautifulSoup(file.read(), "lxml")
            expect(result["links"]).to(
                equal(
                    [
                        (li.text, (li.a.get("href") if li.a else None))
                        for li in soup.article.ul.find_all("li")
                    ]
                )
            )
            expect(result["active_nav"]).to(
                equal(
                    [
                        next(active.label.stripped_strings)
                        for active in soup.find_all(class_="md-nav__item--active")
                        if active.label
                    ]
                    + [
                        next(active.stripped_strings)
                        for active in soup.find_all(class_="md-nav__link--active")
                    ]
                )
            )
            expect(result["nav"]).to(
                equal(
                    [
                        next(a.stripped_strings)
                        for a in soup.find_all(class_="md-nav__link")
                    ]
                )
            )
            expect(result["alternate"]).to(
                equal(
                    [
                        (li.text.strip(), (li.a.get("href") if li.a else None))
                        for li in soup.find_all(class_="md-select__item")
                    ]
                )
            )

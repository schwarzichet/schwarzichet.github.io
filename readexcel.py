from os import sep
from typing import List, Tuple, Any
from numpy import NaN, remainder
import pandas
from mdutils.mdutils import MdUtils
import markdown_strings
import os
from pathlib import Path
import sys
import re

game_sheets = ["2014-2000年", "2015-2021年", "古早作品"]


for gs in game_sheets:
    gamelife = pandas.read_excel(
        "gamelife.xlsx",
        sheet_name=gs,
        engine="openpyxl",
    )

    games: List[Tuple[Any, pandas.Series]] = list(gamelife.iterrows())

    for index, game in games:
        # game = games[62][1]

        name: str = game["作品名"].strip()
        date: pandas.Timestamp = game["发售日"]
        year = date.year
        print(name, year)

        if not os.path.exists("docs/game/"+str(year)):
            Path("docs/game/"+str(year)).mkdir(parents=False, exist_ok=True)

        if not os.path.exists("docs/game/"+str(year) + "/README.md"):
            readme_mdFile = MdUtils(file_name="docs/game/"+str(year) + "/README.md")
            readme_mdFile.new_header(1, str(year))
            readme_mdFile.new_line(f"This is for {year}'s games.")
            readme_mdFile.create_md_file()

        if "/" in name:
            name = name.replace("/", "forward slash")
        if ":" in name:
            name = name.replace(":", "Colon")

        mdFile = MdUtils(file_name="docs/game/"+str(year) + "/" + name)
        mdFile.new_header(1, game["作品名"])
        # mdFile.new_table_of_contents(table_title='Contents', depth=2)
        meta_info = ["TAG", "发售日", "备注", "总评人数", "好评人数"]
        for i in meta_info:
            if i in game.keys():
                if not pandas.isna(game[i]):
                    mdFile.new_line(i + ": " + str(game[i]))
                else:
                    mdFile.new_line(i + ": no data~")
            else:
                mdFile.new_line(i + ": no data~")

        try:
            for i in game.iteritems():
                if i[0] not in meta_info and i[0] != "作品名" and not pandas.isna(i[1]):
                    comment: str = i[1]
                    if not comment or comment.isspace():
                        continue
                    seps = list(re.finditer("；|：|;", comment))
                    score, comment, name = (
                        comment[: seps[0].start()],
                        comment[seps[0].end() : seps[-1].start()],
                        comment[seps[-1].end() :],
                    )
                    mdFile.new_header(2, name + " " + score, style="atx")
                    mdFile.new_paragraph(comment)
        except Exception as e:
            print(game)
            print(e)
            print(comment)
            # print(comment.split(sep="；：", maxsplit=1))
            # print(comment.rsplit(sep='；：', maxsplit=1))
            sys.exit()

        mdFile.create_md_file()

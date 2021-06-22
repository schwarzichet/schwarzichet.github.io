from os import sep
from typing import List, Tuple, Any
from numpy import NaN, remainder
import pandas
from mdutils.mdutils import MdUtils,MarkDownFile
import markdown_strings
import os
from pathlib import Path
import sys
import re
import yaml

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

        if not os.path.exists("docs/game/README.md"):
            Path("docs/game/").mkdir(parents=True, exist_ok=True)
            readme_mdFile = MdUtils(file_name="docs/game/README.md")
            readme_mdFile.new_header(1, "Game")
            readme_mdFile.new_line(f"This is for games.")
            readme_mdFile.create_md_file()

        if not os.path.exists("docs/game/" + str(year)):
            Path("docs/game/" + str(year)).mkdir(parents=True, exist_ok=True)

        if not os.path.exists("docs/game/" + str(year) + "/README.md"):
            readme_mdFile = MdUtils(file_name="docs/game/" + str(year) + "/README.md")
            readme_mdFile.new_header(1, str(year))
            readme_mdFile.new_line(f"This is for {year}'s games.")
            readme_mdFile.create_md_file()

        if "/" in name:
            name = name.replace("/", "forward slash")
        if ":" in name:
            name = name.replace(":", "Colon")

        mdFile = MdUtils(file_name="docs/game/" + str(year) + "/" + name)
        mdFile.title = ""
        md_file  = MarkDownFile("docs/game/" + str(year) + "/" + name)
        md_metadata = {"game_release_date": date.strftime("%Y-%m-%d") if not pandas.isna(date) else "unknown"}
        mdFile.write("---\n")
        mdFile.write(yaml.dump(md_metadata))
        mdFile.write("---\n")

        mdFile.new_header(1, game["作品名"])
        meta_info = ["TAG", "发售日", "备注", "总评人数", "好评人数"]
        for i in meta_info:
            if i in game.keys():
                if not pandas.isna(game[i]):
                    if i == "发售日":
                        mdFile.new_line(i + ": " + str(game[i].strftime("%Y-%m-%d")))
                    else:
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

                    if score.strip() == "+1":
                        score = "<Badge type=\"tip\" text=\"+1\" vertical=\"middle\" />"
                    if score.strip() == '-1':
                        score = "<Badge type=\"danger\" text=\"-1\" vertical=\"middle\" />"

                    mdFile.new_header(2, name + " " + score, style="atx")


                    collapse_text = []
                    if "剧透" in comment:
                        collapse_text.append("剧透警告")
                    

                    if len(comment) > 500:
                        collapse_text.append("小作文警告")

                    if len(collapse_text)!=0: 
                        c_t = "&".join(collapse_text)
                        comment = f"::: details {c_t}\n" + comment + "\n:::\n"
                        mdFile.write(comment)
                    else:
                        mdFile.new_paragraph(comment)

        except Exception as e:
            print(game)
            print(e)
            print(comment)
            # print(comment.split(sep="；：", maxsplit=1))
            # print(comment.rsplit(sep='；：', maxsplit=1))
            sys.exit()


        print(mdFile.title, mdFile.table_of_contents)
        mdFile.create_md_file()

from typing import List, Tuple, Any
import pandas
from mdutils.mdutils import MdUtils, MarkDownFile
import markdown_strings
import os
from pathlib import Path
import sys
import re
import yaml
from pathvalidate import sanitize_filename


def read_excel(file_path: str, sheet_name: str) -> List[Tuple[Any, pandas.Series]]:
    excel_file = pandas.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
    entries: List[Tuple[Any, pandas.Series]] = list(excel_file.iterrows())
    return entries


def create_category_readme(category: str, content: str, header: str):
    if not os.path.exists(f"docs/{category}/README.md"):
        Path(f"docs/{category}/").mkdir(parents=True, exist_ok=True)
        readme_mdFile = MdUtils(file_name=f"docs/{category}/README.md")
        readme_mdFile.new_header(1, header)
        readme_mdFile.new_line(content)
        readme_mdFile.create_md_file()


def create_year_folders(category: str, year: int):
    if not os.path.exists(f"docs/{category}/" + str(year)):
        Path(f"docs/{category}/" + str(year)).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(f"docs/{category}/" + str(year) + "/README.md"):
        readme_mdFile = MdUtils(
            file_name=f"docs/{category}/" + str(year) + "/README.md"
        )
        readme_mdFile.new_header(1, str(year))
        readme_mdFile.new_line(f"This is for {year}'s {category}s.")
        readme_mdFile.create_md_file()


def check_filename(name: str) -> str:
    return str(sanitize_filename(name)).replace("'", "quote").replace('"', "quote")


def parse_comment(comment: str):
    seps = list(re.finditer("；|：|;", comment))
    score, comment, name = (
        comment[: seps[0].start()],
        comment[seps[0].end() : seps[-1].start()],
        comment[seps[-1].end() :],
    )

    if score.strip() == "+1":
        score = '<Badge type="tip" text="+1" vertical="middle" />'
    if score.strip() == "+2":
        score = '<Badge type="tip" text="+2" vertical="middle" />'
    if score.strip() == "-1":
        score = '<Badge type="danger" text="-1" vertical="middle" />'
    if score.strip() == "0" or score.strip() == "+0":
        score = '<Badge type="warning" text="0" vertical="middle" />'

    comment_header = score + " " + name

    collapse_text = []
    if "剧透" in comment:
        collapse_text.append("剧透警告")

    if len(comment) > 500:
        collapse_text.append("小作文警告")

    if len(collapse_text) != 0:
        c_t = "&".join(collapse_text)
        comment = f"::: details {c_t}\n" + comment + "\n:::\n"
    else:
        comment = "\n\n" + comment

    return comment_header, comment


def make_game():
    game_sheets = ["2014-2000年", "2015-2021年", "古早作品"]
    for gs in game_sheets:
        games = read_excel("游戏人生.xlsx", gs)
        for index, game in games:

            name: str = game["作品名"].strip()
            date: pandas.Timestamp = game["发售日"]
            year = date.year

            create_category_readme("game", "This is for games.", "Game")

            create_year_folders("game", year)

            filename = check_filename(name)

            mdFile = MdUtils(file_name="docs/game/" + str(year) + "/" + filename)
            mdFile.title = ""
            md_metadata = {
                "release_date": date.strftime("%Y-%m-%d")
                if not pandas.isna(date)
                else "unknown"
            }
            mdFile.write("---\n")
            mdFile.write(yaml.dump(md_metadata))
            mdFile.write("---\n")

            mdFile.new_header(1, game["作品名"])
            meta_info = ["TAG", "发售日", "备注", "总评人数", "好评人数"]
            for i in meta_info:
                if i in game.keys():
                    if not pandas.isna(game[i]):
                        if i == "发售日":
                            mdFile.new_line(
                                i + ": " + str(game[i].strftime("%Y-%m-%d"))
                            )
                        else:
                            mdFile.new_line(i + ": " + str(game[i]))
                    else:
                        mdFile.new_line(i + ": no data~")
                else:
                    if i in meta_info[-2::]:
                        mdFile.new_line(i + ": no data~")

            try:
                for i in game.iteritems():
                    if (
                        i[0] not in meta_info
                        and i[0] != "作品名"
                        and not pandas.isna(i[1])
                    ):
                        comment: str = i[1]
                        if not comment or comment.isspace():
                            continue

                        comment_header, comment = parse_comment(comment)
                        mdFile.new_header(2, comment_header, style="atx")
                        mdFile.write(comment)

            except Exception as e:
                print(game)
                print(e)
                print(comment)
                sys.exit()

            mdFile.create_md_file()


def make_anime():

    anime_sheets = [f"{x}番剧目录" for x in range(2010, 2022)]
    anime_sheets.append("上古番剧目录")

    for anime_sheet in anime_sheets:
        animes = read_excel("番剧茶话会.xlsx", anime_sheet)
        for index, anime in animes:
            if pandas.isna(anime["全称"]) or anime["全称"] == "其他":
                continue

            name: str = anime["全称"].strip()
            if type(anime["放送时间"]) is float:
                date: pandas.Timestamp = pandas.Timestamp(
                    year=int(anime["放送时间"]), month=1, day=1
                )
            else:
                date: pandas.Timestamp = anime["放送时间"]
            year = date.year

            create_category_readme("anime", "This is for animes", "Anime")

            create_year_folders("anime", year)

            filename = check_filename(name)

            mdFile = MdUtils(file_name="docs/anime/" + str(year) + "/" + filename)
            mdFile.title = ""
            md_metadata = {
                "release_date": date.strftime("%Y-%m")
                if not pandas.isna(date)
                else "unknown"
            }
            mdFile.write("---\n")
            mdFile.write(yaml.dump(md_metadata))
            mdFile.write("---\n")

            mdFile.new_header(1, anime["全称"])

            meta_info = ["TAG", "放送时间", "备注", "总评人数", "好评人数"]

            for i in meta_info:
                if i in anime.keys():
                    if not pandas.isna(anime[i]):
                        if i == "放送时间":
                            if anime_sheet == "上古番剧目录":
                                mdFile.new_line(i + ": " + str(year))
                            else:
                                mdFile.new_line(i + ": " + str(date.strftime("%Y-%m")))
                        else:
                            mdFile.new_line(i + ": " + str(anime[i]))
                    else:
                        mdFile.new_line(i + ": no data~")

            try:
                for i in anime.iteritems():
                    if i[0] not in meta_info and i[0] != "全称" and not pandas.isna(i[1]):
                        comment: str = i[1]
                        if not comment or comment.isspace():
                            continue
                        comment_header, comment = parse_comment(comment)
                        mdFile.new_header(2, comment_header, style="atx")
                        mdFile.write(comment)

            except Exception as e:
                print(anime)
                print(e)
                print(comment)
                sys.exit()

            mdFile.create_md_file()


def make_tvfilm():
    tvfilm_sheets = ["影视剧", "电影"]
    for tvfilm_sheet in tvfilm_sheets:
        tvfilms = read_excel("三次元影视评鉴.xlsx", tvfilm_sheet)
        for index, tvfilm in tvfilms:
            if pandas.isna(tvfilm["名称"]) and pandas.isna(tvfilm["原文名称"]):
                continue

            if pandas.isna(tvfilm["名称"]):
                name: str = tvfilm["原文名称"].strip()
            else:
                name: str = tvfilm["名称"].strip()

            if tvfilm_sheet == "影视剧":
                date: pandas.Timestamp = tvfilm["播出时间"]
                year = date.year
            if tvfilm_sheet == "电影":
                date: pandas.Timestamp = tvfilm["上映时间（世界首映）"]
                year = date.year

            create_category_readme("tvfilm", "This is for tv&films", "tv&film")

            create_year_folders("tvfilm", year)

            filename = check_filename(name)

            mdFile = MdUtils(file_name="docs/tvfilm/" + str(year) + "/" + filename)
            mdFile.title = ""
            md_metadata = {
                "release_date": date.strftime("%Y-%m-%d")
                if not pandas.isna(date)
                else "unknown"
            }
            mdFile.write("---\n")
            mdFile.write(yaml.dump(md_metadata))
            mdFile.write("---\n")

            mdFile.new_header(1, name)

            if tvfilm_sheet == "影视剧":
                meta_info = ["原文名称", "tag", "播出时间", "结束时间", "备注", "总评人数", "好评人数"]
            if tvfilm_sheet == "电影":
                meta_info = ["原文名称", "tag", "上映时间（世界首映）", "导演", "备注", "总评人数", "好评人数"]

            for i in meta_info:
                if i in tvfilm.keys():
                    if not pandas.isna(tvfilm[i]):
                        if i == "播出时间" or i == "结束时间" or i == "上映时间（世界首映）":
                            mdFile.new_line(i + ": " + str(date.strftime("%Y-%m-%d")))
                        else:
                            mdFile.new_line(i + ": " + str(tvfilm[i]))
                    else:
                        mdFile.new_line(i + ": no data~")

            try:
                for i in tvfilm.iteritems():
                    if i[0] not in meta_info and i[0] != "名称" and not pandas.isna(i[1]):
                        comment: str = i[1]
                        if not comment or comment.isspace():
                            continue
                        comment_header, comment = parse_comment(comment)
                        mdFile.new_header(2, comment_header, style="atx")
                        mdFile.write(comment)

            except Exception as e:
                print(tvfilm)
                print(e)
                print(comment)
                sys.exit()

            mdFile.create_md_file()


if __name__ == "__main__":
    make_anime()
    make_game()
    make_tvfilm()

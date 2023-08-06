from pathlib import Path

from typer import echo
from typer import Exit
from typer import getchar

from visual_novel_toolkit.speller.mistakes import load_mistakes
from visual_novel_toolkit.speller.words import FileWords


def review_mistakes() -> None:
    for mistake in load_mistakes():
        echo("")
        echo(mistake)
        echo("")
        echo("[i] Insert   [s] Skip   [q] Quit")
        ask_user = True
        while ask_user:
            match getchar():
                case "q":
                    raise Exit(code=0)
                case "s":
                    ask_user = False
                case "i":
                    file_words = FileWords(Path("personal.json"))
                    dictionary = file_words.loads()
                    dictionary.append(mistake)
                    dictionary.sort()
                    file_words.dumps(dictionary)

                    ask_user = False

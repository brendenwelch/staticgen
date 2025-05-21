# maze solver. use sdl to create a game-like interface, to display the maze solver in observable time.


from markdown import markdown_to_html_node


def main():
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    print(md)
    print(markdown_to_html_node(md))


if __name__ == "__main__":
    main()

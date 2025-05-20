# import textnode
import htmlnode


def main():
    html = htmlnode.LeafNode("a", "linktext", {"href": "https://link.com"})
    print(html.to_html())


if __name__ == "__main__":
    main()

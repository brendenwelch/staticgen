# import textnode
import htmlnode


def main():
    sentence = ",aaaaaa ,bbbbbb,c"
    word, rest = sentence.split(",", maxsplit=1)
    print(word)
    print(rest)

if __name__ == "__main__":
    main()

from pdfminer.high_level import extract_text
import sys
replacements = [
    ["\n\n","\n"],
    [" ",""],
    ["\t",""],
    ["\u3000",""]
]
# key = [
#     "机器编号","名称","开户行及账号",
# ]
# ignore = [
#     "购","买","方"
# ]
def extract_recipt(name):
    text = extract_text(name)
    for r in replacements:
        text = text.replace(*r)
    return text

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("please input pdf name")
        exit(0)
    t = extract_recipt(sys.argv[1])
    for i,tt in enumerate(t.splitlines()):
        print(i,tt)

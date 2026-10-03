import os
from pathlib import Path
import shutil

script = Path(__file__).resolve()
projectDir = script.parent
topicsDir = projectDir / "topics"

buildDir = projectDir / "build"
buildDir.mkdir(exist_ok=True)

replaceStr = "<!-- TEMPLATE -->"
templatePath = projectDir / "template.html"
with open(templatePath, "r", encoding="utf-8") as source_file:
    template = source_file.read()
    templateSize = os.path.getsize(templatePath)


replacementIdx = 0
subStrIdx = 0
if templateSize < len(replaceStr):
    exit()

for idx in range(templateSize - len(replaceStr)):
    if replaceStr[subStrIdx] == template[idx]:
        subStrIdx += 1
        if subStrIdx == len(replaceStr):
            replacementIdx = idx - len(replaceStr) + 1
            break
    else:
        if (subStrIdx > 0):
            idx -= 1

        subStrIdx = 0

print(replacementIdx)
print(template[replacementIdx:replacementIdx + len(replaceStr)])

topicsBuildDir = buildDir / "topics"
topicsBuildDir.mkdir(exist_ok=True)

for filePath in topicsDir.rglob("*.html"):
    if filePath.is_file():
        with open(filePath, "rb") as source_file:
            data = source_file.read()

        print(f"File found: {filePath.name}")

        outPath = topicsBuildDir / filePath.name
        with open(outPath, "wb") as file:
            file.write(template[0:replacementIdx].encode())
            file.write(data)
            file.write(template[replacementIdx + len(replaceStr) + 1:templateSize].encode())


# copy others
shutil.copy("home.html", buildDir / "home.html")
shutil.copy("style.css", buildDir / "style.css")

imagesPath = projectDir / "images"
shutil.copytree(imagesPath, buildDir / "images")

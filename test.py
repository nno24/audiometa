from mutagen.id3 import ID3, TIT2, TALB, TOWN

path = "snippet-dont-walk-away.mp3"
tags = ID3(path)
tags.add(TIT2(encoding=3, text="Dont walk away - test"))
tags.add(TALB(text="album1"))
tags.add(TOWN(text="Nikolay Cranner"))
print(tags.pprint())




# polygone

polyglot png file embedding

inspired by and based on <https://github.com/DavidBuchanan314/tweetable-polyglot-png>

## example

pack an mp3 within a zip file into a PNG image:
```sh
polygone pack -z ./test/funkwiki.png ./test/virtuabones_smoove.mp3 ./test/out/poly_funk_1.png
```

show the embedded file:
```sh
7z l ./test/out/poly_funk_1.png
```

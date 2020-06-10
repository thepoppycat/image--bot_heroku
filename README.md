# Image Bot backend 

## Dependencies

- python-opencv
https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku#51004957

- pytesseract
https://stackoverflow.com/a/56457594/12960862


Find the installation location by first entering the heroku bash terminal

`heroku run bash`

Then find the location using 

`$find -iname tessdata`

Finally set the config variable using 

`heroku config:set TESSDATA_PREFIX=[LOCATION HERE]` 

## Buildpacks 
- https://github.com/heroku/heroku-buildpack-apt
- heroku/python
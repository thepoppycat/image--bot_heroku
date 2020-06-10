# Image Bot backend 

Find the installation location by first entering the heroku bash terminal

`heroku run bash`

Then find the location using 

`$find -iname tessdata`

Finally set the config variable using 

`heroku config:set TESSDATA_PREFIX=[LOCATION HERE]`
M4All
=====

Introduction
------------
It is GUI app for Music. I have number of ideas which are being incorporated. Current focus is on Music Discovery. This is a huge side project and is being rapidly developed. 

Screenshots
------------
Latest Top Tracks
![Screenshot](https://github.com/munagekar/m4all/blob/master/toptrackscreen.jpg)

See Lyrics for Tracks
![Screenshot](https://github.com/munagekar/m4all/blob/master/songinfolyrics.jpg)

See the wiki for Tracks
![Screenshot](https://github.com/munagekar/m4all/blob/master/songinfowiki.jpg)


Supported Platforms
-------------------
M4All is built using Kivy, a cross platform python GUI framework. Thus it can be easily work on Windows, Linux and Android(not supported though, please build & debug on your own).

Installation Instructions
-------------------------

 - Android: Android Support Has been removed since it takes too much time affecting development. Anyone interested in Android Building & Debugging please contact me.
 - Linux: You need to get Kivy with all dependencies and run it
 - Windows: Need to get Kivy and all dependencies and run it.
 - IOS: Need to get Kivy and all dependencies and run it,should work hopefully , not Tested.
 
 Just a head's up the API key in the LastFM lfm.py module is missing. Obtain a free key and use the same. The m4all team would add in the key when a package is created through cythonized obfuscated encrypted code.
 
Why isn't it Packaged ?
-------------------------
 1. This application is not yet complete
 2. Packaging involves cythonizing the code and then using pyinstaller for Windows and Linux and this takes time
 3. Creation of Deb for Ubuntu Linux would need py2Deb package building, which I am not interested in.
 4. Apple Environment needs Apple devices for testing as well as building. And I don't own a single apple device.

Features
--------
Developed
 1. See the top tracks in the world
 2. See song info, playcount, listeners and lyrics.
 
Under Development
 1. Song information Screen Under Development.
 2. Image Compression with PIL
 3. UI design is not paid much attention to instead more time is spent on adding features. Improvement of ui is later concern.

The Team
--------

 - Abhishek Munagekar: Sole Team Member :-)
 - Debian Packaging: Need someone to package this to .deb. With the help of py2deb or stddeb or however possible and test the same for Ubuntu Linux
 - Ios Packaging: Need someone to test and package the code
 - Windows Packaging : Need someone to test and package the code for Windows so that easy to install.
 - UI Development : Need someone to make design and make changes to User Interface
 - Android Packaging : Need someone to test, debug & package for android.


A special thanks to last.fm, proudly powered by last.fm

Disclaimer
--------
As a end user of this software code you are responsible for any violation of law as per your area of residence. The M4All team isn't responsible for any use of this code. We do not host any content in app or on our own servers and merely act as content providers.


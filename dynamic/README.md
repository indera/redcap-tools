
Installing webdrivers
==================

# Firefox/PhantomJS
    sudo pip install selenium

# Safari:
    mkdir -p ~/drivers
    cd ~/drivers
    wget http://selenium-release.storage.googleapis.com/2.44/selenium-server-standalone-2.44.0.jar
    echo 'export SELENIUM_SERVER_JAR=`echo $HOME/drivers` >> ~/.bash_profile
    . ~/.bash_profile

# Chrome:
    cd ~/drivers
    wget http://chromedriver.storage.googleapis.com/2.13/chromedriver_mac32.zip
    unzip chromedriver_mac32.zip
    sudo mv chromedriver /usr/bin/


# Opera: (not working)
    https://github.com/operasoftware/operaprestodriver/blob/master/README.md


# balanc3r-for-ev3way

Robot balancing program for EV3way-ET. This program made by Python.<br>
You can see the self-balancing robot like segway in youtube.

https://www.youtube.com/watch?v=nxw2QlfK0tQ

# Prerequisite

You assemble self-balancing robot named EV3Way-ET.
And you install OS ev3dev.

- Body: [EV3Way-ET](https://github.com/ETrobocon/etroboEV3/wiki)
- OS: [ev3dev](http://www.ev3dev.org/)

# How to use

In host shell,  login your EV3Way-ET by ssh.

```shell
$ ssh username@xxx.xxx.xxx.xxx
```



In EV3(ev3dev) shell, get this repository and execute balancing program "BALANC3R".

```shell
$ git clone https://github.com/ETRobocon2017-TeamD/balanc3r-for-ev3way-et.git
$ cd balanc3r-for-ev3way-et
$ python3 BALANC3R
```



# Reference 

- [SC4050+ Integration Project: Balancing Robot](http://laurensvalk.com/files/Bos_Valk_SC4050_Balancing_Robot.pdf)
- [NXTWay-GS(Self-Balancing Tow-Wheeled Robot) Controller Design](http://jp.mathworks.com/matlabcentral/fileexchange/19147-nxtway-gs--self-balancing-two-wheeled-robot--controller-design)
- [ev3dev issue+ Tips to get a more constant loop time](https://github.com/ev3dev/ev3dev/issues/324)
- [segway](https://github.com/laurensvalk/segway)
- [ETrobocon/etroboEV3 (in Japanese)](https://github.com/ETrobocon/etroboEV3)




# Acknowledgements

We are grateful to [The ETrobocon 2017 executive committee](http://www.etrobo.jp/).<br>
We want to thank [segway](https://github.com/laurensvalk/segway) author [Laurens Valk](http://laurensvalk.com/), and [ev3dev-lang-python](https://github.com/rhempel/ev3dev-lang-python) developer [Ralph Hempel](https://github.com/rhempel) and commiters.


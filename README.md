# balanc3r-for-ev3way

Robot balancing program for EV3way-ET. This program made by Python.<br>
You can see the self-balancing robot like segway in youtube.

https://www.youtube.com/watch?v=sKaeCxrSDG8


# Prerequisite

- Body: [EV3Way-ET](https://github.com/ETrobocon/etroboEV3/wiki)
- OS:ev3dev
 - [ev3dev-stretch-2019-03-03](https://github.com/ev3dev/ev3dev/releases/download/ev3dev-stretch-2019-03-03/ev3dev-stretch-ev3-generic-2019-03-03.zip)
- Python: 3.5.3

# Development environment

## Docker

If your host OS is not linux, you should install vagrant. and then install debian-stretch into vm.

[Vagrant](https://www.vagrantup.com/)

Host shell
```
$ vagrant up
$ vagrant ssh
```

You will use EV3dev developer tool, you must install docker.

[DockerCE Ubuntu install](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

vm shell
```
$ sudo apt-get remove docker docker-engine docker.io containerd runc
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Install brickstrap tool, then you will run qemu-armel container.

vm shell
```
$ sudo add-apt-repository ppa:ev3dev/tools
$ sudo apt update
$ sudo apt install brickstrap
```

Get the container for developing ev3dev.

vm shell
```
$ sudo docker pull ev3dev/ev3dev-jessie-ev3-generic
$ sudo docker tag ev3dev/ev3dev-jessie-ev3-generic ev3jg
```

Check the container behaviour.

vm shell
```
$ sudo docker run --rm -it ev3jg su -l robot
```

[(optionnal) Manage Docker as a non-root user](https://docs.docker.com/install/linux/linux-postinstall/)

vm shell
```
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```

Install cython package

```
$ sudo apt install cython3
```

Build cross build container

vm shell
```
$ docker pull yjono/ev3jcrs
$ docker tag yjono/ev3jcrs ev3jsrs
```

or 

vm shell 
```
$ docker build -t balan3er-for-ev3way-et/ev3jsrs .
$ docker tag balan3er-for-ev3way-et/ev3jsrs ev3jsrs
```

# How to build(Python Extension Module)

## short script

vm shell
```
make
```

## description

Generate C source

vm shell
```
$ cython xxxx.pyx
```

Run the container for cross compile.

vm shell
```
$ docker run -it -v /host:/host ev3jcrs /bin/bash
$ docker run -it -v /host:/host ev3jsrs /bin/bash
```

or

host shell
```
$ docker run -it -v $HOME/src/github.com/ETRobocon2017-TeamD/balanc3r-for-ev3way-et:/host ev3jcrs /bin/bash
$ docker run -it -v $HOME/src/github.com/ETRobocon2017-TeamD/balanc3r-for-ev3way-et:/host ev3jsrs /bin/bash
```

ev3dev(jessie) python include dir

container shell
```
$ CFLAGS=$(arm-linux-gnueabi-python3-config --cflags) \
LDFLAGS=$(arm-linux-gnueabi-python3-config --ldflags) \
INCLUDES=$(arm-linux-gnueabi-python3-config --includes)
$ arm-linux-gnueabi-gcc ${INCLUDES} -c xxxx.c ${CFLAGS}
$ arm-linux-gnueabi-gcc xxxx.o -o xxxx.so -shared ${LDFLAGS}
```

# How to drive the EV3Way-ET

In host shell,  login your EV3Way-ET by ssh.

```shell
$ ssh username@xxx.xxx.xxx.xxx
```

In EV3(ev3dev) shell, Execute "ps lax" to find processes given "-20" nice value.

```shell
$ ps lax
F   UID   PID  PPID PRI  NI    VSZ   RSS WCHAN  STAT TTY        TIME COMMAND
4     0     1     0  20   0  23876  3640 -      Ss   ?          0:10 /sbin/init splash
1     0     2     0  20   0      0     0 -      S    ?          0:00 [kthreadd]
1     0     3     2  20   0      0     0 -      S    ?          0:01 [ksoftirqd/0]
1     0     4     2  20   0      0     0 -      S    ?          0:12 [kworker/0:0]
1     0     5     2   0 -20      0     0 -      S<   ?          0:00 [kworker/0:0H]
1     0     6     2  20   0      0     0 -      S    ?          0:02 [kworker/u2:0]
1     0     7     2  20   0      0     0 -      S    ?          0:01 [rcu_preempt]
1     0     8     2  20   0      0     0 -      S    ?          0:00 [rcu_sched]
1     0     9     2  20   0      0     0 -      S    ?          0:00 [rcu_bh]
5     0    10     2  20   0      0     0 -      S    ?          0:00 [kdevtmpfs]
1     0    11     2   0 -20      0     0 -      S<   ?          0:00 [netns]
1     0    12     2   0 -20      0     0 -      S<   ?          0:00 [writeback]
1     0    13     2   0 -20      0     0 -      S<   ?          0:00 [crypto]
1     0    14     2   0 -20      0     0 -      S<   ?          0:00 [bioset]
1     0    15     2   0 -20      0     0 -      S<   ?          0:00 [kblockd]
1     0    16     2  20   0      0     0 -      S    ?          0:00 [kworker/0:1]
1     0    17     2   0 -20      0     0 -      S<   ?          0:00 [rpciod]
1     0    18     2  20   0      0     0 -      S    ?          0:01 [kswapd0]
1     0    19     2  20   0      0     0 -      S    ?          0:00 [fsnotify_mark]
1     0    20     2   0 -20      0     0 -      S<   ?          0:00 [nfsiod]
1     0    43     2   0 -20      0     0 -      S<   ?          0:00 [bioset]
1     0    44     2   0 -20      0     0 -      S<   ?          0:00 [bioset]
1     0    45     2   0 -20      0     0 -      S<   ?          0:00 [bioset]
1     0    46     2   0 -20      0     0 -      S<   ?          0:00 [bioset]
1     0    47     2   0 -20      0     0 -      S<   ?          0:00 [bioset]
1     0    48     2 -51   -      0     0 -      S    ?          0:00 [irq/56-spi_davi]
1     0    49     2  20   0      0     0 -      S    ?          0:00 [spi1]
1     0    50     2 -51   -      0     0 -      S    ?          0:00 [irq/20-spi_davi]
1     0    51     2  20   0      0     0 -      S    ?          0:08 [spi0]
1     0    52     2  20   0      0     0 -      D    ?          0:01 [kworker/u2:1]
1     0    53     2   0 -20      0     0 -      S<   ?          0:00 [deferwq]
1     0    54     2  20   0      0     0 -      S    ?          0:03 [kworker/0:2]
1     0    55     2  20   0      0     0 -      S    ?          0:02 [kworker/u2:2]
1     0    56     2   0 -20      0     0 -      S<   ?          0:00 [bioset]
1     0    57     2  20   0      0     0 -      S    ?          0:02 [mmcqd/0]
1     0    58     2  20   0      0     0 -      S    ?          0:01 [kworker/0:3]
1     0    59     2  20   0      0     0 -      S    ?          0:00 [jbd2/mmcblk0p2-]
1     0    60     2   0 -20      0     0 -      S<   ?          0:00 [ext4-rsv-conver]
4     0    92     1  20   0   4044  1724 -      Ss   ?          0:00 /lib/systemd/systemd-journald
4     0   112     1  20   0  10844  2124 -      Ss   ?          0:01 /lib/systemd/systemd-udevd
1     0   206     2   0 -20      0     0 -      S<   ?          0:00 [cfg80211]
1     0   300     2  20   0      0     0 -      S    ?          0:00 [kworker/u2:3]
1     0   302     2  20   0      0     0 -      S    ?          0:00 [kworker/u2:4]
4   105   304     1  20   0   3844  2324 -      Ss   ?          0:00 avahi-daemon: running [ev3dev.local]
1     0   306     1  20   0   1760   548 -      Ss   ?          0:00 /usr/sbin/ldattach 29 /dev/tty_in4
1     0   307     1  20   0   1760   568 -      Ss   ?          0:00 /usr/sbin/ldattach 29 /dev/tty_in2
1     0   308     1  20   0   1760   524 -      Ss   ?          0:00 /usr/sbin/ldattach 29 /dev/tty_in3
4     0   315     1  20   0   3820  2244 -      Ss   ?          0:00 /lib/systemd/systemd-logind
1     0   316     2   0 -20      0     0 -      S<   ?          0:00 [kworker/u3:0]
1     0   317     2   0 -20      0     0 -      S<   ?          0:00 [hci0]
1     0   318     2   0 -20      0     0 -      S<   ?          0:00 [hci0]
1     0   319     2   0 -20      0     0 -      S<   ?          0:00 [kworker/u3:1]
1     0   320     2   0 -20      0     0 -      S<   ?          0:00 [kworker/u3:2]
4   104   322     1  20   0   5692  2408 -      Ss   ?          0:02 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activatio
1   105   334   304  20   0   3844  1396 -      S    ?          0:00 avahi-daemon: chroot helper
1     0   335     1  10 -10   2008   596 -      S<   ?          0:00 /usr/bin/hciattach -t 30 /dev/ttyS2 texas 2000000 flow nosleep
4     0   385     1  20   0   5000  1960 -      Ss   ?          0:00 /usr/lib/bluetooth/bluetoothd
4     0   387     1  20   0   7916  3604 -      Ss   ?          0:02 /usr/sbin/connmand -n
1     0   390     2   0 -20      0     0 -      S<   ?          0:00 [kworker/0:1H]
4     0   391     1  20   0   7916  3968 -      Ss   ?          0:00 /usr/sbin/sshd -D
4     0   402     1  20   0  53584  4552 -      Ssl+ tty1       0:07 /usr/sbin/brickman
4     0   407     1  20   0   7028  4324 -      Ds   ?          0:01 /sbin/wpa_supplicant -u -s -O /run/wpa_supplicant
5   106   520     1  20   0   5940  3016 -      Ss   ?          0:00 /usr/sbin/ntpd -p /var/run/ntpd.pid -g -u 106:110
1     0   526     2  20   0      0     0 -      S    ?          0:06 [kworker/0:4]
4     0   527   391  20   0  12172  5032 -      Ss   ?          0:02 sshd: robot [priv]
4  1000   537     1  20   0   4956  3288 SyS_ep Ss   ?          0:00 /lib/systemd/systemd --user
5  1000   540   537  20   0  25240  1844 -      S    ?          0:00 (sd-pam)
5  1000   543   527  20   0  12172  3524 -      S    ?          0:00 sshd: robot@pts/0
0  1000   545   543  20   0   3576  2804 wait   Ss   pts/0      0:00 -bash
5     0   556     1  20   0  21024  4484 -      Ss   ?          0:00 /usr/sbin/nmbd -D
0  1000   586   545  20   0   2624  1404 -      R+   pts/0      0:00 ps lax
```

And execute "renice" for all displayed processes to give "0" nice value.

```shell
$ ps lax | grep -- [-]20 | awk '{print $3}' | xargs sudo renice 0 -p
[sudo] password for robot:
5 (process ID) old priority -20, new priority 0
11 (process ID) old priority -20, new priority 0
12 (process ID) old priority -20, new priority 0
13 (process ID) old priority -20, new priority 0
14 (process ID) old priority -20, new priority 0
15 (process ID) old priority -20, new priority 0
17 (process ID) old priority -20, new priority 0
20 (process ID) old priority -20, new priority 0
43 (process ID) old priority -20, new priority 0
44 (process ID) old priority -20, new priority 0
45 (process ID) old priority -20, new priority 0
46 (process ID) old priority -20, new priority 0
47 (process ID) old priority -20, new priority 0
53 (process ID) old priority -20, new priority 0
56 (process ID) old priority -20, new priority 0
60 (process ID) old priority -20, new priority 0
206 (process ID) old priority -20, new priority 0
316 (process ID) old priority -20, new priority 0
317 (process ID) old priority -20, new priority 0
318 (process ID) old priority -20, new priority 0
319 (process ID) old priority -20, new priority 0
320 (process ID) old priority -20, new priority 0
390 (process ID) old priority -20, new priority 0
```

Then, Get this repository and execute "stop_deamons.sh".

```shell
$ git clone https://github.com/ETRobocon2017-TeamD/balanc3r-for-ev3way-et.git
$ cd balanc3r-for-ev3way-et
$ chmod 755 stop_daemons.sh
$ sudo ./stop_daemons.sh
[....] Stopping avahi-daemon (via systemctl): avahi-daemon.serviceWarning: Stopping avahi-daemon.service, but it can still be activated by:
  avahi-daemon.socket
. ok
```

After, Execute "pistol.py" by "nice" command to give "-12" nice value.

```shell
$ sudo nice -n -13 python3 pistol.py
```

# How to tuning parameter


## Setup jupyter for japanese 

**Find matplotlib, then write japanese fonts setting.**

```shell
sudo apt install fonts-takao-pgothic fonts-takao-mincho
```

```shell
$ pipenv shell

or

$ conda activate

$ python3
```

```python
>>> import matplotlib
>>> matplotlib.matplotlib_fname()
```

$HOME/.local/share/virtualenvs/balanc3r-for-ev3way-et-9y2obqay/lib/python3.5/site-packages/matplotlib/mpl-data/matplotlibrc

$HOME/.local/share/virtualenvs/balanc3r-for-ev3way-et-SkxC7aZY/lib/python3.4/site-packages/matplotlib/mpl-data/fonts/ttf

if matplot>=3.1.0 
```matplotlibrc
font.serif          : Noto Serif CJK JP, DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman, New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L, Times New Roman, Times, Palatino, Charter, serif

font.sans-serif     : Noto Sans CJK JP, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
```

else matplot<3.1.0
```matplotlibrc
font.serif          : TakaoPMincho, DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman, New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L, Times New Roman, Times, Palatino, Charter, serif

font.sans-serif     : TakaoPGothic, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
```

```shell
rm -rf ~/.cache/matplotlib/
```

TODO: Write usage Jupyter, pandas, matplotlib.


# Reference

- [SC4050+ Integration Project: Balancing Robot](http://laurensvalk.com/files/Bos_Valk_SC4050_Balancing_Robot.pdf)
- [NXTWay-GS(Self-Balancing Tow-Wheeled Robot) Controller Design](http://jp.mathworks.com/matlabcentral/fileexchange/19147-nxtway-gs--self-balancing-two-wheeled-robot--controller-design)
- [ev3dev issue+ Tips to get a more constant loop time](https://github.com/ev3dev/ev3dev/issues/324)
- [laurensvalk/segway](https://github.com/laurensvalk/segway)
- [ETrobocon/etroboEV3 (in Japanese)](https://github.com/ETrobocon/etroboEV3)
- [Linux超入門 (in Japanese)](http://shop.cqpub.co.jp/hanbai/books/44/44721.html)
- [制御のためのMATLAB (in Japanese)](http://www.tdupress.jp/bd/isbn/9784501327606/)
- [MATLAB/Simulinkによるやさしいシステム制御工学 (in Japanese)](https://www.morikita.co.jp/books/book/2355)
- [倒立振子で学ぶ制御工学 (in Japanese)](http://www.morikita.co.jp/books/book/3110)


# Acknowledgements

We are grateful to [The ETrobocon 2017 executive committee](http://www.etrobo.jp/).

We want to thank [segway](https://github.com/laurensvalk/segway) author [Laurens Valk](http://laurensvalk.com/), and [ev3dev-lang-python](https://github.com/rhempel/ev3dev-lang-python) developer [Ralph Hempel](https://github.com/rhempel) and commiters.


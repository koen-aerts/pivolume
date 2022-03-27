#!/usr/bin/env python3

from gpiozero import Button
import subprocess
import time

VOL_ADD = 1
VOL_MIN = 60
VOL_MAX = 100

VOL_CMD_GET = "get HDMI"
VOL_CMD_SET = "set HDMI {}%"

buttonUp = Button(19)
buttonDown = Button(26)

direction = 0
level = -1;

def getVolume():
  global level
  output = execVolumeApp(VOL_CMD_GET)
  lines = output.readlines()
  stat = lines[-1].decode('utf-8')
  p1 = stat.index('[') + 1
  p2 = stat.index('%')
  pct = stat[p1:p2]
  level = int(pct)


def execVolumeApp(cmd):
  prc = subprocess.Popen("amixer {}".format(cmd), shell=True, stdout=subprocess.PIPE)
  stat = prc.wait()
  if stat != 0:
    raise Error("Error executing amixer")
    sys.exit(0)
  return prc.stdout

def setVolume():
  global level
  if direction == 0:
    return
  getVolume();
  if direction == 1:
    if level < VOL_MAX:
      level += VOL_ADD
      execVolumeApp(VOL_CMD_SET.format(level))
      getVolume();
      print("Volume: {}%".format(level))
    else:
      print("Maxed out.")
  elif direction == -1:
    if level > VOL_MIN:
      level -= VOL_ADD
      execVolumeApp(VOL_CMD_SET.format(level))
      getVolume();
      print("Volume: {}%".format(level))
    else:
      print("Bottomed out.")


def volume_up():
  global direction
  direction = 1


def volume_down():
  global direction
  direction = -1


def volume_keep():
  global direction
  direction = 0


def main():
  try:
    getVolume();
    print("Volume: {}%".format(level))
    buttonUp.when_pressed = volume_up
    buttonUp.when_released = volume_keep
    buttonDown.when_pressed = volume_down
    buttonDown.when_released = volume_keep
    while 1:
      setVolume()
      time.sleep(0.2)
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()

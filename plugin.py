import pigpio, time, socket, signal, sys, threading, queue

class Plugin:
  FILTER = []
  PATHDBT = "gps.STALK1_DBT"
  PATHSTW = "gps.STALK1_STW"
  CONFIG=[
    {
      'name': 'gpio',
      'description': 'Define gpio where the SeaTalk1 (yellow wire) is sensed (default is 4 => GPIO4 on pin 7)',
      'default': '4'
    },
    {
      'name': 'inverted',
      'description': 'Define if input signal shall be inverted 0 => not inverted, 1 => Inverted (default is 1)',
      'default': '1'
    },
    {
      'name': 'pulldown',
      'description': 'Define if using internal RPi pull up/down 0 => No, 1= Pull down, 2=Pull up (default is 2)',
      'default': '2'
    }    
  ]
  @classmethod
  def pluginInfo(cls):
    """
    the description for the module
    @return: a dict with the content described below
            parts:
               * description (mandatory)
               * data: list of keys to be stored (optional)
                 * path - the key - see AVNApi.addData, all pathes starting with "gps." will be sent to the GUI
                 * description
    """
    return {
      'description': 'seatalk 1 protocol reader',
      'config': cls.CONFIG,
      'data': [
        {
          'path': cls.PATHDBT,
          'description': 'deepth below transducer',
        },
        {
          'path': cls.PATHSTW,
          'description': 'speed trough water',
        },
      ]
    }

  def __init__(self,api):
    """
        initialize a plugins
        do any checks here and throw an exception on error
        do not yet start any threads!
        @param api: the api to communicate with avnav
        @type  api: AVNApi
    """
    self.api = api # type: AVNApi
    #we register an handler for API requests
    self.gpio='4'
    self.inverted='1'
    self.pulldown='2'
    self.isConnected=False
    if hasattr(self.api,'registerEditableParameters'):
      self.api.registerEditableParameters(self.CONFIG,self._changeConfig)
    if hasattr(self.api,'registerRestart'):
      self.api.registerRestart(self._apiRestart)
    self.changeSequence=0
    self.startSequence=0
    self.st1read =pigpio.pi()
    try:
        st1read.bb_serial_read_close(int(gpio)) #close if already run
    except:
        pass

    self.queue = queue.Queue()

  def _apiRestart(self):
    self.startSequence+=1
    self.changeSequence+=1

  def _changeConfig(self,newValues):
    self.api.saveConfigValues(newValues)
    self.changeSequence+=1

  def getConfigValue(self,name):
    defaults=self.pluginInfo()['config']
    for cf in defaults:
      if cf['name'] == name:
        return self.api.getConfigValue(name,cf.get('default'))
    return self.api.getConfigValue(name)

  def run(self):
    startSequence=self.startSequence
    while startSequence == self.startSequence:
      self.runInternal()

  def runInternal(self):
    """
    the run method
    this will be called after successfully instantiating an instance
    this method will be called in a separate Thread
    The plugin sends every 10 seconds the depth value via seatalk
    @return:
    """
    changeSequence=self.changeSequence
    seq=0
    self.api.log("started")
    self.api.setStatus('STARTED', 'running')
    enabled=self.getConfigValue('enabled')
    if enabled is not None and enabled.lower()!='true':
      self.api.setStatus("INACTIVE", "disabled by config")
      return
    try:
      self.gpio=self.getConfigValue('gpio')
      self.inverted=self.getConfigValue('inverted')
      self.pulldown=self.getConfigValue('pulldown')
    except Exception as e:
      self.api.setStatus("ERROR", "config error %s "%str(e))

    connectionHandler=threading.Thread(target=self.handleConnection, name='seatalk1-reader-rpi-gpio')
    connectionHandler.setDaemon(True)
    connectionHandler.start()

    #seq, data = self.api.fetchFromQueue(seq, number=100, waitTime=100, includeSource=True,filter=self.FILTER)

    while changeSequence == self.changeSequence:
      #if not self.isConnected:
        #return {'status': 'not connected'}

      source='internal'


      try:
        item = self.queue.get(block=True, timeout=10)
        data = item.split("\r")
        self.api.debug("Read from queue: '" + str(data[0]) + "'")
        darray = data[0].split(",")
        if ( darray[0] == '$STALK' ):

            ''' DPT: 00  02  YZ  XX XX  Depth below transducer: XXXX/10 feet'''
            if((darray[1] == '00') and (darray[2] == '02') and (darray[3] == '00')):
              rt={}
              value=int('0x' + str(darray[4]),base=16) + (int('0x'+ str(darray[5]), base=16)*255)
              self.api.debug("Get DBT SEATALK frame: " + str(value) + "'")
              rt['DBT'] = float(value or '0') / (10.0 * 3.281)
              self.api.addData(self.PATHDBT, rt['DBT'],source=source)

#                DBT - Depth below transducer
#                1   2 3   4 5   6 7
#                |   | |   | |   | |
#
#        $--DBT,x.x,f,x.x,M,x.x,F*hh<CR><LF>
#        Field Number:
#         1) Depth, feet
#         2) f = feet
#         3) Depth, meters
#         4) M = meters
#         5) Depth, Fathoms
#         6) F = Fathoms
#         7) Checksum

            ''' STW: 20  01  XX  XX  Speed through water: XXXX/10 Knots'''
            if((darray[1] == '20') and (darray[2] == '01')):
              rt={}
              value=int('0x' + str(darray[3]),base=16) + (int('0x'+ str(darray[4]), base=16)*255)
              self.api.debug("Get STW SEATALK frame: " + str(value) + " (0x" + str(darray[4]) +  str(darray[3]) + ")")
              rt['STW'] = ((float(value or '0') / 10.0) * 1.852) / 3.6
              self.api.addData(self.PATHSTW, rt['STW'],source=source)

      #VHW - Water speed and heading

      #        1   2 3   4 5   6 7   8 9
      #        |   | |   | |   | |   | |
      # $--VHW,x.x,T,x.x,M,x.x,N,x.x,K*hh<CR><LF>

      # Field Number:
      #  1) Degress True
      #  2) T = True
      #  3) Degrees Magnetic
      #  4) M = Magnetic
      #  5) Knots (speed of vessel relative to the water)
      #  6) N = Knots
      #  7) Kilometers (speed of vessel relative to the water)
      #  8) K = Kilometers
      #  9) Checksum


      except Exception as e:
        self.api.error("unable to read from queue: " + str(e))
        self.api.addData(self.PATHDBT, float('0'),source=source)
        self.api.addData(self.PATHSTW, float('0'),source=source)
        pass

  def handleConnection(self):
    changeSequence=self.changeSequence
    errorReported=False
    last_gpio=-1
    while changeSequence == self.changeSequence:
      if int(self.gpio) >= 0:
        if int(self.gpio) != last_gpio:
          self.api.setStatus("STARTED", "trying to connect to GPIO%s (inverted:%s)" % (self.gpio, self.inverted))
          last_gpio=int(self.gpio)
        self.isConnected=False
        self.isBusy=False

        try:
          self.st1read.bb_serial_read_close(int(self.gpio)) #close if already run
        except:
          pass

        try:
          self.st1read.bb_serial_read_open(int(self.gpio), 4800,9)
          self.st1read.bb_serial_invert(int(self.gpio), int(self.inverted))	# Invert data
          self.st1read.set_pull_up_down(int(self.gpio), int(self.pulldown))	# Set pull up/down

          self.api.setStatus("NMEA","connected to GPIO%s (inverted:%s)" % (self.gpio, self.inverted))
          self.api.log("connected to GPIO%s (inverted:%s)" % (self.gpio, self.inverted))
          self.isConnected=True
          errorReported=False
          data=""
          while True:
            out=(self.st1read.bb_serial_read(int(self.gpio)))
            out0=out[0]
            if out0>0:
                out_data=out[1]
                x=0
                while x < out0:
                    #self.api.log("Get Data: " + str(out_data[x]) + ": " + str(out_data[x+1]))
                    if out_data[x+1] ==0:
                        string1=str(hex(out_data[x]))
                        data1=str(string1[2:])
                        if (len(data1)==1):
                            data1="0"+data1
                        data= data+data1+ ","
                        #self.api.log("Byte: " + str(data1))
                    else:
                        data=data[0:-1]
                        data="$STALK,"+data
                        #self.api.log("Got SEATALK frame: '" + str(data) + "'")
                        data=data+"\r\n"
                        self.queue.put(data)
                        string2=str(hex(out_data[x]))
                        string2_new=string2[2:]
                        if len(string2_new)==1:
                            string2_new="0"+string2_new
                        data=string2_new + ","
                    x+=2

        except Exception as e:
          if not errorReported:
            self.api.setStatus("ERROR","unable to connect/connection lost to GPIO%s: %s"%(self.gpio, str(e)))
            self.api.error("unable to connect/connection lost to GPIO%s: %s" % (self.gpio, str(e)))
            errorReported=True
          else:
            self.api.error("unable to connect/connection lost to GPIO%s: %s" % (self.gpio, str(e)))

          self.isConnected=False
          time.sleep(1)
      time.sleep(1)


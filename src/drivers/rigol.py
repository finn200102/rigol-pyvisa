import pyvisa 

class Rigol:
    def __init__(self, ip_address):
        """Initialize connection to Rigol oscilloscope.

        Args:
            ip_address (str): IP address of the oscilloscope

        Raises:
            pyvisa.errors.VisaIOError: If connection fails
        """
        self.rm = pyvisa.ResourceManager('@py')
        self.osci = self.rm.open_resource(f'TCPIP::{ip_address}::INSTR')
        self.osci.timeout = 2000
        self.osci.read_termination = '\n'
        self.osci.write_termination = '\n'
        print(self.osci.query('*IDN?'))


    def configure_channel(self, channel, scale, coupling):
        """Configure oscilloscope channel settings.

        Args:
            channel (int): Channel number (1-4)
            scale (float): Vertical scale in V/div
            coupling (str): Coupling mode ('AC', 'DC', or 'GND')
        """
        self.osci.write(f":CHANnel{channel}:DISPlay ON")
        self.osci.write(f":CHANnel{channel}:SCALe {scale}")
        self.osci.write(f":CHANnel{channel}:COUPling {coupling}")

    def setup_trigger(self, source, level, mode):
        """Configure trigger settings.

        Args:
            source (int): Trigger source channel (1-4)
            level (float): Trigger level in volts
            mode (str): Trigger mode ('AUTO', 'NORMAL', or 'SINGLE')
        """
        self.osci.write(f':TRIG:EDGE:SOURce CHAN{source}')
        self.osci.write(f':TRIG:EDGE:LEV {level}')
        self.osci.write(f':TRIG:SWE {mode}')

    def get_time_step(self):
        """Get time between waveform points.

        Returns:
            float: Time increment between points in seconds
        """
        return float(self.osci.query(':WAV:XINC?'))
    
    def set_memory_depth(self, memory_depth):
        """Set acquisition memory depth.

        Args:
            memory_depth (int): Memory depth in points
            Allowed values depend on oscilloscope model
        """
        self.osci.write(f':ACQuire:MDEPth {memory_depth}')
    
    def get_memory_depth(self):
        """Get current memory depth setting.

        Returns:
            str: Current memory depth setting
        """
        return self.osci.query(':ACQuire:MDEPth?')

    def acquire_waveform(self, channel, mode, points):
        """Acquire waveform data from specified channel.

        Args:
            channel (int): Channel number (1-4)
            mode (str): Acquisition mode ('NORM', 'MAX', or 'RAW')
            points (int): Number of points to acquire

        Returns:
            str: Waveform data in ASCII format
        """
        self.osci.write(f':WAV:SOUR CHAN{channel}')
        self.osci.write(f':WAV:MODE {mode}')
        self.osci.write(f':WAV:POIN {points}')
        self.osci.write(':WAV:FORM ASC')
        return self.osci.query(':WAV:DATA?')
    
    def get_trigger_status(self):
        """Get current trigger status.

        Returns:
            str: Trigger status ('TD', 'WAIT', 'RUN', 'AUTO', or 'STOP')
        """
        return self.osci.query(':TRIG:STAT?').strip()

    def close(self):
        """Close connection to oscilloscope."""
        if self.osci:
            self.osci.close()

    def set_time_scale(self, time_scale):
        """Set horizontal time scale.

        Args:
            time_scale (float): Time per division in seconds
        """
        self.osci.write(f":TIMebase:MAIN:SCALe {time_scale}")
    
    def set_time_offset(self, time_offset):
        """Set horizontal time offset.

        Args:
            time_offset (float): Time offset in seconds relative to trigger point
        """
        self.osci.write(f":TIMebase:MAIN:OFFSet {time_offset}")
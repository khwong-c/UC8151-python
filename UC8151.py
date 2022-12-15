from machine import SPI, Pin
from time import sleep_ms
Enum = object


class UC8151:
    class REG(Enum):
        PSR      = b'\x00'
        PWR      = b'\x01'
        POF      = b'\x02'
        PFS      = b'\x03'
        PON      = b'\x04'
        PMES     = b'\x05'
        BTST     = b'\x06'
        DSLP     = b'\x07'
        DTM1     = b'\x10'
        DSP      = b'\x11'
        DRF      = b'\x12'
        DTM2     = b'\x13'
        LUT_VCOM = b'\x20'
        LUT_WW   = b'\x21'
        LUT_BW   = b'\x22'
        LUT_WB   = b'\x23'
        LUT_BB   = b'\x24'
        PLL      = b'\x30'
        TSC      = b'\x40'
        TSE      = b'\x41'
        TSR      = b'\x43'
        TSW      = b'\x42'
        CDI      = b'\x50'
        LPD      = b'\x51'
        TCON     = b'\x60'
        TRES     = b'\x61'
        REV      = b'\x70'
        FLG      = b'\x71'
        AMV      = b'\x80'
        VV       = b'\x81'
        VDCS     = b'\x82'
        PTL      = b'\x90'
        PTIN     = b'\x91'
        PTOU     = b'\x92'
        PGM      = b'\xa0'
        APG      = b'\xa1'
        ROTP     = b'\xa2'
        CCSET    = b'\xe0'
        PWS      = b'\xe3'
        TSSET    = b'\xe5'

    class PSR_FLAGS(Enum):
        RES_96x230    = 0b00000000
        RES_96x252    = 0b01000000
        RES_128x296   = 0b10000000
        RES_160x296   = 0b11000000

        LUT_OTP       = 0b00000000
        LUT_REG       = 0b00100000

        FORMAT_BWR    = 0b00000000
        FORMAT_BW     = 0b00010000

        SCAN_DOWN     = 0b00000000
        SCAN_UP       = 0b00001000

        SHIFT_LEFT    = 0b00000000
        SHIFT_RIGHT   = 0b00000100

        BOOSTER_OFF   = 0b00000000
        BOOSTER_ON    = 0b00000010

        RESET_SOFT    = 0b00000000
        RESET_NONE    = 0b00000001

    class PWR_FLAGS_1(Enum):
        VDS_EXTERNAL  = 0b00000000
        VDS_INTERNAL  = 0b00000010

        VDG_EXTERNAL  = 0b00000000
        VDG_INTERNAL  = 0b00000001

    class PWR_FLAGS_2(Enum):
        VCOM_VD       = 0b00000000
        VCOM_VG       = 0b00000100

        VGHL_16V      = 0b00000000
        VGHL_15V      = 0b00000001
        VGHL_14V      = 0b00000010
        VGHL_13V      = 0b00000011

    class BOOSTER_FLAGS(Enum):
        START_10MS    = 0b00000000
        START_20MS    = 0b01000000
        START_30MS    = 0b10000000
        START_40MS    = 0b11000000

        STRENGTH_1    = 0b00000000
        STRENGTH_2    = 0b00001000
        STRENGTH_3    = 0b00010000
        STRENGTH_4    = 0b00011000
        STRENGTH_5    = 0b00100000
        STRENGTH_6    = 0b00101000
        STRENGTH_7    = 0b00110000
        STRENGTH_8    = 0b00111000

        OFF_0_27US    = 0b00000000
        OFF_0_34US    = 0b00000001
        OFF_0_40US    = 0b00000010
        OFF_0_54US    = 0b00000011
        OFF_0_80US    = 0b00000100
        OFF_1_54US    = 0b00000101
        OFF_3_34US    = 0b00000110
        OFF_6_58US    = 0b00000111

    class PFS_FLAGS(Enum):
        FRAMES_1      = 0b00000000
        FRAMES_2      = 0b00010000
        FRAMES_3      = 0b00100000
        FRAMES_4      = 0b00110000

    class TSE_FLAGS(Enum):
        TEMP_INTERNAL = 0b00000000
        TEMP_EXTERNAL = 0b10000000

        OFFSET_0      = 0b00000000
        OFFSET_1      = 0b00000001
        OFFSET_2      = 0b00000010
        OFFSET_3      = 0b00000011
        OFFSET_4      = 0b00000100
        OFFSET_5      = 0b00000101
        OFFSET_6      = 0b00000110
        OFFSET_7      = 0b00000111

        OFFSET_MIN_8  = 0b00001000
        OFFSET_MIN_7  = 0b00001001
        OFFSET_MIN_6  = 0b00001010
        OFFSET_MIN_5  = 0b00001011
        OFFSET_MIN_4  = 0b00001100
        OFFSET_MIN_3  = 0b00001101
        OFFSET_MIN_2  = 0b00001110
        OFFSET_MIN_1  = 0b00001111

    class PLL_FLAGS(Enum):
        HZ_29         = 0b00111111
        HZ_33         = 0b00111110
        HZ_40         = 0b00111101
        HZ_50         = 0b00111100
        HZ_67         = 0b00111011
        HZ_100        = 0b00111010
        HZ_150        = 0b00101001
        HZ_200        = 0b00111001

    LUTS = {
        'default': {
            REG.LUT_VCOM:
                b'\x00\x64\x64\x37\x00\x01'
                b'\x00\x8c\x8c\x00\x00\x04'
                b'\x00\x64\x64\x37\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00',
            REG.LUT_WW:
                b'\x54\x64\x64\x37\x00\x01'
                b'\x60\x8c\x8c\x00\x00\x04'
                b'\xa8\x64\x64\x37\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BW:
                b'\x54\x64\x64\x37\x00\x01'
                b'\x60\x8c\x8c\x00\x00\x04'
                b'\xa8\x64\x64\x37\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_WB:
                b'\xa8\x64\x64\x37\x00\x01'
                b'\x60\x8c\x8c\x00\x00\x04'
                b'\x54\x64\x64\x37\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BB:
                b'\xa8\x64\x64\x37\x00\x01'
                b'\x60\x8c\x8c\x00\x00\x04'
                b'\x54\x64\x64\x37\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.PLL: PLL_FLAGS.HZ_100,
        },
        'medium': {
            REG.LUT_VCOM:
                b'\x00\x16\x16\x0d\x00\x01'
                b'\x00\x23\x23\x00\x00\x02'
                b'\x00\x16\x16\x0d\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00',
            REG.LUT_WW:
                b'\x54\x16\x16\x0d\x00\x01'
                b'\x60\x23\x23\x00\x00\x02'
                b'\xa8\x16\x16\x0d\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BW:
                b'\x54\x16\x16\x0d\x00\x01'
                b'\x60\x23\x23\x00\x00\x02'
                b'\xa8\x16\x16\x0d\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_WB:
                b'\xa8\x16\x16\x0d\x00\x01'
                b'\x60\x23\x23\x00\x00\x02'
                b'\x54\x16\x16\x0d\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BB:
                b'\xa8\x16\x16\x0d\x00\x01'
                b'\x60\x23\x23\x00\x00\x02'
                b'\x54\x16\x16\x0d\x00\x01'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.PLL: PLL_FLAGS.HZ_100,
        },
        'fast': {
            REG.LUT_VCOM:
                b'\x00\x04\x04\x07\x00\x01'
                b'\x00\x0c\x0c\x00\x00\x02'
                b'\x00\x04\x04\x07\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00',
            REG.LUT_WW:
                b'\x54\x04\x04\x07\x00\x01'
                b'\x60\x0c\x0c\x00\x00\x02'
                b'\xa8\x04\x04\x07\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BW:
                b'\x54\x04\x04\x07\x00\x01'
                b'\x60\x0c\x0c\x00\x00\x02'
                b'\xa8\x04\x04\x07\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_WB:
                b'\xa8\x04\x04\x07\x00\x01'
                b'\x60\x0c\x0c\x00\x00\x02'
                b'\x54\x04\x04\x07\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BB:
                b'\xa8\x04\x04\x07\x00\x01'
                b'\x60\x0c\x0c\x00\x00\x02'
                b'\x54\x04\x04\x07\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.PLL: PLL_FLAGS.HZ_100,
        },
        'turbo': {
            REG.LUT_VCOM:
                b'\x00\x01\x01\x02\x00\x01'
                b'\x00\x02\x02\x00\x00\x02'
                b'\x00\x02\x02\x03\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00',
            REG.LUT_WW:
                b'\x54\x01\x01\x02\x00\x01'
                b'\x60\x02\x02\x00\x00\x02'
                b'\xa8\x02\x02\x03\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BW:
                b'\x54\x01\x01\x02\x00\x01'
                b'\x60\x02\x02\x00\x00\x02'
                b'\xa8\x02\x02\x03\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_WB:
                b'\xa8\x01\x01\x02\x00\x01'
                b'\x60\x02\x02\x00\x00\x02'
                b'\x54\x02\x02\x03\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.LUT_BB:
                b'\xa8\x01\x01\x02\x00\x01'
                b'\x60\x02\x02\x00\x00\x02'
                b'\x54\x02\x02\x03\x00\x02'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00',
            REG.PLL: PLL_FLAGS.HZ_100,
        },
    }
    UPDATE_TIME = {
        'default'   : 4500,
        'medium'    : 2000,
        'fast'      : 800,
        'turbo'     : 250,
    }

    def __init__(self, spi_inst,
                 pin_cs=17, pin_dc=20, pin_reset=21, pin_busy=26):
        # Config
        self.update_speed = 'default'
        self.pixel_inverted = True

        self.spi: SPI = spi_inst

        # Init Pins
        self.pin_cs = Pin(pin_cs, mode=Pin.OUT)
        self.pin_dc = Pin(pin_dc, mode=Pin.OUT)
        self.pin_reset = Pin(pin_reset, mode=Pin.OUT)
        self.pin_busy = Pin(pin_busy, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin_cs(True)
        self.pin_reset(True)

        # Set up the Device
        self._setup()

    # Status
    def is_busy(self):
        return not self.pin_busy()

    def busy_wait(self):
        while self.is_busy():
            pass

    def reset(self):
        self.pin_reset(False)
        sleep_ms(10)
        self.pin_reset(True)
        sleep_ms(10)
        self.busy_wait()

    def power_off(self):
        self.busy_wait()
        self._command(UC8151.REG.POF)

    # Graphics
    def update(self, graphics, blocking=True):
        self.busy_wait()

        self._command(UC8151.REG.PON)              # Turn on Device
        self._command(UC8151.REG.PTOU)             # Disable partial mode
        self._command(UC8151.REG.DTM2, graphics)   # Transmit Pixel Data
        self._command(UC8151.REG.DSP)              # Transmission Stop
        self._command(UC8151.REG.DRF)              # Display Refresh

        if blocking:
            self.power_off()

    def partial_update(self, graphics, region, blocking=True):
        # Region is a Tuple of (X,Y,W,H)
        x, y, w, h = region
        partial_window = [
            y & 0xF8,
            ((y+h-1) & 0xFF) | 0x03,
            (x >> 8) & 0x01,
            x & 0xFF,
            ((x+w-1) >> 8) & 0x01,
            (x+w-1) & 0xFF,
            0x01
        ]
        self.busy_wait()

        self._command(UC8151.REG.PON)              # Turn on Device
        self._command(UC8151.REG.PTIN)             # Enable partial mode
        self._command(UC8151.REG.PTL, partial_window)  # Set Window
        self._command(UC8151.REG.DTM2, graphics)   # Transmit Pixel Data
        self._command(UC8151.REG.DSP)              # Transmission Stop
        self._command(UC8151.REG.DRF)              # Display Refresh

        if blocking:
            self.power_off()

    # Config Operations
    def set_update_speed(self, update_speed):
        self.update_speed = update_speed
        self._setup()

    def get_update_speed(self):
        return self.update_speed

    def get_update_time(self):
        return UC8151.UPDATE_TIME.get(
            self.update_speed, UC8151.UPDATE_TIME['default']
        )

    # Setup
    def _setup(self):
        self.reset()

        # Panel Setting
        psr_setting = \
            UC8151.PSR_FLAGS.RES_128x296 + \
            UC8151.PSR_FLAGS.FORMAT_BW + \
            UC8151.PSR_FLAGS.BOOSTER_ON + \
            UC8151.PSR_FLAGS.RESET_NONE
        psr_setting += UC8151.PSR_FLAGS.LUT_OTP if self.update_speed == 'default' else UC8151.PSR_FLAGS.LUT_REG
        # psr_setting |= rotation == ROTATE_180 ? SHIFT_LEFT | SCAN_UP : SHIFT_RIGHT | SCAN_DOWN;
        psr_setting += UC8151.PSR_FLAGS.SHIFT_LEFT + UC8151.PSR_FLAGS.SCAN_UP
        self._command(UC8151.REG.PSR, psr_setting)

        # Update LUTS
        setup_steps = UC8151.LUTS.get(self.update_speed, {})
        for reg, data in setup_steps.items():
            self._command(reg, data)

        # Power Setting
        self._command(UC8151.REG.PWR, (
            UC8151.PWR_FLAGS_1.VDS_INTERNAL + UC8151.PWR_FLAGS_1.VDG_INTERNAL,
            UC8151.PWR_FLAGS_2.VCOM_VD + UC8151.PWR_FLAGS_2.VGHL_16V,
            0b00101011,
            0b00101011,
            0b00101011,
        ))

        # Power On
        self._command(UC8151.REG.PON)
        self.busy_wait()

        # Set Booster Soft Start
        self._command(UC8151.REG.BTST, (
            UC8151.BOOSTER_FLAGS.START_10MS + UC8151.BOOSTER_FLAGS.STRENGTH_3 + UC8151.BOOSTER_FLAGS.OFF_6_58US,
            UC8151.BOOSTER_FLAGS.START_10MS + UC8151.BOOSTER_FLAGS.STRENGTH_3 + UC8151.BOOSTER_FLAGS.OFF_6_58US,
            UC8151.BOOSTER_FLAGS.START_10MS + UC8151.BOOSTER_FLAGS.STRENGTH_3 + UC8151.BOOSTER_FLAGS.OFF_6_58US,
        ))

        # Power Off Sequence
        self._command(UC8151.REG.PFS, UC8151.PFS_FLAGS.FRAMES_1)

        # Temperature Sensor: Internal
        self._command(UC8151.REG.TSE, UC8151.TSE_FLAGS.TEMP_INTERNAL + UC8151.TSE_FLAGS.OFFSET_0)

        # TCON, VCom and Data Interval Setting
        self._command(UC8151.REG.TCON, 0x22)
        self._command(UC8151.REG.CDI, 0b10011100 if self.pixel_inverted else 0b01001100)

        self.power_off()

    # Data Transaction
    def _read(self, reg, read_len):
        self.pin_cs(0)
        self.pin_dc(0)
        self.spi.write(reg)
        self.pin_dc(1)
        result = self.spi.read(read_len)
        self.pin_cs(1)
        return result

    def _command(self, reg, data=None):
        if data is None:
            data_available = False
        else:
            if isinstance(data, int):
                data = (data,)
            if isinstance(data, list) or isinstance(data, tuple):
                data = bytes(data)
            data_available = len(data) > 0

        self.pin_cs(0)

        self.pin_dc(0)
        self.spi.write(reg)
        if data_available:
            self.pin_dc(1)
            self.spi.write(data)

        self.pin_cs(1)

    def _data(self, data):
        if isinstance(data, int):
            data = (data,)
        if isinstance(data, list) or isinstance(data, tuple):
            data = bytes(data)
        self.pin_cs(0)
        self.pin_dc(1)
        self.spi.write(data)
        self.pin_cs(1)

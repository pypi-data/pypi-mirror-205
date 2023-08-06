from enum import Enum, Flag, IntFlag
from typing import *
from typing import BinaryIO
import struct
import io
import numpy as np


try:
    # Import h5py for optional hdf5 support
    import h5py
    import datetime
    H5PY_AVAILABLE = True
except ImportError:
    H5PY_AVAILABLE = False

class SenseX1000Base(object):
    USB_VID: int = 0x1FC9
    USB_PID: int = 0x8271

    class IPVersion(Enum):
        IPV4 = 4
        IPV6 = 6

    class IPv4AutoconfStatus(Enum):
        OFF = 0
        PROBING = 1
        ANNOUNCING = 2
        BOUND = 3

    class IPv6AutoconfStatus(Enum):
        NOTIMPLEMENTED = 0

    class IPv4DHCPStatus(Enum):
        OFF = 0
        REQUESTING = 1
        INIT = 2
        REBOOTING = 3
        REBINDING = 4
        RENEWING = 5
        SELECTING = 6
        INFORMING = 7
        CHECKING = 8
        PERMANENT = 9
        BOUND = 10
        RELEASING = 11
        BACKINGOFF = 12

    class IPv6DHCPStatus(Enum):
        NOTIMPLEMENTED = 0

    class PowerLevel(Enum):
        UNKNOWN = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        AUTO = 4

    class RadarState(Enum):
        OFF = 0
        STANDBY = 11
        IDLE = 12
        BUSY = 15
        DETECTFAIL = 40
        MAGICFAIL = 45

    # Enums for CONTrol subsystem
    class RampMode(Enum):
        """Ramp mode used with CONTrol:RADAR:MPLL:RMODe"""
        SINGLE = 0
        """Perform single ramps on each trigger"""
        DOUBLE = 1
        """Perform double ramps on each trigger"""
        ALTERNATING = 2
        """Perform alternating ramps on each trigger"""

    class ChannelCoupling(Enum):
        """Frontend coupling of receive channel used with CONTrol:RADAR:FRONtend:CHANnel#:COUPling"""
        GND = 0
        """Set GND channel coupling"""
        DC = 1
        """Set DC channel coupling"""
        AC = 2
        """Set AC channel coupling (R^2 compensation)"""

    class ChannelForce(Enum):
        """Frontend channel force used with CONTrol:RADAR:FRONtend:CHANnel#:FORCe"""
        NONE = 0
        """Do not force channel state"""
        ON = 1,
        """Force channel to always-on"""
        OFF = 2
        """Force channel to always-off"""

    # Enums for SENSe subsystem
    class FrequencyMode(Enum):
        """Frequency mode used with SENSe:FREQuency:MODE"""
        CW = 0
        """Operate in continuous wave mode on a single frequency (aka zero-span)"""
        SWEEP = 1
        """Operate in swept mode (normal)"""

    class SweepDirection(Enum):
        """Sweep direction used with SENSe:SWEep:DIRection"""
        DOWN = -1
        """Sweep slope of (first) sweep is down"""
        UP = 1
        """Sweep slope of (first) sweep is up"""

    class SweepMode(Enum):
        """Sweep mode used with SENSe:SWEep:MODE"""
        NORMAL = 0
        """Sweep slope is constant with jump back to start frequency at the end of sweep"""
        ALTERNATING = 1
        """Sweep slope is alternating in consecutive sweeps"""

    class RefOscSource(Enum):
        """Reference Oscillator source used with SENSe:ROSCillator:SOURCE"""
        NONE = 0
        """No reference oscillator, free running"""
        INTERNAL = 1
        """Internal reference oscillator source (if available)"""
        EXTERNAL = 2
        """External reference oscillator source (if available)"""

    class RefOscStatus(Enum):
        """Status of reference oscillator used with SENSe:ROSCillator:STATus"""
        OFF = 0
        """Reference oscillator PLL is disabled, i.e. during power-off"""
        HOLDOVER = 1
        """Reference oscillator PLL is in holdover mode (source lost)"""
        LOCKING = 2
        """Reference oscillator PLL is trying to lock to selected reference"""
        LOCKED = 3
        """Reference oscillator PLL is locked to selected reference"""
        LOCK = 3
        """Deprecated"""

    # Enums for TRIGger subsystem
    class TrigSource(Enum):
        """Trigger source used with TRIGger:SOURce"""
        IMMEDIATE = 0
        """A trigger will commence immediately after the device is initiated"""
        EXTERNAL = 1
        """An external trigger input is used for triggering the acquisition"""
        INTERNAL = 2
        """An internal trigger signal is used for triggering the acquisition"""

    # Data type information container
    class AcqDTypeInfo(NamedTuple):
        min: Optional[Union[int, complex]]
        max: Optional[Union[int, complex]]
        mag: Optional[int]
        np: np.dtype

    # Enums/Flags for AcquisitionHeader
    class AcqDType(Enum):
        """Acquisition Datatype used in acquisition header"""
        S16RLE = 0
        """Signed 16 bit (real), little endian"""
        S16RILE = 4
        """Signed 16 bit (real, imaginary), little endian"""
        S32RLE = 8
        """Signed 32 bit (real), little endian"""
        S32RILE = 12
        """Signed 32 bit (real, imaginary), little endian"""
        S64RLE = 16
        """Signed 64 bit (real), little endian"""
        S64RILE = 20
        """Signed 64 bit (real, imaginary), little endian"""
        F64DTMALE = 32
        """Compound datatype of 64 bit float (distance, propagation time, magnitude, angle)"""

        @property
        def info(self) -> 'SenseX1000Base.AcqDTypeInfo':
            """Information about data type as AcqDTypeInfo object"""
            return {
                self.S16RLE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-32768, max=32767, mag=32768, np=np.dtype('<i2')),
                self.S16RILE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-32768-32768j, max=32767+32767j, mag=32768, np=np.dtype([('re', '<i2'), ('im', '<i2')])),
                self.S32RLE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-2147483648, max=2147483647, mag=2147483648, np=np.dtype('<i4')),
                self.S32RILE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-2147483648-2147483648j, max=2147483647+2147483647j, mag=2147483648, np=np.dtype([('re', '<i4'), ('im', '<i4')])),
                self.S64RLE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-9223372036854775808, max=9223372036854775807, mag=0x8000000000000000, np=np.dtype('<i8')),
                self.S64RILE.value: SenseX1000Base.AcqDTypeInfo(
                    min=-9223372036854775808-9223372036854775808j, max=9223372036854775807+9223372036854775807j, mag=9223372036854775808, np=np.dtype([('re', '<i8'), ('im', '<i8')])),
                self.F64DTMALE.value: SenseX1000Base.AcqDTypeInfo(
                    min=None, max=None, mag=None, np=np.dtype([('dist', '<f8'), ('time', '<f8'), ('mag', '<f8'), ('angle', '<f8')]))
            }[self.value]

    class AcqFlags(Flag):
        """Acquisition flags used in acquisition header"""
        INVALID = 1 << 1
        """Configuration and/or data are invalid for processing"""
        INFINITE = 1 << 2
        """Acquisition contains infinite number of sweeps"""
        SDOMAIN = 1 << 4
        """Sweep Domain data"""
        RDOMAIN = 1 << 5
        """Range Domain data"""
        DIRECTION = 1 << 8
        """Falling (0) or rising (1) slope of first sweep in acquisition"""
        ALTERNATING = 1 << 9
        """Constant (0) or alternating (1) sweep slope for multiple sweep acquisitions"""

    class AcqSubheaderFlags(IntFlag):
        """Acquisition subheader flags"""
        ACQTIMING = 1 << 4
        """Header includes timestamp information"""
        TIMEAXIS = 1 << 8
        """Header includes time axis information"""
        FREQAXIS = 1 << 9
        """Header includes frequency axis information"""
        ENVINFO = 1<<11
        """Header includes Environmental information"""
        SUPPDATA = 1 << 12
        """Header includes supplemental data information"""

    class AcqSubheaderAcqTiming(NamedTuple):
        """Class representing a timing subheader"""
        # header fields as named tuple entries.
        # Note that the order of these entries must match the binary header format
        trigger_timestamp: int
        """Timestamp of trigger in nanoseconds UTC since 1970-01-01 00:00:00"""
        trigger_delay: int
        """Delay between trigger event and acquisition start in nanoseconds"""
        sweep_period: int
        """The period with which sweeps are carried out in nanoseconds"""

        @classmethod
        def _struct(cls) -> struct.Struct:
            return struct.Struct('<8xQQQ')

        @classmethod
        def _npdtype(cls) -> np.dtype:
            return np.dtype({'names': cls._fields,
                             'formats': [np.uint64, np.uint64, np.uint64]})

        @classmethod
        def _flag(cls) -> 'SenseX1000Base.AcqSubheaderFlags':
            return SenseX1000Base.AcqSubheaderFlags.ACQTIMING

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqSubheaderAcqTiming':
            # Get struct object, unpack binary data and create the NamedTuple object
            s = cls._struct()
            buffer = stream.read(s.size)
            return cls(*s.unpack(buffer))

        @classmethod
        def _from_array(cls, array: np.array) -> 'SenseX1000Base.AcqSubheaderAcqTiming':
            return cls(**{k: t(array[k]) for k, t in get_type_hints(cls).items()})

        def __array__(self):
            # Convert this subheader into a numpy structured array for better hdf5 serialization
            return np.array([tuple(self)], self._npdtype())

    class AcqSubheaderTimeAxis(NamedTuple):
        """Class representing a time axis subheader"""
        # header fields as named tuple entries.
        # Note that the order of these entries must match the binary header format
        start: float
        """Start value of the axis"""
        stop: float
        """Stop value of the axis"""

        @classmethod
        def _struct(cls) -> struct.Struct:
            return struct.Struct('<8xd8xd')

        @classmethod
        def _npdtype(cls) -> np.dtype:
            return np.dtype({'names': cls._fields,
                             'formats': [np.float64, np.float64]})

        @classmethod
        def _flag(cls) -> 'SenseX1000Base.AcqSubheaderFlags':
            return SenseX1000Base.AcqSubheaderFlags.TIMEAXIS

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqSubheaderTimeAxis':
            # Get struct object, unpack binary data and create the NamedTuple object
            s = cls._struct()
            buffer = stream.read(s.size)
            return cls(*s.unpack(buffer))

        @classmethod
        def _from_array(cls, array: np.array) -> 'SenseX1000Base.AcqSubheaderTimeAxis':
            return cls(**{k: t(array[k]) for k, t in get_type_hints(cls).items()})

        def __array__(self):
            # Convert this subheader into a numpy structured array for better hdf5 serialization
            return np.array([tuple(self)], self._npdtype())

        @property
        def delta(self) -> float:
            return self.stop - self.start

    class AcqSubheaderFreqAxis(NamedTuple):
        """Class representing a time axis subheader"""
        # header fields as named tuple entries.
        # Note that the order of these entries must match the binary header format
        start: float
        """Start value of the axis"""
        stop: float
        """Stop value of the axis"""

        @classmethod
        def _struct(cls) -> struct.Struct:
            return struct.Struct('<8xd8xd')

        @classmethod
        def _npdtype(cls) -> np.dtype:
            return np.dtype({'names': cls._fields,
                             'formats': [np.float64, np.float64]})

        @classmethod
        def _flag(cls) -> 'SenseX1000Base.AcqSubheaderFlags':
            return SenseX1000Base.AcqSubheaderFlags.FREQAXIS

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqSubheaderFreqAxis':
            # Get struct object, unpack binary data and create the NamedTuple object
            s = cls._struct()
            buffer = stream.read(s.size)
            return cls(*s.unpack(buffer))

        @classmethod
        def _from_array(cls, array: np.array) -> 'SenseX1000Base.AcqSubheaderFreqAxis':
            return cls(**{k: t(array[k]) for k, t in get_type_hints(cls).items()})

        def __array__(self):
            # Convert this subheader into a numpy structured array for better hdf5 serialization
            return np.array([tuple(self)], self._npdtype())

        @property
        def delta(self) -> float:
            return self.stop - self.start

    class AcqSubheaderEnvironmentalInfo(NamedTuple):
        """Class representing environmental data"""
        class AcqSubheaderEnvironmentalInfoItem(NamedTuple):
            address0: int
            address1: int
            address2: int
            address3: int
            address4: int
            address5: int
            age: int
            rssi: int
            battery: float
            temperature: float
            humidity: float
            pressure: float

            @classmethod
            def _struct(cls) -> struct.Struct:
                return struct.Struct('<BBBBBBBbffffxxxxxxxx')

            @classmethod
            def _npdtype(cls) -> np.dtype:
                return np.dtype({'names': cls._fields,
                                 'formats': [np.uint8, np.uint8, np.uint8, np.uint8, np.uint8, np.uint8,
                                             np.uint8, np.int8, np.float32, np.float32, np.float32, np.float32]})
            @classmethod
            def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqSubheaderEnvironmentalInfo.AcqSubheaderEnvironmentalInfoItem':
                s = cls._struct()
                buffer = stream.read(s.size)
                return cls(*s.unpack(buffer))

            @classmethod
            def _from_array(cls, array: np.array) -> 'SenseX1000Base.AcqSubheaderEnvironmentalInfo.AcqSubheaderEnvironmentalInfoItem':
                  return cls(**{k: t(array[k]) for k, t in get_type_hints(cls).items()})

            @property
            def address(self) -> Tuple[int, int, int, int, int, int]:
                return (self.address0, self.address1, self.address2,
                        self.address3, self.address4, self.address5)

        items: List[AcqSubheaderEnvironmentalInfoItem]

        @classmethod
        def _flag(cls) -> 'SenseX1000Base.AcqSubheaderFlags':
            return SenseX1000Base.AcqSubheaderFlags.ENVINFO

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqSubheaderEnvironmentalInfo':
            # Get struct object, unpack binary data and create the NamedTuple object
            n_items = 4
            buffer = stream.read(cls.AcqSubheaderEnvironmentalInfoItem._struct().size * n_items)
            bytesio = io.BytesIO(buffer)

            items = [cls.AcqSubheaderEnvironmentalInfoItem._from_stream(bytesio) for i in range(n_items)]

            return cls(items)

        @classmethod
        def _from_array(cls, array: np.array) -> 'SenseX1000Base.AcqSubheaderEnvironmentalInfo':
            return cls([cls.AcqSubheaderEnvironmentalInfoItem._from_array(t) for t in array])

        def __array__(self):
            # Convert this subheader into a numpy structured array for better hdf5 serialization
            return np.array([self.items], self.AcqSubheaderEnvironmentalInfoItem._npdtype())

        @property
        def sensors(self) -> List[dict]:
            attrs = ['address', 'age', 'rssi', 'battery', 'temperature', 'humidity', 'pressure']
            return [{k: getattr(item, k) for k in attrs} for item in self.items]

    class AcqSubheaderSupplementalData(NamedTuple):
        """Class representing supplemental data subheader"""
        class AcqSubHeaderSupplementalDataItem(NamedTuple):
            data_points: int
            data_size: int
            data_type: int
            data_flags: int

            @classmethod
            def _struct(cls) -> struct.Struct:
                return struct.Struct('<LBBH')

            @classmethod
            def _npdtype(cls) -> np.dtype:
                return np.dtype({'names': cls._fields,
                                 'types': [np.uint32, np.uint8, np.uint8, np.uint16]})

            @classmethod
            def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqSubheaderSupplementalData.AcqSubHeaderSupplementalDataItem':
                # Get struct object, unpack binary data and create the NamedTuple object
                s = cls._struct()
                buffer = stream.read(s.size)
                return cls(*s.unpack(buffer))

            @classmethod
            def _from_array(cls, array: np.array) -> 'SenseX1000Base.AcqSubheaderSupplementalData.AcqSubHeaderSupplementalDataItem':
                return cls(**{k: t(array[k]) for k, t in get_type_hints(cls).items()})

            @property
            def dtype(self) -> 'SenseX1000Base.AcqDType':
                return SenseX1000Base.AcqDType(self.data_type)

        items: List[AcqSubHeaderSupplementalDataItem]

        @classmethod
        def _flag(cls) -> 'SenseX1000Base.AcqSubheaderFlags':
            return SenseX1000Base.AcqSubheaderFlags.SUPPDATA

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqSubheaderSupplementalData':
            # Get struct object, unpack binary data and create the NamedTuple object
            n_items = 4
            buffer = stream.read(cls.AcqSubHeaderSupplementalDataItem._struct().size * n_items)
            bytesio = io.BytesIO(buffer)

            items = [cls.AcqSubHeaderSupplementalDataItem._from_stream(bytesio) for i in range(n_items)]

            return cls(items)

        @classmethod
        def _from_array(cls, array: np.array):
            return cls([cls.AcqSubHeaderSupplementalDataItem._from_array(t) for t in array])

        def __array__(self):
            # Convert this subheader into a numpy structured array for better hdf5 serialization
            return np.array([self.items], self.AcqSubHeaderSupplementalDataItem._npdtype())


    class AcqBaseHeader(NamedTuple):
        """Class representing the header prepended to every acquisition"""
        # header fields as named tuple entries.
        # Note that the order of these entries must match the binary header format
        header_length: int
        """Binary header size"""
        header_id: int
        """Binary header identifier"""
        header_version: int
        """Binary header version"""
        flags: int
        """Acquisition flags as integer"""
        bytes_total: int
        """Total number of bytes in acquisition"""
        sweep_count: int
        """Number of sweeps in acquisition"""
        trace_mask: int
        """Bitmask of enabled traces in acquisition"""
        data_points: int
        """Number of points per trace"""
        data_size: int
        """Size of datatype in bytes"""
        data_type: int
        """Datatype identifier"""
        acq_index: int
        """Index of acquisition"""
        subheader_flags: int
        """Indication of included subheaders"""
        subhdr_acq_timing: 'SenseX1000Base.AcqSubheaderAcqTiming' = None
        """Acquisition timing subheader"""
        subhdr_time_axis: 'SenseX1000Base.AcqSubheaderTimeAxis' = None
        """Time axis subheader"""
        subhdr_freq_axis: 'SenseX1000Base.AcqSubheaderFreqAxis' = None
        """Frequency axis subheader"""
        subhdr_env_info:  'SenseX1000Base.AcqSubheaderEnvironmentalInfo' = None
        """Environmental info subheader"""
        subhdr_supp_data: 'SenseX1000Base.AcqSubheaderSupplementalData' = None
        """Supplemental data subheader"""

        @classmethod
        def _struct(cls) -> struct.Struct:
            # Return a Python struct object for parsing the binary header into the named tuple
            return struct.Struct('<HBBLLLLLBBLH')

        @classmethod
        def _version(cls) -> int:
            # Return version supported by this NamedTuple
            return 1

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqBaseHeader':
            # Get struct object, unpack binary data and create the NamedTuple object
            s = cls._struct()
            buffer = stream.read(s.size)
            header = cls(*s.unpack(buffer))
            assert header.header_version == cls._version(), f'Unsupported header version: {header.header_version:x}'
            return header

        @classmethod
        def _from_dict(cls, attr_dict: dict) -> 'SenseX1000Base.AcqBaseHeader':
            # Filter dictionary for keys that we require for instantiation
            header_dict = {k: attr_dict[k] for k in attr_dict.keys()
                           if k in SenseX1000Base.AcqBaseHeader._fields
                           and k not in SenseX1000Base.AcqBaseHeader._field_defaults}

            # Get required types required for instantiation
            header_types = get_type_hints(cls)

            # Convert fields to correct data type
            header_dict = {k: header_types[k](*v) if isinstance(v, Iterable) else header_types[k](v)
                               for k, v in header_dict.items()}

            # Create the base header object
            header = cls(**header_dict)
            assert header.header_version == cls._version(), f'Unsupported header version: {header.header_version:x}'
            return header


    class AcqHeader(AcqBaseHeader):
        @classmethod
        def _subheaders(cls) -> dict:
            return {
                # The order of this subheader list matters.
                # They must be in the order they would be occuring in the header
                'subhdr_acq_timing': SenseX1000Base.AcqSubheaderAcqTiming,
                'subhdr_time_axis': SenseX1000Base.AcqSubheaderTimeAxis,
                'subhdr_freq_axis': SenseX1000Base.AcqSubheaderFreqAxis,
                'subhdr_env_info': SenseX1000Base.AcqSubheaderEnvironmentalInfo,
                'subhdr_supp_data': SenseX1000Base.AcqSubheaderSupplementalData
            }

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.AcqHeader':
            # Create the base header object
            baseheader = SenseX1000Base.AcqBaseHeader._from_stream(stream)
            subheaders_dict = {}

            # Read all subheaders
            subheaders_length = baseheader.header_length - baseheader._struct().size
            if subheaders_length > 0:
                subheaders_buffer = stream.read(subheaders_length)
                subheaders_iostream = io.BytesIO(subheaders_buffer)

                # Build a list of subheader objects from the subheader table, when they
                # are indicated in the baseheader.subheader_flags attribute
                subheaders_dict = {a: c._from_stream(subheaders_iostream) for a, c in cls._subheaders().items()
                                   if baseheader.subheader_flags & c._flag()}

            # Combine baseheader and subheaders
            header_dict = baseheader._asdict()
            header_dict.update(subheaders_dict)

            # Return new AcqHeader object, created from baseheader and subheaders
            return cls(**header_dict)

        @classmethod
        def _from_dict(cls, attr_dict: dict) -> 'SenseX1000Base.AcqHeader':
            baseheader = SenseX1000Base.AcqBaseHeader._from_dict(attr_dict)
            subheaders_dict = {}

            # Read subheaders
            subheaders_length = baseheader.header_length - baseheader._struct().size
            if subheaders_length > 0:
                # Build a list of subheader objects from the subheader table, when they
                # are indicated in the baseheader.subheader_flags attribute
                subheaders_dict = {a: c._from_array(attr_dict[a][0]) for a, c in cls._subheaders().items()
                                   if baseheader.subheader_flags & c._flag()}

            # Combine baseheader and subheaders
            header_dict = baseheader._asdict()
            header_dict.update(subheaders_dict)

            # Return new AcqHeader object, created from baseheader and subheaders
            return cls(**header_dict)

        @property
        def trace_map(self) -> List[int]:
            """List of traces enabled in this acquisition"""
            mask = self.trace_mask
            lst = []
            i = 0
            while mask > 0:
                if mask & (1 << i):
                    lst += [i]
                    mask = mask & ~(1 << i)
                i += 1
            return lst

        @property
        def trace_count(self) -> int:
            """Number of traces enabled in this acquisition"""
            return len(self.trace_map)

        @property
        def trace_size(self) -> int:
            """Total size of single trace in bytes"""
            size = self.data_points * self.data_size
            if self.subhdr_supp_data is not None:
                # Add size of supplemental data if it exists
                size += sum([i.data_points * i.data_size for i in self.subhdr_supp_data.items])
            return size

        @property
        def sweep_size(self) -> int:
            """Total size of sweep in bytes"""
            return self.trace_count * self.trace_size

        @property
        def acq_dtype(self) -> 'SenseX1000Base.AcqDType':
            """Acqusition data type as AcqDType object"""
            return SenseX1000Base.AcqDType(self.data_type)

        @property
        def acq_flags(self) -> 'SenseX1000Base.AcqFlags':
            """Acquisition flags as AcqFlags object"""
            return SenseX1000Base.AcqFlags(self.flags)

        @property
        def trig_timestamp(self) -> np.datetime64:
            timestamp = self.subhdr_acq_timing.trigger_timestamp if self.subhdr_acq_timing is not None else None
            return np.datetime64(timestamp, 'ns')

        @property
        def trig_delay(self) -> np.datetime64:
            delay = self.subhdr_acq_timing.trigger_delay if self.subhdr_acq_timing is not None else None
            return np.timedelta64(delay, 'ns')

        @property
        def sweep_period(self) -> np.timedelta64:
            timedelta = self.subhdr_acq_timing.sweep_period if self.subhdr_acq_timing is not None else None
            return np.timedelta64(timedelta, 'ns')

        @property
        def time_axis(self) -> Optional[np.ndarray]:
            if self.subhdr_time_axis is None:
                return None
            start, stop = self.subhdr_time_axis.start, self.subhdr_time_axis.stop
            axis = np.linspace(start, stop, self.data_points)
            axis.setflags(write=False)
            return axis

        @property
        def freq_axis(self) -> Optional[np.ndarray]:
            if self.subhdr_freq_axis is None:
                return None
            start, stop = self.subhdr_freq_axis.start, self.subhdr_freq_axis.stop
            axis = np.linspace(start, stop, self.data_points)
            axis.setflags(write=False)
            return axis

        @property
        def time_step(self) -> Optional[float]:
            """Returns delta-time per point"""
            if self.subhdr_time_axis is None:
                return None
            return self.subhdr_time_axis.delta / self.data_points

        @property
        def freq_step(self) -> Optional[float]:
            """Returns delta-frequency per point"""
            if self.subhdr_freq_axis is None:
                return None
            return self.subhdr_freq_axis.delta / self.data_points

        @property
        def environmental_info(self) -> Optional[dict]:
            if self.subhdr_env_info is None:
                return None
            # drop all invalid sensors
            sensors = [sensor for sensor in self.subhdr_env_info.sensors if not all(a == 0 for a in sensor['address'])]

            # Reformat as dict
            return {':'.join([f'{item:02x}' for item in sensor['address']]): {k: v for k, v in sensor.items() if k != 'address'}
                     for sensor in sensors}

    class AcqData(NamedTuple):
        """Class representing an acquisition data object holding data for one or more consecutive sweeps"""
        header: 'SenseX1000Base.AcqHeader'
        """Copy of the acquisition header to which this data container belongs"""
        array: np.ndarray
        """Acquisition data as numpy array with shape N_sweeps x N_traces x N_points"""
        supplemental_data: List[Optional[np.ndarray]]
        """List of supplemental data arrays that is attached to the acquisition data"""
        n_sweeps: int
        """Number of sweeps in this container"""
        n_traces: int
        """Number of traces per sweep"""
        n_points: int
        """Number of points per trace"""
        trace_map: list
        """Mapping of the trace index in the data array to the respective trace number"""
        seq_nums: range
        """List of sweep sequence numbers with respect to entire acquisition for each sweep in data array"""
        sweep_dirs: list
        """List of sweep directions for each sweep in data array as sign value (-1, +1)"""
        timestamps: List[np.datetime64]
        """List of timestamps for each sweep in data array as UTC since 1970-01-01 00:00:00 in 1 ns resolution"""
        time_axes: List[np.ndarray]
        """List of time axes for each sweep in data array"""
        freq_axes: List[np.ndarray]
        """List of frequency axes for each sweep in data array"""


        @classmethod
        def _from_stream(cls, stream: BinaryIO, header: 'SenseX1000Base.AcqHeader', seq_num: int, n_sweeps: int) -> 'SenseX1000Base.AcqData':
            # Calculate and read requested number of bytes from stream and create an AcqData object
            stream_data = stream.read(n_sweeps * header.trace_count * header.trace_size)

            # Extract the actual acquisition data
            seq_nums = range(seq_num, seq_num + n_sweeps)
            shape = [n_sweeps, header.trace_count, header.data_points]
            strides = [header.sweep_size, header.trace_size, header.data_size]
            array = np.frombuffer(stream_data, offset=0, dtype=header.acq_dtype.info.np)
            array.setflags(write=False)
            data = [np.lib.stride_tricks.as_strided(array, shape, strides)]

            if header.subhdr_supp_data is not None:
                # Also extract supplemental data if available
                offset = header.data_points * header.data_size

                for item in header.subhdr_supp_data.items:
                    if item.data_points > 0 and item.data_size > 0:
                        length = item.data_points * item.data_size
                        shape = [n_sweeps, header.trace_count, item.data_points]
                        strides = [header.sweep_size, header.trace_size, item.data_size]
                        array = np.frombuffer(stream_data, offset=offset, dtype=item.dtype.info.np)
                        array.setflags(write=False)
                        data.append(np.lib.stride_tricks.as_strided(array, shape, strides))
                        offset += length
                    else:
                        data.append(None)

            return SenseX1000Base.AcqData._create(header, data[0], data[1:], seq_nums)

        @classmethod
        def _create(cls, header: 'SenseX1000Base.AcqHeader', array: np.ndarray, supplemental_data: List[Optional[np.ndarray]], seq_nums: range) -> 'SenseX1000Base.AcqData':
            # Construct object from binary data, current header and sweep sequence number/number of sweeps
            sweep_dir = 1 if header.acq_flags & SenseX1000Base.AcqFlags.DIRECTION else -1
            sweep_dirs = [(-sweep_dir if seq_num % 2 else sweep_dir)
                               if header.acq_flags & SenseX1000Base.AcqFlags.ALTERNATING
                               else sweep_dir for seq_num in seq_nums]

            return SenseX1000Base.AcqData(
                header=header,
                array=array,
                supplemental_data=supplemental_data,
                n_sweeps=len(seq_nums),
                n_traces=header.trace_count,
                n_points=header.data_points,
                trace_map=header.trace_map,
                seq_nums=seq_nums,
                sweep_dirs=sweep_dirs,
                timestamps=[header.trig_timestamp + header.trig_delay + seq_num * header.sweep_period for seq_num in seq_nums],
                time_axes=[header.time_axis for seq_num in seq_nums],
                freq_axes=[(np.flip(header.freq_axis) if seq_num % 2 else header.freq_axis)
                              if header.acq_flags & SenseX1000Base.AcqFlags.ALTERNATING and
                                 header.acq_flags & SenseX1000Base.AcqFlags.SDOMAIN else header.freq_axis
                              for seq_num in seq_nums]
            )


        def to_hdf5(self, parent: Union['h5py.Group', str], name: Optional[str] = None, **kwargs) -> 'h5py.Group':
            """Serializes an AcqData object into a HDF5 representation and adds it under the given HDF5 group"""
            if not H5PY_AVAILABLE:
                raise RuntimeError("This feature requires the h5py library to be installed.")

            if isinstance(parent, str):
                # When string is given as parent, treat it as a filename
                parent = h5py.File(parent, 'a')

            if name is None:
                timestamp = str(
                    self.header.trig_timestamp) if self.header.trig_timestamp is not None else datetime.datetime.utcnow().isoformat()
                range = f'{self.seq_nums.start}:{self.seq_nums.stop}'
                name = f'{timestamp}[{range}]'

            # Create group as a container for the acquisition data
            group = parent.create_group(name)
            group.attrs.create('COMMENT', 'This group contains 2piSENSE sensor measurement data with header attributes')

            # Add header data as attrs to group
            for field in self.header._fields:
                # This converts each field of the header into a HDF5 attribute in a numpy (array/scalar) representation
                data = getattr(self.header, field)
                if data is not None:
                    group.attrs.create(name=field, data=np.array(data))

            # Create the primary dataset
            acq_dataset = group.create_dataset(name='acquisition_data', data=self.array, **kwargs)
            acq_dataset.attrs.create('COMMENT', 'The main data array with various convenience attributes')
            # Create supplemental datasets
            supplemental_dataset_refs = np.full((len(self.supplemental_data),), h5py.Reference(False), dtype=h5py.ref_dtype)
            for idx, supplemental_data in enumerate(self.supplemental_data):
                if supplemental_data is not None:
                    supplemental_dataset = group.create_dataset(name=f'supplemental_data[{idx}]', data=supplemental_data, **kwargs)
                    supplemental_dataset.attrs.create('COMMENT', 'Supplemental data array as reported by the sensor')
                    supplemental_dataset_refs[idx] = supplemental_dataset.ref

            # Setup dimensions
            acq_dataset.dims[0].label = 'sweep'
            acq_dataset.dims[1].label = 'trace'
            acq_dataset.dims[2].label = 'point'

            seq_num_scale = group.create_dataset(name='seq_nums', data=self.seq_nums)
            seq_num_scale.attrs.create('COMMENT', 'Sequence numbers for each performed sweep')
            seq_num_scale.make_scale()
            sweep_dirs_scale = group.create_dataset(name='sweep_dirs', data=self.sweep_dirs)
            sweep_dirs_scale.attrs.create('COMMENT', 'Sweep directions for each performed sweep')
            sweep_dirs_scale.make_scale()
            timestamps_scale = group.create_dataset(name='timestamps', data=np.array(self.timestamps).astype(np.int64))
            timestamps_scale.attrs.create('COMMENT', 'UTC timestamps in nanoseconds since 1970-01-01T00:00:00 for each performed sweep')
            timestamps_scale.make_scale()
            trace_map_scale = group.create_dataset(name='trace_map', data=self.header.trace_map)
            trace_map_scale.attrs.create('COMMENT', 'List of mapped traces for each recorded trace')
            trace_map_scale.make_scale()

            acq_dataset.dims[0].attach_scale(seq_num_scale)
            acq_dataset.dims[0].attach_scale(sweep_dirs_scale)
            acq_dataset.dims[0].attach_scale(timestamps_scale)
            acq_dataset.dims[1].attach_scale(trace_map_scale)

            # Create axes datasets and scales
            if self.header.subhdr_freq_axis is not None:
                freqaxis_scale = group.create_dataset(name='freq_axis', data=self.header.freq_axis)
                freqaxis_scale.attrs.create('COMMENT', 'Primary axis with instantaneous frequency for each data point')
                freqaxis_scale.make_scale()
                acq_dataset.dims[2].attach_scale(freqaxis_scale)

                # When in alternating mode and data is sweep domain take care of reversed frequency axis
                if  self.header.acq_flags & SenseX1000Base.AcqFlags.ALTERNATING and \
                    self.header.acq_flags & SenseX1000Base.AcqFlags.SDOMAIN:
                    freqaxis_scale_2nd = group.create_dataset(name='freq_axis_2nd', data=np.flip(self.header.freq_axis))
                    freqaxis_scale_2nd.attrs.create('COMMENT', 'Secondary axis with instantaneous frequency for each data point')
                    freqaxis_scale_2nd.make_scale()
                    acq_dataset.dims[2].attach_scale(freqaxis_scale_2nd)
                    freqaxes_refs = [freqaxis_scale.ref if (seq_num % 2) == 0 else freqaxis_scale_2nd.ref for seq_num in self.seq_nums]
                else:
                    freqaxes_refs = [freqaxis_scale.ref for seq_num in self.seq_nums]

                freqaxes_scale = group.create_dataset(name='freq_axes', data=np.array(freqaxes_refs, dtype=h5py.ref_dtype))
                freqaxes_scale.attrs.create('COMMENT', 'References to the used frequency axis for each sweep')
                freqaxes_scale.make_scale()
                acq_dataset.dims[0].attach_scale(freqaxes_scale)
                freqaxes_scale_ref = freqaxes_scale.ref
            else:
                freqaxes_scale_ref = h5py.Reference(False)

            if self.header.subhdr_time_axis is not None:
                timeaxis_scale = group.create_dataset(name='time_axis', data=self.header.time_axis)
                timeaxis_scale.attrs.create('COMMENT', 'Instantaneous sample time for each data point')
                timeaxis_scale.make_scale()
                acq_dataset.dims[2].attach_scale(timeaxis_scale)
                timeaxes_refs = [timeaxis_scale.ref for seq_num in self.seq_nums]
                timeaxes_scale = group.create_dataset(name='time_axes', data=np.array(timeaxes_refs, dtype=h5py.ref_dtype))
                timeaxes_scale.attrs.create('COMMENT', 'References to the used time axis for each sweep')
                timeaxes_scale.make_scale()
                acq_dataset.dims[0].attach_scale(timeaxes_scale)
                timeaxes_scale_ref = timeaxes_scale.ref
            else:
                timeaxes_scale_ref = h5py.Reference(False)

            # Create some references and other special types to acq_dataset
            acq_dataset.attrs.create(name='header', data=group.ref)
            acq_dataset.attrs.create(name='array', data=acq_dataset.ref)
            acq_dataset.attrs.create(name='supplemental_data', data=supplemental_dataset_refs)
            acq_dataset.attrs.create(name='timestamps', data=timestamps_scale.ref) # Timestamps in nanoseconds
            acq_dataset.attrs.create(name='seq_nums', data=seq_num_scale.ref)
            acq_dataset.attrs.create(name='sweep_dirs', data=sweep_dirs_scale.ref)
            acq_dataset.attrs.create(name='freq_axes', data=freqaxes_scale_ref)
            acq_dataset.attrs.create(name='time_axes', data=timeaxes_scale_ref)

            # And additional attrs as well
            for field in self._fields:
                if field not in acq_dataset.attrs.keys():
                    data = getattr(self, field)
                    if data is not None:
                        acq_dataset.attrs.create(name=field, data=np.array(data))

            return group

        @classmethod
        def from_hdf5(cls, parent: Union['h5py.Group', str], name: str, **kwargs) -> 'SenseX1000Base.AcqData':
            """Creates an AcqData object from a h5py group or filename"""
            if not H5PY_AVAILABLE:
                raise RuntimeError("This feature requires the h5py library to be installed.")

            if isinstance(parent, str):
                # When string is given as parent, treat it as a filename
                parent = h5py.File(parent, 'r')

            # This raises an exception if 'name' cannot be found in parent
            if not isinstance(parent[name], h5py.Group) or 'acquisition_data' not in parent[name].keys():
                raise TypeError(f'\'{parent[name].name}\' does not seem to be a loadable AcqData object')

            group = parent[name]
            acq_data = group['acquisition_data']

            if 'header' not in acq_data.attrs:
                raise ValueError(f'{group} is missing acquisition header information')

            # Deserialize the header
            header_dict = dict(group[acq_data.attrs['header']].attrs)
            header = SenseX1000Base.AcqHeader._from_dict(header_dict)

            # Read data
            array = group[acq_data.attrs['array']][:]
            array.setflags(write=False)
            data = [array]

            if header.subhdr_supp_data is not None:
                # Also extract supplemental data if available
                for idx, item in enumerate(header.subhdr_supp_data.items):
                    if item.data_points > 0 and item.data_size > 0:
                        array = group[acq_data.attrs['supplemental_data'][idx]][:]
                        array.setflags(write=False)
                        data.append(array)
                    else:
                        data.append(None)

            seq_nums = group[acq_data.attrs['seq_nums']][:]

            # Create data object
            acqData = SenseX1000Base.AcqData._create(header, data[0], data[1:], range(seq_nums[0], seq_nums[0] + len(seq_nums)))

            return acqData

    class Acquisition(object):
        """Container class representing an entire acquisition"""
        _header: 'SenseX1000Base.AcqHeader'
        _stream: BinaryIO

        @classmethod
        def _from_stream(cls, stream: BinaryIO) -> 'SenseX1000Base.Acquisition':
            """Create acquisition header from the device data stream and instantiate an Acquisition object"""
            header = SenseX1000Base.AcqHeader._from_stream(stream)
            return SenseX1000Base.Acquisition(header=header, stream=stream)

        def __init__(self, header: 'SenseX1000Base.AcqHeader', stream: BinaryIO):
            # Initialize variables required acquisition logic
            self._header = header
            self._stream = stream
            self._sweeps_remaining = header.sweep_count
            self._seq_num = 0

        @property
        def header(self):
            """The header object associated with this acquisition"""
            return self._header

        @property
        def sweeps_remaining(self):
            """The number of sweeps that can still be read from this acquisition"""
            return self._sweeps_remaining

        @property
        def seq_num(self):
            """The sequence number of the acquisition next to be read"""
            return self._seq_num

        def read(self, n_sweeps=-1) -> 'SenseX1000Base.AcqData':
            """Read given number of sweeps (or all sweeps by default) from device"""
            if (self._header.acq_flags & SenseX1000Base.AcqFlags.INFINITE):
                # This acquisition has an infinite amount of sweeps.
                # Thus we require the n_sweeps parameter to be set
                if n_sweeps == -1: raise ValueError('n_sweeps parameter needs to be set for infinite acquisitions')
            else:
                # Determine actual number of sweeps available to be read
                # Create data object from device stream
                # Advance variables
                n_sweeps = self._sweeps_remaining if n_sweeps < 0 else min(n_sweeps, self._sweeps_remaining)
                self._sweeps_remaining -= n_sweeps

            data = SenseX1000Base.AcqData._from_stream(self._stream, self._header, self._seq_num, n_sweeps)
            self._seq_num += n_sweeps

            return data

        def data(self, n_sweeps=1):
            """Returns a generator object producing an AcqData object with given number of sweeps per iteration"""

            # generator syntax
            while (self._sweeps_remaining > 0) or (self._header.acq_flags & SenseX1000Base.AcqFlags.INFINITE):
                yield self.read(n_sweeps=n_sweeps)

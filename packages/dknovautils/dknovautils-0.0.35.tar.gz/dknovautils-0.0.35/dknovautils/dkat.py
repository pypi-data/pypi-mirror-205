
import dknovautils
from dknovautils.commons import *

import beepy


DkAppVer = '0.0.35'
_unknown_err = '_unknown_err4035'


class AT(object):

    _innerLoggerFun_ = None

    _AstErrorCnt_ = 0

    __logger = None

    @classmethod
    def log(cls, loggerName='dkn'):
        if cls.__logger is None:
            logger = logging.getLogger(loggerName)
            cls.__logger = logger

        return cls.__logger

    @staticmethod
    def log_loggerFun(loggerName='dkn', initInnerLoggerFun=True, beepError=True, beepWarn=False):

        logger = logging.getLogger(loggerName)

        def mloggerFun(obj, llevel):
            assert isinstance(llevel, LLevel)
            if False:
                pass
            elif llevel == LLevel.Trace:
                # 也用debug级别。只是在prod模式下可以关闭。
                logger.debug(obj)
            elif llevel == LLevel.Debug:
                logger.debug(obj)
            elif llevel == LLevel.Info:
                logger.info(obj)
            elif llevel == LLevel.Warn:
                logger.warning(obj)
                if beepWarn:
                    AT.beep_error_buffered()
            elif llevel == LLevel.Error:
                logger.error(obj)
                if beepError:
                    AT.beep_error_buffered()
            else:
                assert False, f"bad {llevel}"

            pass

        if initInnerLoggerFun:
            AT._innerLoggerFun_ = mloggerFun

        return mloggerFun

    _LOG_FORMAT_100 = "%(asctime)s - %(levelname)s - %(message)s"
    _DATE_FORMAT_100 = "%m/%d/%Y %H:%M:%S %p"
    # _DATE_FORMAT_iso_simple = "%m/%d/%Y %H:%M:%S %p"

    STRFMT_ISO_COMPACT_SIMPLE = "%Y%m%dT%H%M%S"
    STRFMT_ISO_COMPACT_ALL_A = "%Y%m%dT%H%M%SS%f"
    STRFMT_ISO_ALL_A = "%Y-%m-%dT%H:%M:%S,%f%Z"

    _LOG_FORMAT_106 = '%(asctime)s %(name)s %(threadName)s %(levelname)s %(message)s'

    '''
    
    dtstr = datetime.now().strftime("%Y%m%dT%H%M%S")

        
    '''

    @classmethod
    def log_basicConfig(cls, filename='tmp_test.log', loggerName='dkn', initInnerLoggerFun=True):

        logging.basicConfig(filename=filename, level=logging.NOTSET,
                            format=cls._LOG_FORMAT_106,
                            # datefmt=cls._DATE_FORMAT_100,
                            force=True)

        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            cls._LOG_FORMAT_106)

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        mloggerFun = AT.log_loggerFun(loggerName, initInnerLoggerFun)

        return mloggerFun

    @staticmethod
    def assertAllNotNone(*args):
        assert isinstance(args, tuple)
        AT.assert_(all(_ is not None for _ in args),
                   'err7540 some value is None')

    @staticmethod
    def deg_to_rad(d):
        return d/180.0*math.pi

    __beep_last_time = 0

    @staticmethod
    def beep_error_buffered(tone='ping'):
        '''
        在0.5秒内最多播放一次 类似防止按钮双击的效果

        '''
        t = 0.5
        now = AT.fepochSecs()
        if now < AT.__beep_last_time+t:
            return
        else:
            AT.__beep_last_time = now
            AT.beep(tone)

    @staticmethod
    def beep(tone='ping'):
        beepy.beep(sound=tone)

    @staticmethod
    def beep2():
        #!wget -q -T 1 http://localhost:333/hello
        print('\7')

    @staticmethod
    def never(s=None):
        AT.assert_(False,  s if s is not None else 'never come here')

    @staticmethod
    def checksys():
        assert sys.version_info >= (3, 11)

    @staticmethod
    def fepochMillis() -> int:
        millisec = int(AT.fepochSecs() * 1000)
        return millisec

    _last_epochsecs = 0.0

    @classmethod
    def fepochSecs(cls) -> float:
        '''
         time.monotonic()不是epoch值。fuck

        '''
        # return time.monotonic()
        r = time.time()
        if r <= cls._last_epochsecs:
            return cls._last_epochsecs
        else:
            cls._last_epochsecs = r
            return r

    '''
        # dd/mm/YY H:M:S
    dts = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dts)

    # 20200101T120000
    dts = datetime.now().strftime("%Y%m%dT%H%M%S")
    print("date and time =", dts)
    
    
    '''

    @staticmethod
    def sdf_isocompact_format_datetime(dt, *, precise: str = 'a'):
        assert precise in ['a', 'd', 's'], 'err5554 bad precise'

        if dt is not None:
            AT.unsupported()

        dt = datetime.now()
        dts = dt.strftime(AT.STRFMT_ISO_COMPACT_ALL_A)

        if precise == 'a':
            pass
        elif precise == 's':
            dts = dts[:(8+0+1+6)]
        elif precise == 'd':
            dts = dts[:(8)]
        else:
            AT.never()

        return dts

    @staticmethod
    def sdf_logger():
        pass

    @staticmethod
    def _now_dt():

    @staticmethod
    def sdf_logger_format_datetime(dt: int = None, *, precise: str = 'a') -> str:
        '''
https://strftime.org/    
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
https://man7.org/linux/man-pages/man3/strftime.3.html

2023-12-01T08:30:00.123456

"yyyy-MM-ddTHH:mm:ss"

date -I

d date
s seconds
a all

        '''
        assert precise in ['a', 'd', 's'], 'err5554 bad precise'

        if dt is not None:
            dt = datetime.fromtimestamp(dt/1000, tz=None)
        else:
            dt = datetime.now()

        dts = dt.strftime(AT.STRFMT_ISO_ALL_A)

        if precise == 'a':
            pass
        elif precise == 's':
            dts = dts[:(10+1+8)]
        elif precise == 'd':
            dts = dts[:(10)]
        else:
            AT.never()

        return dts

    @staticmethod
    def assert_(b: bool, s: str = None):
        # 改成完善的形式

        assert isinstance(b, bool)

        if b:
            return

        AT._AstErrorCnt_ += 1
        msg = _unknown_err if s is None else s

        dknovautils.commons.iprint_error(msg)

        raise DkAstException(msg)

    @staticmethod
    def mychdir(s):
        assert isinstance(s, str) and len(s) > 0
        iprint_debug(f'chdir: {s}')
        os.chdir(s)

    @staticmethod
    def never(s=None):
        AT.assert_(False, f"should never come here {s}")

    @staticmethod
    def astTrace(b: bool, s: str):
        '''在prod中完全不需要的'''
        AT.assert_(b, s)

    @staticmethod
    def unsupported(s: str = None):
        AT.assert_(False, s if s is not None else 'err8255 unsupported 不支持的功能')

    @staticmethod
    def unimplemented(s: str = None):
        AT.assert_(False, s if s is not None else 'err4823 unimplemented 未实现的功能')

    VERSION = DkAppVer


class DkAstException(Exception):
    pass


'''

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='/mnt/d/tmp/demo0726.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)





'''


from dknovautils.dk_imports import *


from dknovautils.dkat import *

from dknovautils.dkipy import *


def write_async():
    pass


def dtprint(s: str):
    print(s)


def iprint(obj):
    iprint_info(obj)


def iprint_trace(obj):
    _iprint(obj, level=LLevel.Trace)


def iprint_debug(obj):
    _iprint(obj, level=LLevel.Debug)


def iprint_info(obj):

    _iprint(obj, level=LLevel.Info)


def iprint_warn(obj):
    _iprint(obj, level=LLevel.Warn)


def iprint_error(obj):
    _iprint(obj, level=LLevel.Error)


_log_inited = False


def _iprint(obj, level: LLevel):

    if AT._innerLoggerFun_ is not None:
        AT._innerLoggerFun_(obj, level)
        return
    else:
        pass

    # now = datetime.now()
    # dts = now.strftime("%d/%m/%Y %H:%M:%S")
    # otstr = now.isoformat()[:(10 + 1 + 8+4)]

    # _FORMAT_111 = '%(asctime)s %(message)s'
    # logging.basicConfig(format=_FORMAT)

    global _log_inited
    if not _log_inited:
        _log_inited = True

        # 只在没有配置的时候起作用 不会重复执行
        logging.basicConfig(level=logging.NOTSET,
                            format=AT._LOG_FORMAT_106)

    # 采用这个将级别提升一下。不知为何 NotSET的设置没有生效 并不会打印。
    if level == LLevel.Trace:
        level = LLevel.Debug

    logging.log(level.value, obj)

    return

    if False:

        otstr2 = datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%dT%H:%M:%S.%f")[0:23]

        msg = f'[{otstr}]{obj}'

    print(f"[{otstr}][{level.name.lower()}]{obj}")

# _myCntInfos = {}


'''

https://docs.python.org/3/howto/logging.html



class NoteItem(val ctime: Long, val msg: String?, val cnt: Long, val useTime: Long?) {

  val ctimeStr get() = AT.sdf_logger().format(Date(ctime))
}

class MyCntInfo(val title: String) {
  var cnt: Long = 0
  var items: LinkedList<NoteItem> = LinkedList()
  var utime: Long = 0

  val utimeStr get() = AT.sdf_logger().format(Date(utime))

}

'''

'''


@dataclass
class NoteItem:
    ctime: int
    cnt: int
    msg: str = None   # 这个字段是没有缺省值的
    useTime: int = None

    def ctimeStr(self) -> str:

        return 0 * 0


class DkCntInfoUtils(object):

    @staticmethod
    def recordCnt(_key, _cnt=1, _msg: str = None, _useTime: int = None):
        pass

    pass



'''

# ���ڴ���Զ��������
# ������ʱ��package����Ҫ�쳣�����ʲ�Ϊ�ļ�˽�б���
import physicsLab._colorUtils as _colorUtils

def warning(msg: str) -> None:
    _colorUtils.printf(msg, _colorUtils.YELLOW)

# ��ʵ���쳣
class openExperimentError(Exception):
    pass

class wireColorError(Exception):
    pass

class wireNotFoundError(Exception):
    def __str__(self):
        return "Unable to delete a nonexistent wire"
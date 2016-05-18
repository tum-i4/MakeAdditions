import abc


class Transformer(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def canBeAppliedOn(cmd: str) -> bool:
        return False

    @staticmethod
    @abc.abstractmethod
    def applyTransformationOn(cmd: str, container) -> str:
        return cmd

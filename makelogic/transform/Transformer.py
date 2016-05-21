import abc


class TransformerBase(metaclass=abc.ABCMeta):
    """ Container class for all transformations """

    @staticmethod
    @abc.abstractmethod
    def canBeAppliedOn(cmd: str) -> bool:
        return False

    @staticmethod
    @abc.abstractmethod
    def applyTransformationOn(cmd: str, container) -> str:
        return cmd


class TransformerSingle(TransformerBase):
    """ Container class for all single instruction commands """
    pass


class TransformerMulti(TransformerBase):
    """ Container class for all multi instruction commands """
    pass

# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class OculusTouchButtons(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsOculusTouchButtons(cls, buf, offset):
        n = tdw.flatbuffers.encode.Get(tdw.flatbuffers.packer.uoffset, buf, offset)
        x = OculusTouchButtons()
        x.Init(buf, n + offset)
        return x

    # OculusTouchButtons
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # OculusTouchButtons
    def Left(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # OculusTouchButtons
    def Right(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # OculusTouchButtons
    def LeftAxis(self, j):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(tdw.flatbuffers.number_types.Float32Flags, a + tdw.flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # OculusTouchButtons
    def LeftAxisAsNumpy(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(tdw.flatbuffers.number_types.Float32Flags, o)
        return 0

    # OculusTouchButtons
    def LeftAxisLength(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # OculusTouchButtons
    def RightAxis(self, j):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(tdw.flatbuffers.number_types.Float32Flags, a + tdw.flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # OculusTouchButtons
    def RightAxisAsNumpy(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.GetVectorAsNumpy(tdw.flatbuffers.number_types.Float32Flags, o)
        return 0

    # OculusTouchButtons
    def RightAxisLength(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def OculusTouchButtonsStart(builder): builder.StartObject(4)
def OculusTouchButtonsAddLeft(builder, left): builder.PrependInt32Slot(0, left, 0)
def OculusTouchButtonsAddRight(builder, right): builder.PrependInt32Slot(1, right, 0)
def OculusTouchButtonsAddLeftAxis(builder, leftAxis): builder.PrependUOffsetTRelativeSlot(2, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(leftAxis), 0)
def OculusTouchButtonsStartLeftAxisVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def OculusTouchButtonsAddRightAxis(builder, rightAxis): builder.PrependUOffsetTRelativeSlot(3, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(rightAxis), 0)
def OculusTouchButtonsStartRightAxisVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def OculusTouchButtonsEnd(builder): return builder.EndObject()

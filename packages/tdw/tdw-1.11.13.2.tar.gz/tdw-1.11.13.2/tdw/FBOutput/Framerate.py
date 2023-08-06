# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class Framerate(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFramerate(cls, buf, offset):
        n = tdw.flatbuffers.encode.Get(tdw.flatbuffers.packer.uoffset, buf, offset)
        x = Framerate()
        x.Init(buf, n + offset)
        return x

    # Framerate
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # Framerate
    def TargetFramerate(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Framerate
    def FrameDt(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # Framerate
    def PhysicsTimeStep(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def FramerateStart(builder): builder.StartObject(3)
def FramerateAddTargetFramerate(builder, targetFramerate): builder.PrependInt32Slot(0, targetFramerate, 0)
def FramerateAddFrameDt(builder, frameDt): builder.PrependFloat32Slot(1, frameDt, 0.0)
def FramerateAddPhysicsTimeStep(builder, physicsTimeStep): builder.PrependFloat32Slot(2, physicsTimeStep, 0.0)
def FramerateEnd(builder): return builder.EndObject()

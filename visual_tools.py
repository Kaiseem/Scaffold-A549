from mayavi import mlab
import random
from tvtk.util.ctf import ColorTransferFunction, PiecewiseFunction

def volshow(scalar, label=False, cmax=1300, gif=False, gifname=None):
    assert scalar.dtype in [np.uint8,np.int32, np.int16], 'input volume should be integer'
    fig = mlab.figure(size=(900, 900), bgcolor=(0, 0, 0), fgcolor=(1, 1, 1))
    if label:
        color = [[i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255] for i in range(1, cmax + 1, 1)]
        color.insert(0, [0, 0, 0, 0, 0])
    else:
        color = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 0], [255, 255, 255, 255, 255]]
    m = mlab.pipeline.volume(mlab.pipeline.scalar_field(scalar), name='colored map')
    ctf = ColorTransferFunction()
    otf = PiecewiseFunction()
    for c in color:
        ctf.add_rgb_point(c[0], c[1] / 255., c[2] / 255.0, c[3] / 255.0)
        otf.add_point(c[0], c[4] / 255.)
    m._cft = ctf
    m._volume_property.set_color(ctf)
    m._volume_property.shade = False
    m._volume_property.interpolation_type = 0
    m.update_ctf = True
    m._otf = otf
    m._volume_property.set_scalar_opacity(otf)
    mlab.outline()
    if not gif:
        mlab.show()
    else:
        assert gifname is not None, 'gifname should be determined'
        import moviepy.editor as mpy
        def make_frame(t):
            f = mlab.gcf()
            f.scene._lift()
            mlab.view(azimuth=360 * t / duration, distance=1200)
            return mlab.screenshot(antialiased=True)
        mlab.orientation_axes()
        duration = 5
        animation = mpy.VideoClip(make_frame, duration=duration)
        animation.write_gif(gifname, fps=12)

if __name__=='__main__':
    import numpy as np
    a=np.load(r'test\sf_a549_21.npy').transpose((1,2,0))[:,:,::-1]
    volshow(a,label=False,gif=True,gifname='E:/image.gif')
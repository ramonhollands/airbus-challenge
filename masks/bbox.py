import numpy as np

class bbox(object):

    t = (0,0); r = (0,0); b = (0,0); l = (0,0)

    def __init__(self):
        pass

    def get_as_list(self):
        return [self.t,self.r,self.l,self.b]

    def point_as_str(self, p):
        return str(p[0]) + ' ' + str(p[1])

    def get_as_str(self):
        return self.point_as_str(self.t) + " " + self.point_as_str(self.r) + " " + self.point_as_str(self.l) + " " + self.point_as_str(self.b)

    def from_mask(self, mask_rle, shape=(768,768)):
        '''
            returns four corners for the mask
            top (y,x), right (y,x), left (y,x), bottom (y,x)
            '''
        t = (0, shape[1])  # top(and most right)
        r = (0, 0)  # right (and most bottom)
        l = (shape[0], 0)  # left (and most top)
        b = (0, 0)  # bottom (and most left)

        s = mask_rle.split()
        starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]

        # points = []
        for start, length in zip(starts, lengths):
            (x, y) = divmod(start, shape[1])

            y_length = y + length
            # points.append((x, y))

            # top(and most right)
            if (y < t[1] or (y == t[1] and x > t[0])):
                t = (x, y)

            # right (and most bottom)
            if (x > r[0] or (x == r[0] and y_length > r[1])):
                r = (x, y_length)

            # bottom (and most left)
            if (y_length > b[1] or (y_length == b[1] and x < b[0])):
                b = (x, y_length)

            # left (and most top)
            if (x < l[0] or (x == l[0] and y < l[1])):
                l = (x, y)

        xi = 0
        yi = 1

        self.t = (t[yi], t[xi])
        self.r = (r[yi], r[xi])
        self.l = (l[yi], l[xi])
        self.b = (b[yi], b[xi])

        return self

    def from_string(self, s):

        ps = s.split()

        self.t = (int(ps[0]), int(ps[1]))
        self.r = (int(ps[2]), int(ps[3]))
        self.l = (int(ps[4]), int(ps[5]))
        self.b = (int(ps[6]), int(ps[7]))

        return self

    def plot_line(self, plt, f, t, color='y'):
        plt.plot([f[1], t[1]], [f[0], t[0]], color=color, linestyle='-', linewidth=4)

    def plot_rectangle(self, plt):
        self.plot_line(plt, self.l, self.t, 'r')
        self.plot_line(plt, self.t, self.r, 'r')
        self.plot_line(plt, self.r, self.b, 'r')
        self.plot_line(plt, self.b, self.l, 'r')

    def plot_bbox(self, plt):
        self.plot_rectangle(plt)
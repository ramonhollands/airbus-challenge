class CoordTransform(Transform):
    """ A coordinate transform.  """

    def make_lines(self, coordinates, image):

        """ # y = np.array([y1,x1,y2,x2,y3,x3,y4,x4]) """
        r, c, *_ = image.shape
        output_image = np.zeros((r, c))

        coordinates = coordinates.astype(np.int)
        [ty, tx, ry, rx, ly, lx, by, bx] = coordinates

        rr, cc = line(ty, tx, ry, rx)
        output_image[rr, cc] = 1

        rr, cc = line(ly, lx, by, bx)
        output_image[rr, cc] = 1

        return output_image

    @staticmethod
    def get_bbox_coordinates(image):

        '''
        returns four corners for the mask in numpy format (y,x)
        top (y,x), right (y,x), left (y,x), bottom (y,x)
        '''
        shape = image.shape
        nonzeros = image.nonzero()
        rows, cols = nonzeros

        ty = np.min(rows)
        lx = np.min(cols)
        by = np.max(rows)
        rx = np.max(cols)

        tops = []; lefts = []; rights =[]; bottoms = []

        points = np.transpose(nonzeros)

        # points = []
        # todo refactor, remove for loop
        for point in points:
            [y,x] = point

            #top(and most right)
            if(y==ty):
                tops.append([y,x])

            #right (and most bottom)
            if(x==rx):
                rights.append([y,x])

            #bottom (and most left)
            if(y==by):
                bottoms.append([y,x])

            #left (and most top)
            if(x==lx):# or (x==l[1] and y<l[0])):
                lefts.append([y,x])

        yi = 0; xi = 1
        if(lefts[0][yi] < rights[0][yi]):
            t = [tops[0][yi], tops[-1][xi]]
            l = [lefts[0][yi], lefts[0][xi]]
            r = [rights[-1][yi], rights[-1][xi]]
            b = [bottoms[-1][yi], bottoms[0][xi]]
        else:
            t = [tops[0][yi], tops[0][xi]]
            l = [lefts[-1][yi], lefts[0][xi]]
            r = [rights[0][yi], rights[-1][xi]]
            b = [bottoms[-1][yi], bottoms[-1][xi]]

        return np.array([t[yi], t[xi], r[yi], r[xi], l[yi], l[xi], b[yi], b[xi]], dtype=np.float32)

    def transform_coord(self, x, ys):

        #create two lines (from top to right and from left to bottom)
        image_y = self.make_lines(ys,x)

        #rotate these two lines
        image_y_tr = self.do_transform(image_y, True)

        #get the new rotated bounding box coordinates
        y_tr = CoordTransform.get_bbox_coordinates(image_y_tr)

        x = self.do_transform(x, False)
        return x, np.concatenate([y_tr])
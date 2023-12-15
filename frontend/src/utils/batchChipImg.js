import cv from "@techstark/opencv-js";

const batchChipImg = (settings, range, batch_chip, type) => {
  if (settings.imgUrl) {
    try {
      if (cv.getBuildInformation) {
        const image = settings.imgUrl;
        const subrange = range[settings.chip_type];

        let img = image;
        if (type === "chip") img = image.roi(new cv.Rect(100, 90, 600, 300));

        const thres = new cv.Mat();
        cv.threshold(
          img,
          thres,
          subrange[type].threshold,
          255,
          cv.THRESH_BINARY_INV,
        );

        const anchor = new cv.Point(-1, -1);
        const border_val = cv.morphologyDefaultBorderValue();
        const c_ones = cv.Mat.ones(
          subrange[type].close_y,
          subrange[type].close_x,
          cv.CV_8U,
        );
        const close = new cv.Mat();
        cv.morphologyEx(
          thres,
          close,
          cv.MORPH_CLOSE,
          c_ones,
          anchor,
          1,
          cv.BORDER_CONSTANT,
          border_val,
        );

        const e_ones = cv.Mat.ones(
          subrange[type].erode_y,
          subrange[type].erode_x,
          cv.CV_8U,
        );
        const erode = new cv.Mat();
        cv.erode(
          close,
          erode,
          e_ones,
          anchor,
          1,
          cv.BORDER_CONSTANT,
          border_val,
        );

        cv.imshow(batch_chip.current[type].current, erode);

        const contours = new cv.MatVector();
        const hierarchy = new cv.Mat();
        cv.findContours(
          erode,
          contours,
          hierarchy,
          cv.RETR_EXTERNAL,
          cv.CHAIN_APPROX_SIMPLE,
        );

        const res = contours.size();

        thres.delete();
        c_ones.delete();
        close.delete();
        e_ones.delete();
        erode.delete();
        contours.delete();
        hierarchy.delete();

        return res;
      }
    } catch (e) {
      console.log(e);
    }
  }
};

export default batchChipImg;

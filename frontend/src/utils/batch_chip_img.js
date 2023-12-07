import cv from "@techstark/opencv-js";

const batch_chip_img = (settings, range, batch_chip, type) => {
  if (settings[type + "Url"] !== null) {
    try {
      const image = settings[type + "Url"];
      const subrange = range[settings.chip_type];

      const thres = new cv.Mat();
      cv.threshold(
        image,
        thres,
        subrange[type].threshold,
        255,
        cv.THRESH_BINARY_INV,
      );

      const c_ones = cv.Mat.ones(
        subrange[type].close_y,
        subrange[type].close_x,
        cv.CV_8U,
      );
      const close = new cv.Mat();
      cv.morphologyEx(thres, close, cv.MORPH_CLOSE, c_ones);

      const e_ones = cv.Mat.ones(
        subrange[type].erode_y,
        subrange[type].erode_x,
        cv.CV_8U,
      );
      const erode = new cv.Mat();
      cv.morphologyEx(close, erode, cv.MORPH_ERODE, e_ones);

      cv.imshow(batch_chip.current[type].current, erode);

      thres.delete();
      c_ones.delete();
      close.delete();
      e_ones.delete();
      erode.delete();
    } catch (e) {
      console.log(e);
    }
  }
};

export default batch_chip_img;

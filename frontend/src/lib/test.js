export async function fakeProcessAPI(mode, item, lotNo, formData) {
  await new Promise((resolve) => setTimeout(resolve, 1000));

  return {
    unique_key: "ABCD1234567890",
    directory: "CDC/gcm/1234567890/temp",
    defect_batches: [
      {
        batch_no: 1,
        defect_files: [
          {
            file_name: "1234567890_temp_939.png",
            norm_x_center: "0.773153",
            norm_y_center: "0.770182",
            defect_mode: "temp",
          },
          {
            file_name: "1234567890_temp_2965.png",
            norm_x_center: "0.041896",
            norm_y_center: "0.306182",
            defect_mode: "temp",
          },
        ],
      },
      {
        batch_no: 2,
        defect_files: [
          {
            file_name: "1234567890_temp_1584.png",
            norm_x_center: "0.187707",
            norm_y_center: "0.610909",
            defect_mode: "temp",
          },
          {
            file_name: "1234567890_temp_2964.png",
            norm_x_center: "0.053197",
            norm_y_center: "0.306182",
            defect_mode: "temp",
          },
        ],
      },
      {
        batch_no: 3,
        defect_files: [
          {
            file_name: "1234567890_temp_1724.png",
            norm_x_center: "0.783352",
            norm_y_center: "0.585455",
            defect_mode: "temp",
          },
          {
            file_name: "1234567890_temp_2963.png",
            norm_x_center: "0.148842",
            norm_y_center: "0.306182",
            defect_mode: "temp",
          },
        ],
      },
      {
        batch_no: 4,
        defect_files: [],
      },
      {
        batch_no: 5,
        defect_files: [],
      },
      {
        batch_no: 6,
        defect_files: [],
      },
    ],
  };
}

export async function fakeItemAPI(lotNo) {
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // return { item: "" };
  return { item: "GCM32ER71E106KA59_+B55-E01GJ" };
}

export async function fakeInfoAPI() {
  await new Promise((resolve) => setTimeout(resolve, 1000));

  return { plate_no: "test" };
}

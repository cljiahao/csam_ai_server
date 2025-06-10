import { useState } from "react";

import { useInfoBarContext } from "@/features/info-bar/contexts/InfoBarContext";
import { useFetchColors } from "@/features/info-bar/api/info-bar";
import useBaseStore from "@/store/base";
import useImageStore from "@/store/image";
import useMarksStore from "@/store/marks";
import showUploadToast from "../components/showUploadToast";
import useFormValidation from "./useFormValidation";
import useImageProcess from "./useImageProcess";

const useUploadFormDialog = ({ mode }) => {
  const [isDialogOpen, setDialogOpen] = useState(false);
  const { setItem, setLotNo, setPlateNo, setSaved, handleSaveUserInput } =
    useInfoBarContext();

  const updateError = useBaseStore((state) => state.updateError);
  const setError = useImageStore((state) => state.setError);
  const markRef = useMarksStore((state) => state.markRef);

  const { mutateAsync: fetchColors } = useFetchColors(updateError);

  const {
    state: { formRef, uploadFormInfo },
    action: { onSubmit, onReset, uploadForm },
  } = useFormValidation();

  const {
    action: { processImage, setImage },
  } = useImageProcess();

  const handleDialogOpen = () => {
    if (!isDialogOpen) {
      const item = uploadForm.getValues("item");
      const lotNo = uploadForm.getValues("lotNo");
      handleSaveUserInput({ mode, item, lotNo });
      uploadForm.setValue("item", "");
    }
    setDialogOpen((prevState) => !prevState);
  };

  const onFileChange = async (e) => {
    e.preventDefault();
    setError("");
    const file = e.target.files[0];
    if (file) {
      const item = uploadForm.getValues("item");
      const lotNo = uploadForm.getValues("lotNo");
      showUploadToast(item, lotNo, file.name);
      setDialogOpen(false);

      setItem(item);
      setLotNo(lotNo);
      setPlateNo(file.name.split(".")[0]);
      setImage(URL.createObjectURL(file));

      const formData = new FormData();
      formData.append("file", file);

      const colors = await fetchColors({ item });
      const fileBatchDirectory = await processImage({
        mode,
        item,
        lotNo,
        formData,
      });
      const filteredDefectFiles = fileBatchDirectory.file_data_batches.flatMap(
        (batch) =>
          batch.defect_records
            .filter((file) => file.defect_mode !== "temp")
            .map((file) => ({
              file_name: file.file_name,
              defect_mode: file.defect_mode,
            })),
      );
      filteredDefectFiles.forEach(({ file_name, defect_mode }) => {
        const colorObj = colors.find((color) => color.label === defect_mode);
        if (!colorObj) return;
        markRef?.current?.addMark(file_name, {
          name: colorObj.label,
          color: colorObj.color,
          radius: 1,
        });
      });
    }
    setSaved(false);
  };

  return {
    state: { isDialogOpen, formRef, uploadFormInfo },
    action: { handleDialogOpen, uploadForm, onSubmit, onReset, onFileChange },
  };
};

export default useUploadFormDialog;

import { useState } from "react";

import showUploadToast from "../components/showUploadToast";
import useFormValidation from "./useFormValidation";
import { useInfoBarContext } from "@/features/info-bar/contexts/InfoBarContext";
import useImageProcess from "./useImageProcess";
import useImageStore from "@/store/image";

const useUploadFormDialog = ({ mode }) => {
  const [isDialogOpen, setDialogOpen] = useState(false);
  const setError = useImageStore((state) => state.setError);
  const { setItem, setLotNo, setPlateNo } = useInfoBarContext();

  const {
    state: { formRef, uploadFormInfo },
    action: { onSubmit, onReset, uploadForm },
  } = useFormValidation();

  const {
    action: { fetchColors, processImage, setImage },
  } = useImageProcess();

  const handleDialogOpen = () => {
    if (!isDialogOpen) {
      uploadForm.setValue("item", "");
    }
    setDialogOpen((prevState) => !prevState);
  };

  const onFileChange = (e) => {
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

      fetchColors({ item });
      processImage({ mode, item, lotNo, formData });
    }
  };

  return {
    state: { isDialogOpen, ref: formRef, uploadFormInfo },
    action: { handleDialogOpen, uploadForm, onSubmit, onReset, onFileChange },
  };
};

export default useUploadFormDialog;

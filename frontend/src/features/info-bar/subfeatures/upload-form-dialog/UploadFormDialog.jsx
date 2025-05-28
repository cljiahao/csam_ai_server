import { v4 as uuidv4 } from "uuid";
import { useQueryClient } from "@tanstack/react-query";

import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import CustomDialog from "@/components/widgets/custom-dialog/CustomDialog";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import CustomFormField from "@/components/widgets/custom-form-field/CustomFormField";
import { navigation_info } from "@/core/navigation";
import { toast } from "@/hooks/use-toast";
import { resetStore } from "@/store/resetStore";
import useBaseStore from "@/store/base";
import useFormValidation from "./hooks/useFormValidation";
import useImageProcess from "./hooks/useImageProcess";
import useSaveUserInput from "../../hooks/useSaveUserInput";
import useColorUtility from "../utility-panel/hooks/useColorUtility";
import { useState } from "react";
import { useShallow } from "zustand/react/shallow";
import { useItemStore } from "../../store/item";
import { useLotNoStore } from "../../store/lotNo";
import { usePlateNoStore } from "../../store/plateNo";

const UploadFormDialog = ({ mode }) => {
  const [isSaved, setSaved] = useState(true);
  const { error, updateError } = useBaseStore(
    useShallow((state) => ({
      error: state.error,
      updateError: state.updateError,
    })),
  );

  const { item, setItem } = useItemStore(
    useShallow((state) => ({
      item: state.item,
      setItem: state.setItem,
    })),
  );

  const { lotNo, setLotNo } = useLotNoStore(
    useShallow((state) => ({
      lotNo: state.lotNo,
      setLotNo: state.setLotNo,
    })),
  );

  const setPlateNo = usePlateNoStore((state) => state.setPlateNo);

  const nav = navigation_info.find((nav) => nav.name === mode);
  const queryClient = useQueryClient();
  const {
    state: { ref, uploadFormInfo },
    action: { onSubmit, onReset, uploadForm },
  } = useFormValidation();

  const {
    state: { isDialogOpen },
    action: { setDialogOpen, handleImageProcess },
  } = useImageProcess();

  const {
    action: { handleSaveUserInput },
  } = useSaveUserInput();

  const {
    action: { fetchColors },
  } = useColorUtility(updateError);

  const handleDialogOpen = () => {
    if (!isDialogOpen) {
      uploadForm.setValue("item", "");
      handleSaveUserInput({ mode, item, lotNo });
      if (!error) {
        setSaved(true);
      }
    }
    setDialogOpen((prevState) => !prevState);
  };

  const onFileChange = (e) => {
    e.preventDefault();

    const file = e.target.files[0];
    if (file) {
      queryClient.removeQueries();
      resetStore();

      const item = uploadForm.getValues("item");
      const lotNo = uploadForm.getValues("lotNo");

      setDialogOpen(false);
      setItem(item);
      setLotNo(lotNo);
      setPlateNo(file.name.split(".")[0]);

      toast({
        title: "You submitted the following values:",
        description: (
          <pre className="mt-2 flex w-[340px] flex-col rounded-md bg-slate-950 p-4">
            <kbd className="text-white">Lot No: {lotNo}</kbd>
            <kbd className="text-white">File Name: {file.name}</kbd>
            <kbd className="text-white">Item: {item}</kbd>
          </pre>
        ),
        duration: 2000,
      });

      fetchColors({ item }).then((data) => {
        let colors = [];
        if (data?.dot_colors_list.length > 0) {
          colors = data.dot_colors_list;
        } else {
          colors = [
            { uuid: uuidv4(), defect_label: "NG", hex_color: "#FFFF00" },
          ];
        }
        handleImageProcess(mode, item, lotNo, file, colors);
        setSaved(!isSaved);
      });
    }
  };

  return (
    <CustomDialog
      trigger={
        <HoverButton
          className={isSaved ? "" : "bg-red-300"}
          icon={nav.icon}
          hoverText={`${nav.name} Upload`}
        />
      }
      title={mode === "CDC" ? "Defects Collections" : "AI Predict Defects"}
      description="Upload image to start processing."
      open={isDialogOpen}
      onOpenChange={handleDialogOpen}
    >
      <Form {...uploadForm}>
        <form
          onSubmit={uploadForm.handleSubmit(onSubmit)}
          className="space-y-8 pt-4"
        >
          {Object.keys(uploadFormInfo).map((key) => {
            const { label, placeholder, onBlur, disabled } =
              uploadFormInfo[key];
            return (
              <CustomFormField
                control={uploadForm.control}
                key={key}
                name={key}
                label={label}
                placeholder={placeholder}
                onBlur={onBlur}
                disabled={disabled}
              />
            );
          })}
          <div className="flex-between flex">
            <HoverButton
              className="h-12 w-20"
              type="submit"
              hoverText="Upload"
            />
            <HoverButton
              className="h-12 w-20"
              hoverText="Reset"
              onClick={onReset}
            />
          </div>
        </form>
      </Form>
      <Input
        className="hidden"
        type="file"
        accept=".png, .jpg"
        ref={ref}
        onChange={onFileChange}
      />
    </CustomDialog>
  );
};

export default UploadFormDialog;

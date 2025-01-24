import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getItemType } from "@/services/api_retrieve";

const LOT_NO_REGEX = /^[a-zA-Z0-9]{10}$/;

const useLotNoMutation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["validateLotNo"],
    mutationFn: async (lotNo) => await getItemType(lotNo),
    onSuccess: (data) => {
      queryClient.setQueryData(["item"], data);
    },
    onError: (error) => {
      console.log(error);
      queryClient.removeQueries(["item"]); // Clear cache on error
    },
  });
};

const useFormValidation = () => {
  const queryClient = useQueryClient();
  const { mutate: validateLotNo, isLoading } = useLotNoMutation();
  const uploadFormInfo = {
    lotNo: {
      label: "Lot Number",
      placeholder: "1234567890",
      schema: z.string().regex(LOT_NO_REGEX, {
        message: "Lot Number must be exactly 10 alphanumeric characters.",
      }),
      onBlur: onLotNoBlur,
    },
    item: {
      label: "Item Type",
      placeholder: "GCM32ER71E106KA57",
      schema: z.string().min(1, {
        message: "Please key in Item Type.",
      }),
      disabled: !!queryClient.getQueryData(["item"]),
    },
  };

  const uploadSchema = z.object(
    Object.fromEntries(
      Object.entries(uploadFormInfo).map(([key, { schema }]) => [key, schema]),
    ),
  );
  const uploadForm = useForm({
    resolver: zodResolver(uploadSchema),
    defaultValues: Object.keys(uploadFormInfo).reduce((acc, key) => {
      acc[key] = "";
      return acc;
    }, {}),
  });

  function onLotNoBlur(e) {
    const value = e.currentTarget.value;
    if (!LOT_NO_REGEX.test(value)) return;
    validateLotNo(value, {
      onSuccess: (data) => {
        uploadForm.setValue("item", data?.item || "");
        uploadForm.trigger("item");
        if (!data?.item) uploadForm.setFocus("item");
      },
      onError: () => {
        uploadForm.setValue("item", "");
        uploadForm.trigger("item");
        uploadForm.setFocus("item");
      },
    });
  }

  const ref = useRef(null);
  function onSubmit() {
    ref?.current.click();
  }

  function onReset() {
    queryClient.removeQueries(["item"]); // Clear cache on error
    uploadForm.reset();
  }

  return {
    state: { ref, uploadFormInfo, isLoading },
    action: { onSubmit, onReset, uploadForm },
  };
};

export default useFormValidation;

import { useRef } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";

import {
  useLotNoMutation,
  useQueryItem,
} from "@/features/info-bar/api/info-bar";
import useBaseStore from "@/store/base";
import { QUERY_KEYS } from "@/constants/api-keys";

const LOT_NO_REGEX = /^[a-zA-Z0-9]{10}$/;

const useFormValidation = () => {
  const uploadFormInfo = {
    lotNo: {
      label: "Lot Number",
      placeholder: import.meta.env.VITE_TEST_LOT_NO,
      schema: z.string().regex(LOT_NO_REGEX, {
        message: "Lot Number must be exactly 10 alphanumeric characters.",
      }),
      onBlur: onLotNoBlur,
    },
    item: {
      label: "Item Type",
      placeholder: import.meta.env.VITE_TEST_ITEM,
      schema: z.string().min(1, {
        message: "Please key in Item Type.",
      }),
      disabled: !!useQueryItem(),
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

  const updateError = useBaseStore((state) => state.updateError);
  const { mutate: validateLotNo } = useLotNoMutation(updateError);
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

  const formRef = useRef(null);
  function onSubmit() {
    formRef?.current.click();
  }

  const queryClient = useQueryClient();
  function onReset() {
    queryClient.removeQueries([QUERY_KEYS.API_ITEM]);
    uploadForm.reset();
  }

  return {
    state: { formRef, uploadFormInfo },
    action: { uploadForm, onSubmit, onReset },
  };
};

export default useFormValidation;

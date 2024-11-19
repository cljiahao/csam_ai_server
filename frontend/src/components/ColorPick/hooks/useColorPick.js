import { toast } from "@/components/ui/use-toast";
import { useFolderHexContext } from "@/contexts/csamContext";

export function useColorPick({ itemType }) {
  const { folderHex, amendFolderHex } = useFolderHexContext();

  const colorSet = folderHex?.find(({ item }) => item === itemType);

  function addColorPick() {
    if (colorSet.colors.find(({ category }) => category === "Default")) {
      return toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "Default already exists. Change name to add more.",
        duration: 2000,
      });
    }

    const added_data = [
      ...colorSet.colors,
      { category: "Default", hex: "#00ffff" },
    ];

    amendFolderHex(itemType, added_data);
  }

  function removeColorPick(id) {
    const filtered_data = colorSet.colors.filter((item, index) => index != id);
    amendFolderHex(itemType, filtered_data);
  }

  function updateColorPick(e) {
    if (colorSet.colors.find(({ category }) => category === e.target.value)) {
      return toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: `${e.target.value} already exists. Change name to add more.`,
      });
    }

    const updated_data = colorSet.colors.map((inner, index) => {
      return index === Number(e.currentTarget.id)
        ? { ...inner, [e.currentTarget.name]: e.currentTarget.value }
        : inner;
    });

    amendFolderHex(itemType, updated_data);
  }

  return [colorSet, addColorPick, removeColorPick, updateColorPick];
}

import { MdCompare } from "react-icons/md";
import { LuArrowUpDown } from "react-icons/lu";

import CustomDialog from "@/components/widgets/custom-dialog/CustomDialog";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import LabelValue from "@/components/status/label_value";
import { Button } from "@/components/ui/button";
import { DataTable } from "@/components/widgets/data-table/DataTable";
import useModelHistory from "../hooks/useModelHistory";

const ModelHistory = () => {
  const {
    state: { isDialogOpen, allModelHistory, modelHistoryByItem },
    action: { handleDialogOpen },
  } = useModelHistory();
  console.log(allModelHistory);
  const tableColumns = [
    {
      accessorKey: "id",
      header: ({ column }) => {
        return (
          <Button
            className="text-sm underline"
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            S/N
            <LuArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        );
      },
    },
    {
      accessorKey: "date_install",
      header: "Date Installed",
    },
    {
      accessorKey: "item",
      header: "Item Type",
    },
    {
      accessorKey: "model_name",
      header: "Model Name",
    },
  ];

  return (
    <div className="grid w-full grid-cols-2 items-center">
      <CustomDialog
        className="h-5/6 w-5/6 max-w-full"
        trigger={
          <HoverButton
            icon={MdCompare}
            hoverText="Model History"
            className="h-10 w-32"
          />
        }
        title="Model History"
        description="History of Models installed / uploaded."
        open={isDialogOpen}
        onOpenChange={handleDialogOpen}
      >
        <DataTable
          className="bg-white bg-opacity-80"
          columns={tableColumns}
          data={allModelHistory ?? []}
        />
      </CustomDialog>
      <LabelValue
        className="flex-start"
        label="Date Created"
        value={modelHistoryByItem?.date_install}
        toColumn
      />
      <LabelValue
        className="col-span-2"
        label="Model Name"
        value={modelHistoryByItem?.model_name}
      />
    </div>
  );
};

export default ModelHistory;

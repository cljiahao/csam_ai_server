import { Label } from "@/components/ui/label";
import ColorPick from "@/components/ColorPick/ColorPick";
import { FolderHexProvider } from "@/contexts/csamProvider";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ModelsTable from "@/modules/ModelsTable/ModelsTable";


// TODO: Use TabsTrigger to trigger between settings and folderhex
// TODO: Settings page for folder hex add and delete
// TODO: Able to upload settings file and delete too.

const Settings = () => {
  const infoDetails = {
    item: "GCM32ER71E106KA59_+B55-E01GJ",
  };

  const tab_info = [
    {
      value: "Models",
      children: <ModelsTable />,
    },
    {
      value: "FolderHex",
      children: "Change your password here.",
    },
  ];

  return (
    <FolderHexProvider>
      <main className="flex h-screen max-h-screen w-screen overflow-hidden">
        <section className="w-full">
          <Tabs defaultValue="account" className="w-[400px]">
            <TabsList>
              {tab_info.map(({ value }) => (
                <TabsTrigger key={value} value={value}>
                  {value}
                </TabsTrigger>
              ))}
            </TabsList>
            {tab_info.map(({ value, children }) => (
              <TabsContent key={value} value={value}>
                {children}
              </TabsContent>
            ))}
          </Tabs>
        </section>
        <aside className="flex h-full w-5/12 flex-col border-l-2 border-slate-400">
          <ColorPick itemType={infoDetails.item}>
            <header className="hw-full flex-center gap-3">
              <Label className="flex-center h-full w-8">Item Type</Label>
              <Input className="flex-center hw-full text-wrap font-semibold" />
            </header>
          </ColorPick>
        </aside>
      </main>
    </FolderHexProvider>
  );
};

export default Settings;

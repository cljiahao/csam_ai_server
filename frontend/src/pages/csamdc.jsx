import { AppProvider } from "@/contexts/provider";
import { Separator } from "@/components/ui/separator";
import { Toaster } from "@/components/ui/toaster";
import { Gallery, ImageHolder, InfoBar } from "@/modules";

const page = "CDC";

const CsamDC = () => {
  return (
    <AppProvider>
      <main className="flex h-screen max-h-screen w-screen overflow-hidden">
        <section className="w-full">
          <ImageHolder />
        </section>
        <aside className="flex h-full w-3/5 flex-col border-l-2 border-slate-400">
          <InfoBar page={page} />
          <Separator className="h-[0.15em] bg-slate-400" />
          <Gallery page={page} />
        </aside>
      </main>
      <Toaster />
    </AppProvider>
  );
};

export default CsamDC;

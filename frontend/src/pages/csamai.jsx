import BaseLayout from "@/components/layouts/BaseLayout";
import { Separator } from "@/components/ui/separator";
import { ImageHolder, InfoBar, Gallery } from "@/features";

const CsamAI = () => {
  return (
    <BaseLayout>
      <section className="w-full">
        <ImageHolder />
      </section>
      <aside className="flex h-full w-3/5 flex-col border-l-2 border-slate-400">
        <InfoBar />
        <Separator className="h-[0.15em] bg-slate-400" />
        <Gallery />
      </aside>
    </BaseLayout>
  );
};

export default CsamAI;

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";

const MediaCard = ({
  className,
  children,
  title,
  description,
  descClassName,
}) => {
  return (
    <Card
      className={cn("flex-center h-full w-full flex-col space-y-2", className)}
    >
      <CardContent className="flex-center p-0">{children}</CardContent>
      <CardHeader className="flex-center p-0">
        <CardTitle className="break-all text-center">{title}</CardTitle>
        <CardDescription className={cn("text-wrap", descClassName)}>
          {description}
        </CardDescription>
      </CardHeader>
    </Card>
  );
};

export default MediaCard;

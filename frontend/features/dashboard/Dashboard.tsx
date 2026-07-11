import { UploadCloud, FileText, Download, Activity, PlayCircle } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";

export function Dashboard() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Upload Document</CardTitle>
            <CardDescription>
              Upload a STEM PDF to generate a PowerPoint lesson
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center justify-center rounded-lg border border-dashed p-10 text-center hover:bg-muted/50 transition-colors cursor-pointer">
              <UploadCloud className="mb-4 h-10 w-10 text-muted-foreground" />
              <h3 className="mb-1 text-lg font-semibold">Click or drag file to this area</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Supports Digital, Scanned, or Camera PDFs
              </p>
              <Button>Select PDF Document</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Active Processing</CardTitle>
            <CardDescription>Current document generation status</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  <span className="font-medium">Chapter_4_Vectors.pdf</span>
                </div>
                <Badge variant="secondary">Analyzing Subject</Badge>
              </div>
              <Progress value={33} className="h-2" />
              <p className="text-xs text-muted-foreground">
                Document Intelligence Engine identifying layout and equations...
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-muted-foreground" />
                  <span className="font-medium text-muted-foreground">Kinematics_Review.pdf</span>
                </div>
                <Badge variant="outline">Queued</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Projects</CardTitle>
            <CardDescription>Recently generated lessons</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: "Algebra Quadratic Equations", subject: "Mathematics", date: "2 hours ago" },
                { name: "Cellular Respiration", subject: "Biology", date: "Yesterday" },
                { name: "Newton's Laws", subject: "Physics", date: "2 days ago" },
              ].map((project, i) => (
                <div key={i} className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                      <PlayCircle className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm font-medium leading-none">{project.name}</p>
                      <p className="text-sm text-muted-foreground mt-1">{project.subject}</p>
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground">{project.date}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Download History</CardTitle>
            <CardDescription>Previously exported presentations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: "Algebra_Quadratic_Lesson.pptx", size: "2.4 MB", date: "2 hours ago" },
                { name: "Biology_Cells_Lesson.pptx", size: "5.1 MB", date: "Yesterday" },
                { name: "Physics_Newton_Lesson.pptx", size: "3.2 MB", date: "2 days ago" },
              ].map((file, i) => (
                <div key={i} className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
                      <Download className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <div>
                      <p className="text-sm font-medium leading-none">{file.name}</p>
                      <p className="text-sm text-muted-foreground mt-1">{file.size}</p>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">Download</Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
